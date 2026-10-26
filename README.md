# Universe of Legends TCG — Digital Origins (v5 Magitek Edition)

**Universe of Legends TCG — Digital Origins** is a self-contained, single-page web application (`index.html` / `UofL_v5.html`) built for deck building, solo and 2-player hotseat playtesting, booster pack simulation, and live cloud card/deck administration for the **Universe of Legends Trading Card Game** (*Fractures in Time* expansion).

Designed around the game's core blend of **Magic**, **Fantasy**, and **Technology** (**"Magitek"**), the application runs directly in any desktop or mobile horizontal browser while dynamically syncing with Google Sheets, Google Apps Script, and local asset folders.

## 1. Core Application Modules & How They Work

The application is structured into four primary interactive views and three administrative modals, all gated by a role-based security terminal on the start screen.

| Module / View | DOM Container ID | Core Functionality |
| :--- | :--- | :--- |
| **Start Screen & Passcode Gate** | `#start-view` | Master Duel-inspired split widescreen layout featuring the **Magitek Security Terminal**, rotating arcane-tech emblem showcase, 5 Barrier Crystal status bar, and role-gated navigation blades. |
| **Deck Builder** | `#builder-view` | Full card catalog browser with multi-criteria filtering, live deck construction across **Barriers (5)**, **Main Deck (40–50)**, and **Re/Action Deck (up to 10)**, JSON import/export, and Google Sheets cloud deck saving/loading. |
| **Playtest Arena (Solo & 2P)** | `#playtest-view` | Interactive tabletop playmat supporting desktop mouse drag-and-drop and mobile touch gestures (`touchstart` / `touchmove` / `touchend` + double-tap to rest/stand), life/barrier tracking, token generation, and a real-time right-hand **Action Log**. |
| **Pack Opening Simulator** | `#pack-opening-view` | 2-row Arena-style booster pack opening experience that pulls 7 random cards from the active card pool, featuring a 3D interactive pack centerpiece (`Assets/Booster_Pack.webp`), click-to-flip card reveals, and a golden rare-slot aura on the 7th card. |
| **Card Database Editor** *(Admin)* | `#card-editor-modal` | Searchable live card inspector and editor that previews card artwork and updates card stats, costs, realms, colors, keywords, and abilities in both the live session and the master Google Sheet. |
| **Backend Configuration** *(Admin)* | `#backend-modal` | Configures the Google Apps Script Web App URL, manages administrator privileges, toggles deck `LOCKED` (`X`) states, and seeds or refreshes cloud decks. |
| **Save Deck Modal** | `#save-deck-modal` | Validates deck legality, checks lock permissions, and writes new or updated deck lists directly to the Saved Decks Google Sheet. |

### Role-Based Access Control (Passcode Gate)

On launch, `#start-view` requires an access code before unlocking navigation (`verifyStartPasscode()`):

| Access Tier | Login Passcode | Session Storage Value | Unlocked Capabilities |
| :--- | :--- | :--- | :--- |
| **Player Mode** | `Legends` | `sessionStorage.uofl_auth_role = "player"` | Unlocks **Enter Deck Builder** and **Pack Opening Simulator**. Hides the **Backend** button (`#nav-backend-btn`), hides the **Card Database Editor** blade (`#start-card-editor-btn`), and prevents overwriting locked (`X`) official decks. |
| **Admin Mode** | `UofLAdmin` | `sessionStorage.uofl_auth_role = "admin"` | Unlocks all Player features plus the **Card Database Editor** on the start menu, the **Backend** button in the Deck Builder header, and full permission to create, edit, or unlock official (`LOCKED = X`) decks. |
| **Backend Override** | `UofLAdmin2026` | `isAdminModeActive = true` | Secondary backend API passcode (`ADMIN_PASSCODE`) sent in POST payloads to authenticate privileged writes in `GoogleAppsScript_SavedDecks.js`. |

## 2. Game Rules & Deck Construction Enforced by the App

