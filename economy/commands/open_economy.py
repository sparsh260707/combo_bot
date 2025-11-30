from telegram import Update
from telegram.ext import ContextTypes
from helpers import set_group_status

# commands/open_economy.py
async def open_economy(update, context):
    # your code to open economy commands in group
    await update.message.reply_text("✅ Economy commands are now OPEN in this group!")

