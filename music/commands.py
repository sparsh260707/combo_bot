from pyrogram import Client, filters
from pyrogram.types import Message
from pytgcalls import PyTgCalls
from pytgcalls.types.input_stream import AudioPiped
import asyncio
import os

from config import API_ID, API_HASH, ASSISTANT_SESSION
from helpers import download_and_prepare_audio

assistant = Client(
    "assistant",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=ASSISTANT_SESSION
)

pytgcalls = PyTgCalls(assistant)

queues = {}  # {chat_id: [(filepath, title)]}

def register_music_handlers(bot: Client):

    @bot.on_message(filters.command("play") & filters.group)
    async def play_cmd(_, message: Message):
        chat_id = message.chat.id
        query = " ".join(message.command[1:])

        if not query:
            return await message.reply_text("Usage: /play <song>")

        m = await message.reply_text("Downloading…")

        file, title = await asyncio.get_event_loop().run_in_executor(
            None,
            lambda: download_and_prepare_audio(query)
        )

        if chat_id not in queues:
            queues[chat_id] = []

        queues[chat_id].append((file, title))

        if len(queues[chat_id]) == 1:
            try:
                await assistant.start()
                await pytgcalls.join_group_call(
                    chat_id,
                    AudioPiped(file),
                )
                await m.edit_text(f"▶️ Playing: **{title}**")
            except Exception as e:
                await m.edit_text(f"Assistant Error: {e}")
        else:
            await m.edit_text(f"Added to queue: **{title}**")

    @bot.on_message(filters.command("skip"))
    async def skip_cmd(_, message: Message):
        chat_id = message.chat.id

        if chat_id not in queues or len(queues[chat_id]) <= 1:
            return await message.reply_text("Queue empty.")

        queues[chat_id].pop(0)
        next_file, title = queues[chat_id][0]

        await pytgcalls.change_stream(chat_id, AudioPiped(next_file))
        await message.reply_text(f"⏭ Skipped. Now playing: **{title}**")

    @bot.on_message(filters.command("stop"))
    async def stop_cmd(_, message: Message):
        chat_id = message.chat.id
        try:
            await pytgcalls.leave_group_call(chat_id)
            queues[chat_id] = []
            await message.reply_text("Stopped.")
        except:
            await message.reply_text("Already stopped.")
