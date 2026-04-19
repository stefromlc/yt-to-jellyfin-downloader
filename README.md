📥 YouTube → Media Library Downloader

A Python tool that downloads YouTube videos (channels, playlists, or single videos) and automatically converts them into a TV-style media library—complete with metadata and artwork for use in Jellyfin or Kodi.

✨ Features
📺 Download:
Full channels (latest uploads)
Playlists (with optional limits)
Single videos

⚙️ Powered by yt-dlp

🗂️ Automatically organizes content into:
Channel folders
Season/Episode structure

📝 Generates .nfo metadata files (Jellyfin/Kodi compatible)
🖼️ Downloads thumbnails as poster + fanart
🚫 Skips already downloaded videos (archive tracking)
🧵 Background worker queue for staged downloads
📁 Example Output
Media/
└── ChannelName/
    ├── tvshow.nfo
    └── Season 01/
        ├── Video Title 1.mp4
        ├── Video Title 1.nfo
        ├── Video Title 1-poster.jpg
        ├── Video Title 1-fanart.jpg
        └── ...
        
🚀 Quick Start
1. Install dependency
pip install yt-dlp

2. Configure the script
Update these values:
BASE_DIR = r"YOUR_MEDIA_FOLDER"
COOKIE_FILE = r"PATH_TO_YOUR_COOKIES.txt"
SEASON_NAME = "Season 01"

3. Run it
python your_script.py

🧠 How It Works
Paste a YouTube URL (video, playlist, or channel)
Stage multiple downloads
Run go

The script:
Downloads videos using yt-dlp
Extracts metadata
Renames and moves files into a TV-style structure
Generates .nfo files + artwork
Cleans up temp folders automatically

💡 Commands
go → start downloads
clear → clear staged jobs
q → quit

🔧 Configuration Notes
BASE_DIR → where your media library lives
COOKIE_FILE → optional but recommended for restricted/private videos
SEASON_NAME → change if you want different season naming

🧩 Customisation Ideas
Add multiple download threads
Change naming conventions
Split content into multiple seasons
Add a GUI or web interface
Replace hardcoded config with a config file

⚠️ Limitations
Single-season structure by default
Episode numbering is sequential
CLI only (no GUI yet)

📌 Use Cases
Build a personal YouTube-on-Plex library
Archive favourite creators
Offline viewing
Organise long-form content like TV shows

🔐 Generating a cookies.txt File (Optional)
Some videos (age-restricted, private, or members-only) require authentication. You can provide your YouTube cookies to yt-dlp to enable this.

🧩 Steps
Install the Get cookies.txt LOCALLY extension:
Available for Chrome and Firefox
Open a private/incognito window
Sign in to your YouTube account

In the same tab, go to:
https://www.youtube.com/robots.txt

Click the extension icon:
Set Export Format → Netscape

Click Export As
Save the file somewhere safe, e.g.:
C:\path\to\cookies.txt
Update your script:
COOKIE_FILE = r"C:\path\to\cookies.txt"

⚖️ Disclaimer
For personal use only. Please respect YouTube’s terms of service and content creators.
