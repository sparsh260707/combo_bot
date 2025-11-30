from telegram import Update
from telegram.ext import ContextTypes
from helpers import random_percentage

async def crush(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to check your crush %.")

    target_name = update.message.reply_to_message.from_user.first_name
    percent = random_percentage()
    await update.message.reply_text(f"💘 {target_name} Crush Percentage: {percent}%")
