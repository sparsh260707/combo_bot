from pyrogram import Client, filters
from pytgcalls import PyTgCalls, idle
from pytgcalls.types.stream import StreamType
from pytgcalls.types.input_stream import AudioPiped
import yt_dlp
import asyncio

from .config import API_ID, API_HASH, BOT_TOKEN, SESSION

# Bot client
bot = Client("MusicBot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Assistant client (plays music)
assistant = Client("assistant", api_id=API_ID, api_hash=API_HASH, session_string=SESSION)

# PyTgCalls
pytgcalls = PyTgCalls(assistant)

# ---------------- PLAY ---------------- #
@bot.on_message(filters.command("play") & filters.group)
async def play(_, msg):
    if len(msg.command) < 2:
        return await msg.reply("🔍 Song ka naam do!\nExample: /play tu hai ke nhi")

    query = msg.text.split(None, 1)[1]

    await msg.reply("🎧 Searching...")

    # YT search + download
    ydl_opts = {
        "format": "bestaudio",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": "song.%(ext)s",
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(f"ytsearch:{query}", download=True)["entries"][0]
        url = info["url"]

    await msg.reply(f"▶️ Playing: **{info['title']}**")

    try:
        await pytgcalls.join_group_call(
            msg.chat.id,
            AudioPiped(url),
            stream_type=StreamType().local_stream,
        )
    except Exception as e:
        await msg.reply(str(e))


# ---------------- STOP ---------------- #
@bot.on_message(filters.command("stop") & filters.group)
async def stop(_, msg):
    try:
        await pytgcalls.leave_group_call(msg.chat.id)
        await msg.reply("⏹ Stopped Music")
    except:
        await msg.reply("❌ Not playing anything.")


# ---------------- SKIP ---------------- #
@bot.on_message(filters.command("skip") & filters.group)
async def skip(_, msg):
    await msg.reply("⏭ Skip command abhi queue bina kaam nahi karega.")
