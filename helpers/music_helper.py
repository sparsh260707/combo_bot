# helpers/music_helper.py
import os
import yt_dlp
from pyrogram import Client
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH"))
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# ----------------- Pyrogram Client -----------------
if SESSION_STRING:
    app = Client("music_assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)
else:
    app = Client("music_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# ----------------- Only Download Function -----------------
def download_audio(url: str, output_path: str = "downloads/"):
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    opts = {
        "format": "bestaudio/best",
        "outtmpl": os.path.join(output_path, "%(title)s.%(ext)s"),
        "quiet": True,
        "noplaylist": True
    }
    with yt_dlp.YoutubeDL(opts) as ydl:
        info = ydl.extract_info(url, download=True)
        file_path = ydl.prepare_filename(info)
    return file_path

# Dummy function so import error na aaye
def play_music(*args, **kwargs):
    return "Music system disabled"
