
# Manga Downloader V5.3 🌐📚

![Logo Manga Downloader](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png?raw=true)

**Hello, I’m Romh@ckman!**

**Tagline:**
Easily download your favorite manga in just a few clicks from Anime Sama and MangaDex using a simple, open-source application.

**Quick Overview:**
Manga Downloader V5 is an open-source Python application that centralizes all your manga needs: automatic chapter downloads, PDF creation, plugin management, and file organization. Compatible with Windows and Linux, it automatically calculates the number of pages per chapter and allows advanced users to add or create plugins to extend the available manga sources.

---

[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen?style=flat-square)
![Windows](https://img.shields.io/badge/Windows-Yes-blue?style=flat-square)
![Linux](https://img.shields.io/badge/Linux-Yes-blue?style=flat-square)
![Stars](https://img.shields.io/github/stars/romhackman/Manga)
![Forks](https://img.shields.io/github/forks/romhackman/Manga)

---

## 🚀 Features

* Download the latest manga chapters from Anime Sama and MangaDex
* Simple and user-friendly interface
* Open-source: you can contribute or improve it
* Works on Windows and Linux via a ready-to-use executable
* Easily add plugins
* Automatic Anime Sama domain updates
* Automatic project updates

---

## 💻 Download

Access the GitHub repository to **download the application and source code**:

[Manga Downloader Installer on GitHub](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Install_Manga_V5_win_linux.py)

---

## ⚠️ Legal Disclaimer

This project is provided **for educational and technical purposes only**, to experiment and learn coding.

**Important Notes:**

* The user is **fully responsible** for the use of this software and any files downloaded.
* **No copyright-protected files are included** with this program. Any copyrighted content downloaded through the software is the **sole responsibility of the user**.
* The software is provided “as-is,” without any warranty. The author **disclaims all liability** for damages, data loss, or legal issues arising from its use.
* These programs are intended for **personal use only**.

**Summary:** Use this software **at your own risk**.

---

## 📜 License

This project is under the **[MIT License](LICENSE)**.

---

# 📑 Table of Contents

* [Launcher](#-launcher)
* [Plugins](#-plugins)
* [Anime-Sama](#-anime-sama)

  * [MangaV3](#-manga)
  * [ShareV2](#-sharev2)
  * [APPV2](#-appv2)
* [Anime-Sama Scraper](#-anime-sama-domain-scraper)
* [MangaDex](#-mangadex)
* [Update](#-update)

---

## Launcher

![Launcher](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/home/logo.png?raw=true)

The **Launcher** is the main interface of the application. It provides quick access to your favorite manga as well as all modules and features.

### Settings ⚙️

This module allows you to define the **main folder** for your manga.

* On the first launch, the program asks you to select a folder where all downloaded manga will be stored.
* If canceled, a default folder is created inside the Launcher folder.
* Folder information is stored in a JSON file.
* You can change the destination folder anytime by clicking this button again.

### Plugins 🧩

This module allows you to **add extra sites** for downloading manga beyond Anime-Sama and MangaDex.

* You can also create extensions without modifying the main application code.
* Full instructions, from downloading to plugin creation, are detailed in the [manual, Plugins section](#-plugins).

### PDF V2 📜

This module improves manga reading:

* Scroll through manga page by page for optimal reading comfort.

### Anime-Sama 🐾

This module allows downloading scans from **Anime-Sama**, with additional features to manage downloads.

* All details are available in the [manual, Anime-Sama section](#-anime-sama).

### MangaDex 🐈

This module allows downloading scans from **MangaDex**.

* Slightly more complex than Anime-Sama, but provides direct access to the scans available on the site.
* Full details are in the [manual, MangaDex section](#-mangadex).

### Refresh 🔄

This button **refreshes your manga list**.

* This action is also performed automatically every time the Launcher opens.

---

## 🧩 Plugins

![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/logo.png?raw=true)
[Somaine 📑](#-sommaire)

The **Plugins module** is a **plugin manager**. It allows you to **download, install, and run plugins from GitHub easily**, without manually handling files or commands.

### How It Works

* **Display installed plugins:** Reads `plugins/instance_plugins.json` to show all installed plugins.

* **Download a plugin:** When a user enters a GitHub link and clicks **Download**:

  1. Downloads the plugin from the GitHub repository.
  2. Extracts files to `plugins/plugin_name/`.
  3. Runs the installation script (`install.sh` or `install.bat`) if present.
  4. Updates `plugins/instance_plugins.json` to remember the plugin path.

* **Run a plugin:** Double-clicking a plugin in the list automatically runs the main plugin file (`plugin_name.py`) using the virtual environment `.venv`.

* **Path memory:** All installed plugins are stored in the `plugins` folder, and their paths are saved in `plugins/instance_plugins.json` so they remain accessible after closing the program.

### Key Features

* Display all installed plugins
* Run a plugin with one click
* Automatically add new plugins from GitHub

### Usage

**View Plugins**

* Installed plugins appear in the **Plugins:** list on the left.
* Click **Refresh** to update the list if necessary.

**Run a Plugin**

* Double-click the plugin to execute it.

**Add a Plugin from GitHub**

1. Copy the plugin GitHub repository link.

   * Example of a valid link:

     ```text
     https://github.com/username/plugin_name
     ```

   * The repository must contain:

     * A main file `plugin_name.py`
     * Optional installation script (`install.sh` or `install.bat`)

2. Paste the link into the field below the plugin list.

3. Click **Download**.

4. Wait for installation to finish, then click **Refresh** if needed.

**Plugin Storage**

* All plugins are in the program's **plugins** folder.
* The program automatically remembers the paths in **plugins/instance_plugins.json**, so they stay accessible after closing.

**Quick Summary**

* **Double-click** → run plugin
* **Enter link + Download** → add plugin
* **Refresh** → update the list

**💡 Legal Note:**
The user is **fully responsible** for installed plugins and their content. The program does not check plugin files and **disclaims all liability** for illegal or problematic content.

![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/image.png?raw=true)

---

## 🐾 Anime-Sama

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/logo.png)
[Somaine 📑](#-sommaire)

The **Anime-Sama module** allows **downloading scans** from the Anime-Sama site and includes multiple integrated tools for easier manga management and downloading.

---

### General Interface 🪟

The interface consists of several buttons and sections:

#### Main Buttons 🟢

* **MangaV3:** Download scans **manually**.
* **PDV2:** Create **PDFs** from images.
* **ShareV2:** Check the **number of pages** for one or multiple chapters.
* **APPV2:** Main app to **quickly download scans**.

#### Refresh Button 🔄

* Updates the list of available scans and chapters.
* Works like the Launcher refresh button.

---

### 🪢 MangaV3

**MangaV3** is the basic tool to download scans manually using a **template link**.

**Interface 🪟**

* Field to **enter the manga title**, used as the download folder name.
* Field to **enter the scan link**.
* **Choose main folder** button to set the download location.
* Progress bar to track downloads.
* **Download** button to start the operation.

**How It Works ⚙️**

1. **Select main folder:** Creates a subfolder per manga.

2. **Automatic page download:** Each chapter has its own subfolder; pages are retrieved from the template link (`CHAP` → chapter number, `NUM` → page number).

3. **Input info:**

   * Manga title → folder name
   * Template link → automatically generates page URLs

4. **Select chapters to download:** Range or specific number of chapters from a chosen start point.

5. **Number of pages per chapter:** User must enter the exact page count per chapter.

6. **Error handling:** Notifications for missing pages or invalid input.

7. **Completion:** Download finished notification and progress bar reset.

---

### 🔍 ShareV2

**ShareV2** determines the **number of pages per chapter**, useful for MangaV3 and APPV2.

**Interface 🪟**

* Field to **enter scan name**.
* Area to input chapters to process.
* List displaying added chapters.
* Buttons to start page count search and delete temporary files.

**How It Works ⚙️**

1. Reads the current Anime-Sama domain from a JSON file (`domaine.json`).
2. Generates the scan link (normalizes accents and spaces).
3. Handles chapters entered by the user.
4. Searches for the number of pages per chapter using **binary search** for efficiency.
5. Executes in parallel for multiple chapters using `ThreadPoolExecutor`.
6. Temporarily saves results in per-chapter files, deletable by the user.

---

### 🔽 APPV2

**APPV2** is the main tool, combining **Finder** and **Downloader**.

#### Tab 1: Finder 🔍

* Prepares info for downloading.
* Enter the exact manga title and chapters to download.
* Searches the number of pages per chapter using binary optimization.
* Creates a temporary `_Temp` folder to store info.

#### Tab 2: Downloader ⬇

* Uses Finder data to automatically download scans.
* Displays title, template link, chapter list, and page count.
* Select destination folder, automatically creates subfolders per chapter.
* Downloads pages with a progress bar.
* Notifies when download is complete.

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/image.png)

---

💡 **Legal Note:**
The user is **fully responsible** for content downloaded from Anime-Sama. The software does not verify copyright compliance and **disclaims all liability** for illegal use or copyright violations.

---

## 📡 Anime-Sama Domain Scraper

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png)

[Somaine 📑](#-sommaire)

The **Anime-Sama Domain Scraper** is a **Python script** that automatically detects the **active Anime-Sama domain** and saves it in a JSON file.

Since Anime-Sama frequently changes domains, links quickly become outdated in connected apps. This script automates the process so other modules (MangaV3, ShareV2, APPV2) always use a valid URL.

---

### How It Works ⚙️

1. Connects to the official site **anime-sama.pw**
2. Parses HTML with **BeautifulSoup**
3. Finds the **"Access Anime-Sama"** button
4. Retrieves the currently active URL
5. Extracts the **domain extension** (`.fr`, `.si`, `.com`, etc.)
6. Saves the info in `domaine.json`

---

### File Structure 📁

Automatically creates the following folder if needed:

```
ND_anime_sama/
└── domaine.json
```

**Example `domaine.json`:**

```json
{
    "domaine": "si"
}
```

This file can be used by other scripts to dynamically construct the valid Anime-Sama URL.

---

### Advantages ✅

* 🔄 Automatic detection of active domain
* 🛠️ No need to change code after domain updates
* 📦 Simple JSON format for other scripts
* 🚀 Easy integration into other Python projects

---

### History 🆕

Since **V4**, domain change management is **fully automated**.

---

💡 **Legal Note:**
The user is **fully responsible** for using the scraper and any content accessed via the Anime-Sama domain. This script is provided **for educational and technical purposes only**, and **the author disclaims all liability** for copyright violations or illegal use.

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/image.png)

---


# 🐈 MangaDex

[Somaine 📑](#-sommaire)

**MangaDex** is a module that allows downloading manga from the MangaDex website. The application uses the **official API** to retrieve chapters and pages.

> Note: MangaDex usually has fewer scans than Anime-Sama.

---

## Interface 🪟

* Button to access **PDFV2** for generating PDFs from downloaded chapters.
* Language selector: **FR** or **EN**.
* Field to enter the **manga title** to search.
* Area to choose **chapters to download**.
* Button to **start downloading** with a visual progress tracker.

---

## How It Works ⚙️

The MangaDex module is structured in several components:

### 1️⃣ `api.py` – MangaDex Communication

* **`search(title)`** – searches for a manga by title (max 5 results).
* **`chapters(manga_id, lang)`** – lists available chapters for a manga in the selected language.
* **`pages(chapter_id)`** – retrieves all page URLs of a chapter.

### 2️⃣ `downloader.py` – Downloading

* **`download_chapter(data, out_folder, chapter_num, cbz=True)`** – downloads all pages of a chapter into a local folder.
* Each chapter is saved in a folder `Chapter_<num>` and each page is named `Page_<num>.jpg`.
* **CBZ option:** automatically compresses the chapter into a `.cbz` file for easier reading.

### 3️⃣ `main.py` – Graphical Interface (Tkinter)

* Allows selecting the language, searching a manga, and choosing chapters.
* Displays a progress bar to track download status.
* Integrates **PDFV2** to generate PDFs from downloaded chapters.

### 4️⃣ `mangadex.py` – Command-Line Interface (CLI)

* MangaDex can also be used from the terminal:

  * `search <title>` – search for a manga.
  * `chapters <manga_id>` – list available chapters.
  * `download <chapter_id> [-o folder] [--cbz]` – download a chapter to the selected folder, with optional CBZ creation.

### 5️⃣ Full Process

1. User searches or selects a manga.
2. Application fetches chapters via the API.
3. User selects which chapters to download.
4. Program downloads each page and creates a folder/CBZ for each chapter.
5. Progress bar updates in real time.
6. Notification confirms successful download.

---

![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/image.png?raw=true)

💡 **Legal Notice:**
Downloading content from MangaDex must comply with copyright law. The **user is solely responsible** for the files they download. This module is provided **for educational and technical purposes only**, and **the author disclaims any liability** for illegal use.

