from pyrogram import Client, filters
from .youtube import yt_search
from .downloader import download_audio
from .call import pytgcalls, assistant

@Client.on_message(filters.command("play") & filters.group)
async def play(_, message):
    query = " ".join(message.command[1:])
    if not query:
        return await message.reply("❗ **Song name do!**")

    await message.reply("🔍 Searching...")

    url, title = yt_search(query)
    if not url:
        return await message.reply("Song nahi mila.")

    file = download_audio(url)
    if not file:
        return await message.reply("Download error aaya.")

    await message.reply(f"🎧 Playing: **{title}**")

    try:
        await pytgcalls.join_group_call(
            message.chat.id,
            AudioPiped(file)
        )
    except:
        await message.reply("Assistant add nahi hai. Pehle usko group me add karo.")

@Client.on_message(filters.command("end") & filters.group)
async def end(_, message):
    try:
        await pytgcalls.leave_group_call(message.chat.id)
        await message.reply("⛔ Stopped.")
    except:
        await message.reply("Already stopped.")
