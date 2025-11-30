from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user
from datetime import datetime

async def claim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user = get_user(user_id)

    if "claimed" in user and user["claimed"]:
        return await update.message.reply_text("❌ You have already claimed your 3000 coins!")

    users.update_one({"user_id": user_id}, {"$set": {"balance": 3000, "claimed": True}})
    await update.message.reply_text("🎉 You claimed 3000 coins! 💰")
