#!/usr/bin/env python3
"""
Universe of Legends TCG — Google Drive to GitHub Auto-Sync Script
=================================================================
Automatically syncs:
1. Universe_of_Legends_v5.zip from "UofL game" folder (extracts index.html, UofL_v5.html, Assets, etc.)
2. Direct image additions/updates inside "Assets" folder
3. Direct card art additions/updates inside "Card_Images" folder
"""

import io
import json
import os
import sys
import zipfile
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from PIL import Image

UOFL_GAME_FOLDER_ID = os.environ.get("UOFL_GAME_FOLDER_ID", "1mNcsVt4O5QvL6npRBOEAgoc3jyH2ycm7")
ASSETS_FOLDER_ID = os.environ.get("ASSETS_FOLDER_ID", "1525qTxC8cIxsNOfzkyEO98oKh3FvUTD2")
CARD_IMAGES_FOLDER_ID = os.environ.get("CARD_IMAGES_FOLDER_ID", "1krDrBK95s6ZdQpiutz7iSw86mJkvOdNG")
STATE_FILE = ".drive_sync_state.json"


def get_drive_service():
    sa_json = os.environ.get("GDRIVE_SERVICE_ACCOUNT_JSON", "").strip()
    if not sa_json:
        print("ERROR: GDRIVE_SERVICE_ACCOUNT_JSON secret is not set.")
        sys.exit(1)
    creds_info = json.loads(sa_json)
    creds = service_account.Credentials.from_service_account_info(
        creds_info, scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)


def load_sync_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"files": {}}


def save_sync_state(state):
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, sort_keys=True)


def list_folder_files(service, folder_id):
    files = []
    page_token = None
    query = f"'{folder_id}' in parents and trashed = false"
    while True:
        resp = (
            service.files()
            .list(
                q=query,
                spaces="drive",
                fields="nextPageToken, files(id, name, mimeType, modifiedTime, md5Checksum)",
                pageToken=page_token,
                pageSize=100,
            )
            .execute()
        )
        files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break
    return files


def download_file(service, file_id, dest_path):
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    os.makedirs(os.path.dirname(dest_path) or ".", exist_ok=True)
    with open(dest_path, "wb") as f:
        f.write(fh.getvalue())


def ensure_webp_companion(image_path):
    """If a PNG/JPG is downloaded, automatically generate/update its .webp companion."""
    ext = os.path.splitext(image_path)[1].lower()
    if ext in (".png", ".jpg", ".jpeg"):
        webp_path = os.path.splitext(image_path)[0] + ".webp"
        try:
            with Image.open(image_path) as img:
                img.save(webp_path, "WEBP", quality=88, method=6)
                print(f"  -> Generated WebP: {webp_path}")
        except Exception as e:
            print(f"  -> Warning: Could not convert {image_path} to WebP: {e}")


def sync_zip_package(service, state):
    print("Checking 'UofL game' folder for Universe_of_Legends_v5.zip...")
    items = list_folder_files(service, UOFL_GAME_FOLDER_ID)
    zip_candidates = [f for f in items if f["name"] == "Universe_of_Legends_v5.zip"]
    if not zip_candidates:
        print("  No Universe_of_Legends_v5.zip found in main folder.")
        return

    # Pick most recently modified zip if multiple exist
    zip_Candidates_sorted = sorted(zip_candidates, key=lambda x: x.get("modifiedTime", ""), reverse=True)
    latest_zip = zip_Candidates_sorted[0]
    zip_key = f"zip:{latest_zip['id']}"
    sig = f"{latest_zip.get('modifiedTime')}_{latest_zip.get('md5Checksum')}"

    if state["files"].get(zip_key) == sig and os.path.exists("index.html"):
        print("  Universe_of_Legends_v5.zip is already up to date.")
        return

    print(f"  Downloading & extracting updated Universe_of_Legends_v5.zip ({latest_zip.get('modifiedTime')})...")
    tmp_zip = "Universe_of_Legends_v5.zip"
    download_file(service, latest_zip["id"], tmp_zip)
    with zipfile.ZipFile(tmp_zip, "r") as zf:
        zf.extractall(".")
    # Ensure index.html matches UofL_v5.html if UofL_v5.html is newer
    if os.path.exists("UofL_v5.html"):
        with open("UofL_v5.html", "rb") as src, open("index.html", "wb") as dst:
            dst.write(src.read())
    # Remove zip after extracting so repo stays clean and lightweight
    if os.path.exists(tmp_zip):
        os.remove(tmp_zip)
    state["files"][zip_key] = sig
    print("  Extracted Universe_of_Legends_v5.zip into repository root.")


def sync_asset_folder(service, folder_id, local_dir, state):
    print(f"Checking Google Drive folder '{local_dir}' ({folder_id})...")
    os.makedirs(local_dir, exist_ok=True)
    items = list_folder_files(service, folder_id)
    for item in items:
        if item.get("mimeType", "").startswith("application/vnd.google-apps."):
            continue  # Skip Google Docs/Sheets/Folders
        file_id = item["id"]
        name = item["name"]
        sig = f"{item.get('modifiedTime')}_{item.get('md5Checksum')}"
        dest_path = os.path.join(local_dir, name)
        state_key = f"{local_dir}:{name}"

        if state["files"].get(state_key) == sig and os.path.exists(dest_path):
            continue

        print(f"  Downloading updated asset: {dest_path}")
        download_file(service, file_id, dest_path)
        ensure_webp_companion(dest_path)
        state["files"][state_key] = sig


def main():
    service = get_drive_service()
    state = load_sync_state()

    # 1. Sync main zip package first
    sync_zip_package(service, state)

    # 2. Sync individual files in Assets/ and Card_Images/
    sync_asset_folder(service, ASSETS_FOLDER_ID, "Assets", state)
    sync_asset_folder(service, CARD_IMAGES_FOLDER_ID, "Card_Images", state)

    save_sync_state(state)
    print("Google Drive sync complete!")


if __name__ == "__main__":
    main()
