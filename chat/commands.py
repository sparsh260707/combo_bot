import openai
from pyrogram import Client, filters
from pyrogram.types import Message
import os
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")


# SIMPLE AI CHAT FUNCTION
async def ai_reply(text: str):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": text}]
    )
    return response["choices"][0]["message"]["content"]


def register_chat_handlers(bot: Client):

    # /chat command
    @bot.on_message(filters.command("chat") & filters.private)
    async def chat_command(_, message: Message):
        if len(message.command) < 2:
            return await message.reply("Use: `/chat your message`")

        user_text = message.text.split(" ", 1)[1]
        reply = await ai_reply(user_text)

        await message.reply(reply)

    # AUTO CHAT IN GROUP
    @bot.on_message(filters.text & filters.group)
    async def auto_group_chat(_, message: Message):
        if message.from_user.is_bot:
            return

        # Ignore commands
        if message.text.startswith("/"):
            return

        reply = await ai_reply(message.text)
        await message.reply_text(reply)
