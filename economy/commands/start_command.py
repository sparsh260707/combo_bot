# economy/commands/start_command.py
from telegram import Update
from telegram.ext import CallbackContext

async def start_command(update: Update, context: CallbackContext):
    await update.message.reply_text("👋 Welcome to Economy Bot!")

async def button_handler(update: Update, context: CallbackContext):
    # Agar inline buttons hain, yaha handle karo
    await update.callback_query.answer()
