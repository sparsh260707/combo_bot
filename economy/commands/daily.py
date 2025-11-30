from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, is_group_open
from datetime import datetime, timedelta

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_group_open(update.effective_chat.id):
        return await update.message.reply_text("❌ Economy commands are closed in this group!")

    user = get_user(update.effective_user.id)
    now = datetime.utcnow()

    if "last_daily" in user:
        last = user["last_daily"]
        if now - last < timedelta(hours=24):
            remaining = timedelta(hours=24) - (now - last)
            hours = remaining.seconds // 3600
            mins = (remaining.seconds % 3600) // 60
            return await update.message.reply_text(f"⏳ Already claimed!\nNext claim: {hours}h {mins}m")

    reward = 500
    from helpers import users
    users.update_one({"user_id": user["user_id"]}, {"$set": {"balance": user["balance"] + reward, "last_daily": now}})
    await update.message.reply_text(f"🎁 Daily Reward Claimed!\nEarned: {reward} coins\n💰 New Balance: {user['balance'] + reward}")
