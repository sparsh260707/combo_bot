from pyrogram import Client
from config import BOT_TOKEN, API_ID, API_HASH
from economy import register_economy_handlers
from music import register_music_handlers, assistant_client, pytgcalls
from chat import register_chat_handlers

bot = Client("bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Register all handlers
register_economy_handlers(bot)
register_music_handlers(bot, assistant_client, pytgcalls)
register_chat_handlers(bot)

# Start assistant + PyTgCalls
assistant_client.start()
pytgcalls.start()

bot.run()
