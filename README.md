# 📥 YouTube → Media Library Downloader

A Python tool that downloads YouTube videos (channels, playlists, or single videos) and automatically converts them into a clean, TV-style media library—complete with metadata and artwork for use in **Jellyfin** or **Kodi**.

---

## 🗂️ Recommended Media Folder Layout

To keep your media library clean and avoid mixing YouTube content with movies and TV shows, use a structured folder setup like this:

```
M:\Media
│
├── Movies
├── TV
└── YouTube
    ├── ChannelName
    │   └── Season 01
    │       ├── Video Title 1.mp4
    │       ├── Video Title 1.nfo
    │       ├── Video Title 1-poster.jpg
    │       ├── Video Title 1-fanart.jpg
    │       └── ...
    ├── AnotherChannel
    └── Playlists
```

This ensures:

* YouTube content is isolated from films/TV
* Easy scanning by Jellyfin/Kodi
* Cleaner metadata management

---

## ✨ Features

📺 **Download options**

* Full channels (latest uploads)
* Playlists (with optional limits)
* Single videos

⚙️ **Powered by** `yt-dlp`

🗂️ **Automatic TV-style organisation**

* Channel folders
* Season/Episode structure

📝 **Metadata support**

* Generates `.nfo` files (Jellyfin/Kodi compatible)

🖼️ **Artwork handling**

* Downloads thumbnails as poster + fanart

🚫 **Smart skipping**

* Avoids re-downloading existing videos (archive tracking)

🧵 **Staged queue system**

* Queue multiple downloads before running

---

## 📁 Example Output Structure

```
YouTube/
└── ChannelName/
    ├── tvshow.nfo
    └── Season 01/
        ├── Video Title 1.mp4
        ├── Video Title 1.nfo
        ├── Video Title 1-poster.jpg
        ├── Video Title 1-fanart.jpg
        └── ...
```

---

## 🚀 Quick Start

### 1. Install dependency

```
pip install yt-dlp
```

---

### 2. Configure the script

Update these values in your script:

```
BASE_DIR = r"M:\Media\YouTube"
COOKIE_FILE = r"PATH_TO_YOUR_COOKIES.txt"
SEASON_NAME = "Season 01"
```

---

### 3. Run it

```
python your_script.py
```

---

## 🧠 How It Works

1. Paste a YouTube URL (video, playlist, or channel)
2. Stage multiple downloads
3. Run `go`

The script then:

* Downloads videos using `yt-dlp`
* Extracts metadata
* Renames & organises files into TV-style structure
* Generates `.nfo` files + artwork
* Cleans up temporary files automatically

---

## 💡 Commands

```
go      → start downloads
clear   → clear staged jobs
q       → quit
```

---

## 🔧 Configuration Notes

* `BASE_DIR` → Root of your media library (recommended: `M:\Media\YouTube`)
* `COOKIE_FILE` → Optional but recommended for restricted/private videos
* `SEASON_NAME` → Change if you want different season naming

---

## 🧩 Customisation Ideas

* Add multi-threaded downloads
* Change naming conventions
* Split content into multiple seasons per channel
* Add GUI or web interface
* Replace hardcoded config with JSON/YAML config file

---

## ⚠️ Limitations

* Single-season structure by default
* Episode numbering is sequential
* CLI-only (no GUI yet)

---

## 📌 Use Cases

* Build a personal YouTube-on-Jellyfin/Plex library
* Archive favourite creators
* Offline viewing
* Organise long-form YouTube content like TV shows

---

## 🔐 Optional: cookies.txt Setup

For age-restricted, private, or members-only content:

### Steps

1. Install browser extension:

   * “Get cookies.txt (LOCALLY)” for Chrome/Firefox

2. Open an incognito/private window

3. Sign in to YouTube

4. Visit:

```
https://www.youtube.com/robots.txt
```

5. Click extension → Export as **Netscape format**

6. Save file:

```
C:\path\to\cookies.txt
```

7. Update script:

```
COOKIE_FILE = r"C:\path\to\cookies.txt"
```

---

## ⚖️ Disclaimer

This tool is intended for **personal use only**. Please respect YouTube’s Terms of Service and content creators’ rights.
