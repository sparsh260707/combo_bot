from telegram import Update
from telegram.ext import ContextTypes
from helpers import users

async def toprich(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("balance", -1).limit(10)
    msg = "🏆 Top 10 Richest Users:\n\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            username = f"@{chat.username}" if chat.username else chat.first_name
        except:
            username = "Unknown"

        msg += f"{idx}. {username}: ${user['balance']}\n"

    msg += "\nNote: Use username for clickable profile."
    await update.message.reply_text(msg)
