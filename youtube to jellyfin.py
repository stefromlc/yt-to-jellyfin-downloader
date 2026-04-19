import os
import sys
import subprocess
import urllib.request
import json
import re
import time
import threading
import queue
from dataclasses import dataclass
from datetime import timedelta, datetime
os.environ["PYTHONUTF8"] = "1"

# ================== CONFIG ==================

BASE_DIR = r"M:\Media\YouTube"
COOKIE_FILE = r"C:\Users\Documents\cookies.txt"
SEASON_NAME = "Season 01"

# ================== JOB MODEL ==================

@dataclass
class DownloadJob:
    url: str
    max_downloads: str | None = None

download_queue = queue.Queue()
staged_jobs: list[DownloadJob] = []
stop_event = threading.Event()

# ================== SUMMARY STATS ==================

stats = {
    "downloaded": 0,
    "skipped": 0,
    "errors": 0,
    "start_time": None,
}

# ================== URL DETECTION ==================

def is_video_url(url: str) -> bool:
    return "watch?v=" in url or "youtu.be/" in url

def is_playlist_url(url: str) -> bool:
    return "list=" in url

def normalize_input_url(text: str) -> str:
    text = text.strip()
    if text.startswith("@"):
        return f"https://www.youtube.com/{text}"
    return text

# ================== NAME EXTRACTION ==================

def extract_channel_from_url(url: str) -> str:
    m = re.search(r"/(@[^/]+)", url)
    if m:
        return m.group(1)
    m = re.search(r"/channel/([^/]+)", url)
    if m:
        return m.group(1)
    return "UnknownChannel"

