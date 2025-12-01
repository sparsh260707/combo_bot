# helpers/music_helper.py
import os
import yt_dlp
from dotenv import load_dotenv
from pyrogram import Client
from pytgcalls import PyTgCalls
from pytgcalls.types import AudioPiped
from pytgcalls.types.stream import Stream

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
SESSION_STRING = os.getenv("SESSION_STRING", "")

# ----------------- Pyrogram Client -----------------
if SESSION_STRING:
    app = Client(
        "music_assistant",
        api_id=API_ID,
        api_hash=API_HASH,
        session_string=SESSION_STRING
    )
else:
    app = Client(
        "music_bot",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )

# ----------------- PyTgCalls -----------------
pytgcalls = PyTgCalls(app)


# ----------------- AUDIO DOWNLOADER -----------------
def download_audio(url: str, output_path: str = "downloads/"):
    """Download audio from YouTube URL using yt-dlp."""
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


# ----------------- MUSIC PLAY FUNCTION -----------------
async def play_music(chat_id: int, file_path: str):
    """
    Play a downloaded audio file into a Telegram Group Call.
    """
    await pytgcalls.join_group_call(
        chat_id,
        AudioPiped(file_path),
        stream_type=Stream.audio_stream
    )