The Deck Builder and Playtest Arena enforce the official *Universe of Legends TCG* ruleset:

* **Three Realms**: **Magic** (Arcane Purple `#9d4edd`), **Fantasy** (Runic Gold `#ffd700`), and **Technology** (Electric Cyan `#00e5ff`).
* **Five Barrier Colors**: **Blue** (`#00b4ff`), **Green** (`#00e676`), **Red** (`#ff3d57`), **Yellow** (`#ffd700`), and **Purple** (`#b388ff`), plus **White / Neutral** cards.
* **Deck Structure**:
  * **Barrier Deck**: Exactly **5 Barrier cards** (max 1 copy per unique Barrier card). Your Barrier colors determine the color requirements available for your Universe and Re/Action decks.
  * **Main (Universe) Deck**: **40 to 50 cards** consisting of **Units** (Minions, Legends, Celestials), **Items**, and **Anchors**. Up to **3 copies** of any Minion or Item, and **1 copy** of any Legend, Celestial, or Anchor.
  * **Re/Action Deck**: Up to **10 Action / Re-Action cards** (max 1 copy of each unique card, and at most **1 Alpha** Action or Re-Action per deck).
* **Playtest Zones & Mechanics**:
  * **4 Main Field Zones**: Hold active Units and Anchors. Supports **Stacking** (`MOBILIZE` Minions stacking together, `FAMILIAR` Minions stacking under Legends, and up to 3 `Item` cards equipping under a Legend with sufficient Item Slots).
  * **5 Barrier Slots**: Act as the player's life barriers; attacking and breaking all 5 barriers followed by a direct hit wins the match.
  * **Energy Zone**: Cards placed here pay energy costs; cards with the **SPARK** keyword can activate abilities while in the Energy Zone.
  * **Action / Flow Zone**: Dedicated zone where played Actions and Re-Actions resolve on **The Flow** chain.
  * **Universe Deck, Re/Action Deck, & The Unknown**: Draw pile, reaction reserve, and discard/destroyed zone ("The Unknown").

## 3. Data Architecture & How All External Data Connects

The application uses a **three-tier data architecture** (Live Cloud API → Direct Google Sheet CSV Read → Local Browser Cache & Bundled Fallback) so the game always loads instantly, even offline, while staying synchronized with your live Google Sheets whenever online.

### Overview of Connected Data Sources

