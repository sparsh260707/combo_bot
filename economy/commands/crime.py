from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, users
import random

async def crime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    outcome = random.choice(["success", "fail"])

    if outcome == "success":
        amount = random.randint(100, 400)
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": amount}})
        await update.message.reply_text(f"💣 Crime successful! You earned **${amount}**.")
    else:
        fine = random.randint(50, 200)
        users.update_one({"user_id": user["user_id"]}, {"$inc": {"balance": -fine}})
        await update.message.reply_text(f"🚔 Crime failed! Police fined you **${fine}**.")
