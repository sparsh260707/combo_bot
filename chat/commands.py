from pyrogram import filters
from pyrogram.types import Message
import openai
from config import OPENAI_KEY

openai.api_key = OPENAI_KEY

def register_chat_handlers(bot):

    @bot.on_message(filters.command("chat"))
    async def chat_cmd(_, message: Message):
        query = " ".join(message.command[1:])
        if not query:
            return await message.reply_text("Usage: /chat <message>")

        m = await message.reply_text("Thinking…")

        try:
            resp = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            ans = resp["choices"][0]["message"]["content"]
            await m.edit_text(ans)
        except Exception as e:
            await m.edit_text(str(e))