| Data Source | Resource Type | Google ID / Local Path | Direction | Purpose |
| :--- | :--- | :--- | :--- | :--- |
| **[Fractures in Time Card List](https://docs.google.com/spreadsheets/d/1yIp6ArxaQ-gGDVdY6EiR1RDuKzx_Np4i422sX0emmr0/edit)** | Google Sheet | `1yIp6ArxaQ-gGDVdY6EiR1RDuKzx_Np4i422sX0emmr0` | Read (CSV) & Write (Apps Script POST) | Master database of all 131+ cards, stats, abilities, keywords, and image filenames. |
| **[Universe of Legends - Saved Decks](https://docs.google.com/spreadsheets/d/1Z7mxql5ZswCbE927ZOIWmEbnadCA4fzIjLPyX3bqXFU/edit)** | Google Sheet | `1Z7mxql5ZswCbE927ZOIWmEbnadCA4fzIjLPyX3bqXFU` | Read (CSV / GET) & Write (Apps Script POST) | Cloud storage for starter decks, tournament decks, and player-saved deck lists. |
| **[Card Numbering Reference](https://docs.google.com/spreadsheets/d/19SVtBwerAAlmib_5NbKMQFxjOic7q3uOen8U2KagxB4/edit)** | Google Sheet | `19SVtBwerAAlmib_5NbKMQFxjOic7q3uOen8U2KagxB4` | Reference / Script Mapping | Maps original raw illustration filenames to standardized card IDs (`Unit_001`, `Barrier_001`, etc.). |
| **Google Apps Script Backend** | Web App API (`GoogleAppsScript_SavedDecks.js`) | Configured in `#backend-modal` (`localStorage.uofl_deck_webapp_url`) | GET & POST JSON API | Handles authenticated writes to both the **Saved Decks** sheet and the **Master Card List** sheet. |
| **Card Artwork Directory** | Static Image Folder | `Card_Images/` (Drive ID: `1krDrBK95s6ZdQpiutz7iSw86mJkvOdNG`) | Local / CDN Read | Stores all card face images in `.webp` (primary) and `.png` (fallback) formats. |
| **UI & Brand Assets Directory** | Static Image Folder | `Assets/` (Drive ID: `1525qTxC8cIxsNOfzkyEO98oKh3FvUTD2`) | Local / CDN Read | Stores `Color_Logo_Tight.webp`, `Booster_Pack.webp`, `Regular_Card_Back.webp`, `Barrier_Card_Back.webp`, `Reaction.webp`, and `logo.png`. |

### Connection 1: Master Card Database (`Fractures in Time Card List`)

1. **Bundled Baseline (`INITIAL_CARDS_DATA`)**:
   * Inside `index.html` / `UofL_v5.html`, the full 131-card *Fractures in Time* dataset is embedded in the `INITIAL_CARDS_DATA` array so the app boots with zero latency.
2. **Live Google Sheet Auto-Sync (`fetchLiveGoogleSheetBackend()`)**:
   * On startup, the app fetches live CSV data from:
     ```text
     https://docs.google.com/spreadsheets/d/1yIp6ArxaQ-gGDVdY6EiR1RDuKzx_Np4i422sX0emmr0/gviz/tq?tqx=out:csv
     ```
   * It parses the sheet columns (`Card Name`, `Card Type`, `Realm/Affinity`, `Card Color`, `Color Requirement`, `Energy Cost`, `Item Slots / Weight`, `ATK`, `DEF`, `Keywords`, `SPARK`, `Card Text & Abilities`, `Flavor Text`, `Illustrator`, `Image File Name`) and merges any live edits directly into the in-memory `catalog` array.
3. **Admin Card Database Editor Write-Back (`saveCardChangesFromEditor()`)**:
   * When an Admin edits a card in the **Card Database Editor** (`#card-editor-modal`), the app:
     1. Updates the live `catalog` object in memory and re-renders the Deck Builder and Card Editor preview immediately.
     2. Saves the updated catalog to `localStorage.getItem('uofl_custom_card_edits')` so edits persist locally across browser refreshes.
     3. Sends a `POST` request with `action: "updateCard"` and `cardSheetId: "1yIp6ArxaQ-gGDVdY6EiR1RDuKzx_Np4i422sX0emmr0"` to your Google Apps Script Web App URL, which locates the matching row by `Card Name` in the master Google Sheet and updates the cells directly.

### Connection 2: Cloud Saved Decks (`Universe of Legends - Saved Decks`)

The Saved Decks Google Sheet (`1Z7mxql5ZswCbE927ZOIWmEbnadCA4fzIjLPyX3bqXFU`) uses a 7-column schema on `Sheet1`:

| Column Header | Description | Example Value |
| :--- | :--- | :--- |
| `Deck Name` | Unique display name of the deck | `Starter Deck - Fractures in Time` |
| `LOCKED` | Lock flag (`X` = locked official deck; blank = player-editable) | `X` |
| `Barriers` | Comma-separated summary of the 5 selected Barrier card names | `Crossroads of Mystery, Crossroads of Wealth, ...` |
| `Main Deck Count` | Integer count of cards in the Main (Universe) Deck | `40` |
| `Re/Action Count` | Integer count of cards in the Re/Action Deck | `10` |
| `Last Updated` | Timestamp of the most recent save (`yyyy-MM-dd HH:mm:ss`) | `2026-10-07 23:11:32` |
| `Deck Data JSON` | Complete serialized deck object (`deckName`, `barriers`, `mainDeck`, `reactionDeck`) | `{"deckName":"Starter Deck...","barriers":[...]}` |

* **How Decks Are Loaded (`refreshSavedDecks()`)**:
  1. If a Google Apps Script Web App URL is saved in `localStorage.uofl_deck_webapp_url`, the app queries `?action=getDecks` first.
  2. If no Web App URL is set (or if the call fails), it reads directly from the public Google Visualization CSV endpoint:
     ```text
     https://docs.google.com/spreadsheets/d/1Z7mxql5ZswCbE927ZOIWmEbnadCA4fzIjLPyX3bqXFU/gviz/tq?tqx=out:csv
     ```
  3. Loaded decks are cached in `localStorage.uofl_saved_decks_cache` and merged with `DEFAULT_SEED_DECKS` so the **Saved Decks** dropdown (`#saved-decks-dropdown`) is always populated.
* **How Decks Are Saved & Protected (`confirmSaveDeckToSheet()`)**:
  * If a deck has `LOCKED = X` in the Google Sheet, non-admin players are blocked from overwriting or deleting it.
  * When saving a new deck or updating an unlocked deck (or when an Admin saves a locked deck), the app sends a `POST` request (`action: "saveDeck"`) to the Google Apps Script Web App, which updates the existing row or appends a new row in `Universe of Legends - Saved Decks`.

### Connection 3: Google Apps Script Backend (`GoogleAppsScript_SavedDecks.js`)

The file `GoogleAppsScript_SavedDecks.js` is the unified serverless backend deployed inside your Google Sheet (**Extensions → Apps Script → Deploy as Web App** with *Execute as: Me* and *Who has access: Anyone*). It supports the following API actions:

| HTTP Method | Action Parameter | Target Google Sheet | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `action=getDecks` *(default)* | `Universe of Legends - Saved Decks` | Returns all saved rows as structured JSON (`deckName`, `isLocked`, `barriers`, `mainCount`, `reactionCount`, `lastUpdated`, `deckDataJson`). |
| `POST` | `action: "saveDeck"` / `"updateDeck"` | `Universe of Legends - Saved Decks` | Creates or updates a deck row; enforces `LOCKED = 'X'` protection unless `isAdmin: true` or `passcode: "UofLAdmin2026"` is provided. |
| `POST` | `action: "deleteDeck"` | `Universe of Legends - Saved Decks` | Deletes a deck row by name (requires Admin privileges if the deck is locked). |
| `POST` | `action: "toggleLock"` | `Universe of Legends - Saved Decks` | Admin-only action to set or clear the `X` flag in the `LOCKED` column. |
| `POST` | `action: "seedDecks"` | `Universe of Legends - Saved Decks` | Seeds initial starter decks if they do not yet exist in the sheet. |
| `POST` | `action: "updateCard"` | `Fractures in Time Card List` (`1yIp6ArxaQ...`) | Admin-only action from the Card Database Editor that updates or appends a card row in the master card spreadsheet. |

### Connection 4: Local Storage & Session Storage Keys

The browser persists user settings, authentication state, and offline caches across reloads using these keys:

| Storage Key | Storage Type | Purpose |
| :--- | :--- | :--- |
| `uofl_auth_role` | `sessionStorage` | Stores the active passcode role (`"player"` or `"admin"`) for the current browser tab session. |
| `uofl_deck_webapp_url` | `localStorage` | Stores the deployed Google Apps Script Web App `/exec` URL entered in the Backend modal. |
| `uofl_saved_decks_cache` | `localStorage` | Offline cache of all decks synced from `Universe of Legends - Saved Decks`. |
| `uofl_custom_card_edits` | `localStorage` | Offline cache of any card attribute edits made via the Admin Card Database Editor. |
| `uofl_Dismissed_Portrait_Banner` | `sessionStorage` | Remembers if a mobile user dismissed the portrait-orientation advisory banner. |

### Connection 5: Static Image & Asset Pipeline (`Assets/` & `Card_Images/`)

All images use a **WebP-first loading strategy with automatic PNG fallback** (`resolveCardImageUrl()` and `handleCardImgError()`) to minimize bandwidth and memory usage on Netlify:

* **UI & Brand Assets (`Assets/`)**:
  * `Assets/Color_Logo_Tight.webp` (fallback `.png`) — Full-color *Universe of Legends* crest displayed on the right showcase of the Start Screen and in the Pack Simulator header.
  * `Assets/Booster_Pack.webp` (fallback `.png`) — Official *Fractures in Time* booster pack artwork used for both the clickable 3D floating pack and the top-row center anchor of the 7-card pack opening reveal.
  * `Assets/Regular_Card_Back.webp` (fallback `.png`) — Main Universe deck card back used on the playmat and on unrevealed booster pack cards.
  * `Assets/Barrier_Card_Back.webp` (fallback `.png`) — Barrier deck and face-down Barrier slot card back.
  * `Assets/Reaction.webp` (fallback `.png`) — Re/Action deck card back.
  * `Assets/logo.png` — Secondary monochrome/emblem logo used on the playmat watermark.
* **Card Face Artwork (`Card_Images/`)**:
  * Each card references its standardized filename in `Card_Images/` by category prefix:
    * `Unit_001.webp` … `Unit_074.webp` (Legends, Minions, Celestials)
    * `Barrier_001.webp` … `Barrier_015.webp` (Barrier cards)
    * `Item_001.webp` … `Item_017.webp` (Item cards)
    * `Re_Action_001.webp` … `Re_Action_042.webp` (Action & Re-Action cards)
    * `Anchor_000.webp` … `Anchor_007.webp` (Anchor cards)
  * If a `.webp` image is missing, `handleCardImgError()` automatically retries `.png`, then checks root-level fallback paths, and finally renders a clean SVG placeholder with the card's name so broken image icons never appear.

## 4. Repository File Structure

```text
universe-of-legends-tcg/
├── index.html                           # Primary production application entry point (served by Netlify)
├── UofL_v5.html                         # Master source copy (identical to index.html)
├── README.md                            # Full application & data architecture documentation
├── DEPLOYMENT_SETUP_GUIDE.md            # Step-by-step Google Drive -> GitHub -> Netlify pipeline guide
├── GoogleAppsScript_SavedDecks.js       # Google Apps Script backend code for Saved Decks & Card Editor
├── fractures_in_time_cards.csv          # Reference CSV export of the Fractures in Time card database
├── optimize_images.py                   # Utility script to batch-convert .png/.jpg images to .webp
├── rename_to_card_numbers.py            # Utility script to standardize raw card image filenames
├── sync_from_drive.py                   # Automated Google Drive -> GitHub sync script
├── netlify.toml                         # Netlify build and cache-control configuration
├── _headers                             # Netlify static asset caching headers
├── .gitignore                           # Excludes temporary archives and local scratch files
├── .github/
│   └── workflows/
│       └── sync-drive-to-github.yml     # GitHub Actions workflow for automated Google Drive sync
├── Assets/                              # UI graphics, logos, booster pack art, and card backs (.webp & .png)
└── Card_Images/                         # Standardized card artwork files (.webp & .png)
```

## 5. Deployment & Maintenance Workflow (GitHub + Netlify)

1. **Repository**: [urbantcgentertainment/universe-of-legends-tcg](https://www.google.com/search?q=https://github.com/urbantcgentertainment/universe-of-legends-tcg) (`main` branch).
2. **Netlify Configuration**:
   * Link your Netlify site to `urbantcgentertainment/universe-of-legends-tcg`.
   * **Branch to deploy**: `main`
   * **Build command**: *(Leave blank or use default from `netlify.toml`)*
   * **Publish directory**: `.`
3. **Adding New Card Images or UI Assets**:
   * Drop new `.png` or `.webp` card images into `Card_Images/` (or UI graphics into `Assets/`).
   * Run `python3 optimize_images.py` locally (or let the GitHub Action run it automatically) to generate `.webp` companions.
   * Commit and push to `main`—Netlify will deploy the updated build automatically.
