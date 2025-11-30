from telegram import Update
from telegram.ext import ContextTypes
from helpers import is_group_open
import random

async def protect(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")
    if random.choice([True, False]):
        await update.message.reply_text("🛡 You are protected from the next robbery!")
    else:
        await update.message.reply_text("⚠️ Protection failed! Try again.")
