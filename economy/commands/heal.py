from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, users

async def heal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    if not user.get("killed"):
        return await update.message.reply_text("❤️ You are already alive.")

    users.update_one({"user_id": user["user_id"]}, {"$set": {"killed": False}})
    await update.message.reply_text("💖 You healed yourself and are alive again!")