def get_channel_from_video(url: str) -> str:
    cmd = [
        sys.executable, "-m", "yt_dlp",

        "--cookies", COOKIE_FILE,
        
        "--skip-download",
        "--print-json",
        url
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not r.stdout:
        return "UnknownChannel"
    info = json.loads(r.stdout.splitlines()[0])
    return info.get("uploader_id", "UnknownChannel")

def get_playlist_title(url: str) -> str:
    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--cookies", COOKIE_FILE,
        "--skip-download",
        "--print-json",
        url
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    info = json.loads(r.stdout.splitlines()[0])
    title = info.get("playlist_title") or info.get("title") or "UnknownPlaylist"
    return re.sub(r'[\\/:*?"<>|]', "_", title).strip()

def get_playlist_id(url: str) -> str:
    m = re.search(r"[?&]list=([^&]+)", url)
    return m.group(1) if m else "UnknownPlaylistID"

# ================== SEASON HELPERS ==================

def ensure_season_folder(channel_dir: str) -> str:
    path = os.path.join(channel_dir, SEASON_NAME)
    os.makedirs(path, exist_ok=True)
    return path

def get_next_episode_number(season_folder: str) -> int:
    highest = 0
    for f in os.listdir(season_folder):
        nfo = f.lower().endswith(".nfo")
        if not nfo:
            continue
        try:
            with open(os.path.join(season_folder, f), encoding="utf-8") as nf:
                txt = nf.read()
                m = re.search(r"<episode>(\d+)</episode>", txt)
                if m:
                    highest = max(highest, int(m.group(1)))
        except:
            pass
    return highest + 1

def get_display_order(info) -> int:
    if info.get("upload_date"):
        return -int(info["upload_date"])  # newest first
    return -99999999

# ================== ARTWORK ==================

def download_episode_art(video_id: str, folder: str, base: str):
    urls = [
        f"https://i.ytimg.com/vi/{video_id}/maxresdefault.jpg",
        f"https://i.ytimg.com/vi/{video_id}/hq720.jpg",
        f"https://i.ytimg.com/vi/{video_id}/hqdefault.jpg",
    ]
    for u in urls:
        try:
            urllib.request.urlretrieve(u, os.path.join(folder, base + "-fanart.jpg"))
            urllib.request.urlretrieve(u, os.path.join(folder, base + "-poster.jpg"))
            return
        except:
            pass

# ================== METADATA ==================

def write_episode_nfo(folder, base, title, desc, ep, aired, url, display_order):
    with open(os.path.join(folder, base + ".nfo"), "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<episodedetails>
  <title>{title}</title>
  <season>1</season>
  <episode>{ep}</episode>
  <aired>{aired}</aired>
  <plot>{desc}</plot>
  <studio>YouTube</studio>
  <uniqueid type="youtube">{url}</uniqueid>
</episodedetails>
""")

def write_tvshow_nfo(folder, name, url):
    path = os.path.join(folder, "tvshow.nfo")
    if os.path.exists(path):
        return
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"""<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<tvshow>
  <title>{name}</title>
  <studio>YouTube</studio>
  <genre>YouTube</genre>
  <plot>YouTube channel: {name}</plot>
  <uniqueid type="youtube">{url}</uniqueid>
</tvshow>
""")

# ================== POST PROCESS ==================

def process_downloaded_folders(channel_dir: str):
    season = ensure_season_folder(channel_dir)

    for name in os.listdir(channel_dir):
        src = os.path.join(channel_dir, name)
        if not os.path.isdir(src) or src.endswith(SEASON_NAME):
            continue

        info_files = [f for f in os.listdir(src) if f.endswith(".info.json")]
        mp4s = [f for f in os.listdir(src) if f.lower().endswith(".mp4")]
        if not info_files or not mp4s:
            continue

        try:
            with open(os.path.join(src, info_files[0]), encoding="utf-8") as f:
                info = json.load(f)
        except Exception as e:
            print(f"⚠️ Skipping folder (metadata error): {src}")
            stats["errors"] += 1
            continue


        raw_title = info.get("title", "Unknown Title")
        safe_title = re.sub(r'[\\/:*?"<>|]', "", raw_title)

        ep_num = get_next_episode_number(season)
        base = safe_title

        os.rename(os.path.join(src, mp4s[0]), os.path.join(season, base + ".mp4"))

        if info.get("id"):
            download_episode_art(info["id"], season, base)

        aired = "1970-01-01"
        if info.get("upload_date"):
            aired = datetime.strptime(info["upload_date"], "%Y%m%d").date().isoformat()

        write_episode_nfo(
            season,
            base,
            raw_title,
            info.get("description", ""),
            ep_num,
            aired,
            info.get("webpage_url", ""),
            get_display_order(info)
        )

        for f in os.listdir(src):
            os.remove(os.path.join(src, f))
        os.rmdir(src)

        stats["downloaded"] += 1

    write_tvshow_nfo(
        channel_dir,
        os.path.basename(channel_dir),
        f"https://www.youtube.com/{os.path.basename(channel_dir)}"
    )

# ================== DOWNLOAD ==================

def run_yt_dlp(url: str, max_downloads: str | None = None):
    if is_playlist_url(url):
        base_dir = os.path.join(
            BASE_DIR,
            "_Playlists",
            f"{get_playlist_id(url)} - {get_playlist_title(url)}"
        )
    elif is_video_url(url):
        base_dir = os.path.join(BASE_DIR, get_channel_from_video(url))
    else:
        base_dir = os.path.join(BASE_DIR, extract_channel_from_url(url))

    os.makedirs(base_dir, exist_ok=True)
    archive = os.path.join(base_dir, "downloaded.txt")

    cmd = [
        sys.executable, "-m", "yt_dlp",
        "--add-header", "Referer:https://www.youtube.com/",
        "--add-header", "User-Agent:Mozilla/5.0",

        "--cookies", COOKIE_FILE,
        "--progress",
        "--no-color",
        "--no-warnings",

        
        "--match-filter", "!is_live",

        "--download-archive", archive,
        "--write-info-json",
        "--merge-output-format", "mp4",
        "-f", "best[protocol=m3u8_native]/best",


        "-o", os.path.join(base_dir, "%(title)s", "%(title)s.%(ext)s"),
    ]


    if max_downloads:
        cmd += ["--max-downloads", max_downloads]

    cmd.append(url)
    subprocess.run(cmd)
    time.sleep(2)
    process_downloaded_folders(base_dir)

# ================== WORKER ==================

def download_worker():
    while not stop_event.is_set():
        try:
            job = download_queue.get(timeout=0.5)
        except queue.Empty:
            continue
        run_yt_dlp(job.url, job.max_downloads)
        download_queue.task_done()

# ================== MAIN ==================

def main():
    print("📥 YouTube Downloader (Original Titles + Newest First)")
    print("Commands: go | clear | q\n")

    threading.Thread(target=download_worker, daemon=True).start()

    while True:
        raw = input("Enter URL: ").strip()

        if raw.lower() in {"q", "quit", "exit"}:
            stop_event.set()
            download_queue.join()
            break

        if raw.lower() == "go":
            stats["start_time"] = time.time()
            for job in staged_jobs:
                download_queue.put(job)
            staged_jobs.clear()
            download_queue.join()
            break

        if raw.lower() == "clear":
            staged_jobs.clear()
            print("🧹 Cleared\n")
            continue

        url = normalize_input_url(raw)

        if is_playlist_url(url):
            limit = input("How many videos from this playlist? ").strip()
            staged_jobs.append(DownloadJob(url, limit or None))
            print("➕ Playlist staged\n")
            continue

        if is_video_url(url):
            staged_jobs.append(DownloadJob(url))
            print("➕ Video staged\n")
            continue

        limit = input("How many latest videos? ").strip()
        staged_jobs.append(DownloadJob(url + "/videos", limit or None))
        print("➕ Channel staged\n")

if __name__ == "__main__":
    main()


#python yt_020126.py
