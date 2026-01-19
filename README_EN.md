# Manga Downloader V5 🌐📚

![Manga Downloader Logo](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/scraper/logo.png?raw=true)

**Hello, I’m Romh@ckman!**

**Hook:**  
Easily download your favorite mangas in just a few clicks from Anime Sama and MangaDex, thanks to a simple and open-source application.

**Quick Overview:**  
Manga Downloader V5 is an open-source Python application that centralizes all your needs: automatic chapter downloading, PDF creation, plugin management, and file organization. Compatible with Windows and Linux, it automatically calculates the number of pages per chapter and allows advanced users to add or create plugins to extend available manga sources.

---
[![Python](https://img.shields.io/badge/python-3.10-blue)](https://www.python.org/)  
![Open Source](https://img.shields.io/badge/Open%20Source-Yes-brightgreen?style=flat-square)  
![Windows](https://img.shields.io/badge/Windows-Yes-blue?style=flat-square)  
![Linux](https://img.shields.io/badge/Linux-Yes-blue?style=flat-square)  
![Stars](https://img.shields.io/github/stars/romhackman/Manga)  
![Forks](https://img.shields.io/github/forks/romhackman/Manga)

---

## 🚀 Features

- Download the latest manga chapters from Anime Sama and MangaDex  
- Simple and user-friendly interface  
- Open-source: you can contribute or improve it  
- Works on Windows and Linux via a ready-to-use executable  
- Easily add plugins  
- Automatic Anime Sama domain name updates  
- Automatic project updates  

---

## 💻 Download

Access the GitHub repository to **download the application and the source code**:

[Manga Downloader Installer on GitHub](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Install_Manga_V5_win_linux.py)

---

## ⚠️ Disclaimer

I decline all responsibility regarding the use and content of downloaded files. These programs are intended for strictly personal use. Some content may infringe copyright laws or raise ethical and legal issues. The user is solely responsible for their usage and any legal consequences.

---

# 📑 Table of Contents

* [Launcher](#-launcher)
* [Plugins](#-plugins)
* [Anime-Sama](#-anime-sama)
  * [MangaV3](#-manga)
  * [ShareV2](#-sharev2)
  * [APPV2](#-appv2)
* [Anime-Sama Domain Scraper](#-anime-sama-domain-scraper)
* [MangaDex](#-mangadex)
* [Update](#-update)

---

## Launcher
![Launcher](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/home/logo.png?raw=true)

The **Launcher** is the main interface of the application. It provides quick access to your favorite mangas and all available modules and features.

### Configuration ⚙️
Allows you to define the main folder for your mangas. On first launch, the program asks you to select a folder where all mangas will be downloaded. If canceled, a default folder is created inside the Launcher directory. This information is stored in a JSON file and can be changed at any time.

### Plugins 🧩
This module allows adding additional websites to download mangas beyond Anime-Sama and MangaDex. It is also possible to create extensions without modifying the application’s core code. Full details are available in the manual, Plugins section.

### PDF V2 📜
This module improves manga reading comfort by allowing page-by-page scrolling through images.

### Anime-Sama 🐾
Anime-Sama allows downloading scans from this website, which is normally not possible. Additional features are available to simplify scan downloads.

### MangaDex 🐈
MangaDex allows easy downloading of scans from MangaDex. This module is slightly more complex than Anime-Sama and contains fewer available scans.

### Refresh 🔄
Refreshes your manga list. This action is also automatically performed when the Launcher starts.

---

## 🧩 Plugins
![plugins](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/plugins/logo.png?raw=true)

This program is a **plugin manager** that allows users to download, install, and launch plugins directly from GitHub without manual file handling.

### How it Works
- **Plugin display:** Reads `plugins/instance_plugins.json` to list installed plugins  
- **Plugin download:**  
  1. Downloads the plugin from GitHub  
  2. Extracts it into `plugins/plugin_name/`  
  3. Runs `install.sh` or `install.bat` if present  
  4. Updates `instance_plugins.json`  
- **Launching:** Double-clicking a plugin runs its main file using the `.venv` Python environment  
- **Persistence:** Installed plugins remain available after restart

### Features
- View installed plugins  
- Launch plugins with one click  
- Automatically add plugins from GitHub  

---

## 🐾 Anime-Sama

![anime sama](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/anime%20sama/logo.png)

The **Anime-Sama module** is designed to download scans from the Anime-Sama website.

### Main Applications
- **MangaV3** – Manual scan downloader  
- **ShareV2** – Page count finder  
- **APPV2** – Fast automatic downloader  

---

### 🪢 MangaV3

MangaV3 allows *manual* scan downloading using a template link and page count per chapter.

#### Features
- Manga title input  
- Scan URL template input (`CHAP`, `NUM`)  
- Folder selection  
- Download progress bar  
- Error handling and validation  

---

### 🔍 ShareV2

ShareV2 finds the **number of pages per chapter** to facilitate MangaV3 downloads.

#### How It Works
- Reads the Anime-Sama domain from `domaine.json`
- Formats manga titles into valid URLs
- Accepts multiple chapters
- Uses **binary search** with HTTP HEAD requests
- Supports parallel processing
- Saves results in a temporary folder

---

### 🔽 APPV2

APPV2 is the most convenient application in the project.

#### Finder Tab
- Enter exact manga title
- Add chapters
- Find page counts
- Store data in `_Temp`

#### Downloader Tab
- Automatically filled title and URLs
- Select output folder
- Download scans with progress tracking

---

## 📡 Anime-Sama Domain Scraper

This Python scraper automatically detects the **active Anime-Sama domain** and stores it in a JSON file.

### How It Works
1. Visits anime-sama.pw  
2. Parses HTML using BeautifulSoup  
3. Finds the “Access Anime-Sama” button  
4. Extracts the active domain  
5. Saves it to `domaine.json`

### Benefits
- Automatic domain detection  
- No manual URL updates  
- Simple JSON format  
- Easy integration  

---

## 🐈 MangaDex

MangaDex allows downloading mangas using the official API.

### Features
- Language selection (FR / EN)
- Manga search
- Chapter selection
- Download with progress bar
- Optional CBZ compression
- Integrated PDFV2

### Workflow
1. Search manga  
2. Retrieve chapters via API  
3. Select chapters  
4. Download images  
5. Package chapters (optional CBZ)  

![mangadex](https://github.com/romhackman/Manga_Downloader_installer/blob/main/Bank_Image/mangadex/image.png?raw=true)
