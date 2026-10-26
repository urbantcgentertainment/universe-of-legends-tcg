# Seamless Google Drive → GitHub → Netlify Deployment Guide

This guide walks you through connecting your **Google Drive** folders directly to **GitHub** and **Netlify** so that any code update (`Universe_of_Legends_v5.zip`), UI image (`Assets/`), or card image (`Card_Images/`) you drop into Google Drive automatically syncs to GitHub and deploys live to Netlify.

All required automation files are already pre-configured with your exact Google Drive folder IDs and bundled inside `Universe_of_Legends_v5.zip`:

| File | Purpose |
| :--- | :--- |
| `.github/workflows/sync-drive-to-github.yml` | GitHub Actions workflow that pulls changes from Google Drive, converts new PNGs to WebP, and commits to GitHub |
| `sync_from_drive.py` | Python sync engine pre-configured with your `UofL game`, `Assets`, and `Card_Images` Drive folder IDs |
| `netlify.toml` | Netlify build and caching configuration for instant static deployments |
| `.gitignore` | Keeps temporary zip files and system cache files out of your GitHub repository |

## Pre-Configured Google Drive Folder IDs

Your `sync_from_drive.py` script and `.github/workflows/sync-drive-to-github.yml` workflow are already wired to your three core Google Drive folders:

| Folder Name | Google Drive Folder ID | What Gets Synced |
| :--- | :--- | :--- |
| **UofL game** | `1mNcsVt4O5QvL6npRBOEAgoc3jyH2ycm7` | Automatically downloads and extracts `Universe_of_Legends_v5.zip` into the repo root |
| **Assets** | `1525qTxC8cIxsNOfzkyEO98oKh3FvUTD2` | Syncs new/updated UI graphics (`Booster_Pack.png`, `Color Logo.png`, card backs) and generates `.webp` versions |
| **Card_Images** | `1krDrBK95s6ZdQpiutz7iSw86mJkvOdNG` | Syncs new/updated card artwork into `Card_Images/` and generates `.webp` versions |

## Approach 1: 100% Cloud Automation (GitHub Actions + Netlify)

Use this setup if you want changes in Google Drive to deploy to Netlify in the cloud **without needing your computer turned on**.

### Step 1: Create Your GitHub Repository & Upload Initial Files

1. Sign in to [GitHub](https://github.com/) and click **New repository**.
2. Name the repository `universe-of-legends-tcg`, set it to **Private** (or Public), and click **Create repository**.
3. Extract `Universe_of_Legends_v5.zip` into your local project folder (where your `Card_Images/` folder lives) so your folder contains `index.html`, `UofL_v5.html`, `Assets/`, `Card_Images/`, `sync_from_drive.py`, `netlify.toml`, and `.github/workflows/sync-drive-to-github.yml`.
4. Push this folder to your new GitHub repository using [GitHub Desktop](https://desktop.github.com/) or Git CLI:
   ```bash
   git init
   git branch -M main
   git add -A
   git commit -m "Initial commit with Google Drive auto-sync pipeline"
   git remote add origin https://github.com/<YOUR_GITHUB_USERNAME>/universe-of-legends-tcg.git
   git push -u origin main
   ```

### Step 2: Create a Free Read-Only Google Service Account Key

Because your Google Drive folders are private, GitHub Actions uses a read-only Service Account email to download updated files:

1. Open the [Google Cloud Console](https://console.cloud.google.com/) and create a project (e.g., `UofL-Drive-Sync`).
2. Navigate to **APIs & Services → Library**, search for **Google Drive API**, and click **Enable**.
3. Navigate to **IAM & Admin → Service Accounts** and click **+ Create Service Account**.
4. Name it `github-drive-sync`, click **Create and Continue**, and click **Done**.
5. Copy the generated Service Account email address (it looks like `github-drive-sync@uofl-drive-sync.iam.gserviceaccount.com`).
6. Click on your new Service Account → go to the **Keys** tab → click **Add Key → Create new key → JSON** → click **Create**. A `.json` file will download to your computer.
7. Open your [UofL game folder in Google Drive](https://drive.google.com/drive/folders/1mNcsVt4O5QvL6npRBOEAgoc3jyH2ycm7), click **Share**, paste that Service Account email address with **Viewer** access, and click **Share** (sharing the parent `UofL game` folder automatically grants Viewer access to `Assets` and `Universe_of_Legends_v5/Card_Images`).

### Step 3: Add the Key to GitHub Secrets

1. Open your GitHub repository → click **Settings** → **Secrets and variables** → **Actions**.
2. Click **New repository secret**:
   * **Name**: `GDRIVE_SERVICE_ACCOUNT_JSON`
   * **Secret**: Open the downloaded `.json` key file in Notepad, copy the entire JSON text, and paste it here.
3. Click **Add secret**.
4. Still in GitHub **Settings → Actions → General**, scroll down to **Workflow permissions**, select **Read and write permissions**, and click **Save**.

### Step 4: Connect GitHub to Netlify

1. Log in to [Netlify](https://app.netlify.com/), select your existing site (or click **Add new site → Import an existing project**).
2. Go to **Site configuration → Build & deploy → Continuous deployment** and click **Link repository**.
3. Choose **GitHub** and select your `universe-of-legends-tcg` repository:
   * **Branch to deploy**: `main`
   * **Build command**: *(Leave blank or keep default from `netlify.toml`)*
   * **Publish directory**: `.`
4. Click **Deploy site**.

### How Your Cloud Workflow Runs Day-to-Day

* **Automatic Check**: Every 30 minutes (or whenever you click **Run workflow** in the GitHub **Actions** tab), GitHub checks your Google Drive folders (`UofL game`, `Assets`, and `Card_Images`).
* **Automatic Extraction & Optimization**: If a new `Universe_of_Legends_v5.zip` was placed in `UofL game`, GitHub automatically unzips it over your repo. If you uploaded new `.png` images to `Assets` or `Card_Images`, GitHub downloads them and runs `optimize_images.py` to create `.webp` companions.
* **Instant Netlify Deploy**: Whenever GitHub commits those updates to `main`, Netlify detects the commit and publishes your live site within seconds.

## Approach 2: Zero-API-Key Desktop Sync (Google Drive for Desktop + GitHub Desktop)

If you prefer not to set up a Google Cloud Service Account, you can use **Google Drive for Desktop** paired with **GitHub Desktop** on your PC:

1. Install [Google Drive for Desktop](https://www.google.com/drive/download/) and set your `UofL game` folder to **Available offline** (Mirrored).
2. Point [GitHub Desktop](https://desktop.github.com/) to your synced `Universe_of_Legends_v5` folder and publish it to GitHub.
3. Link that GitHub repository to **Netlify** (Step 4 above).
4. Whenever files change in Google Drive, they sync automatically to your PC; one click on **Commit to main → Push origin** in GitHub Desktop deploys the update to Netlify.
