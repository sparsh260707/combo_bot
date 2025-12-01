from telegram import Update
from telegram.ext import ContextTypes
import random

# Users dict in memory (temporary)
users_data = {}

async def farm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # Initialize if new user
    if user_id not in users_data:
        users_data[user_id] = {"balance": 0}

    earn = random.randint(30, 150)
    users_data[user_id]["balance"] += earn

    await update.message.reply_text(
        f"🚜 You farmed crops and earned **${earn}**!\n"
        f"💰 Balance: {users_data[user_id]['balance']}",
        parse_mode="Markdown"
    )
