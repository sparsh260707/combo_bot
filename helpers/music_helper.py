import os
import yt_dlp
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# ----------------- Pyrogram Client -----------------
if SESSION_STRING:
    app = Client(
        name="music_userbot",
        session_string=SESSION_STRING,
        api_id=API_ID,
        api_hash=API_HASH
    )
else:
    app = Client(
        name="music_bot",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH
    )

# ----------------- PyTgCalls -----------------
pytgcalls = PyTgCalls(app)

# ----------------- Download -----------------
def download_audio(url: str):
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": "downloads/%(title)s.%(ext)s"
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# ----------------- Play -----------------
async def play_music(chat_id: int, file_path: str):
    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path)
    )
