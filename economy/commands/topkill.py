from telegram import Update
from telegram.ext import ContextTypes
from helpers import users

async def topkill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    top_users = users.find().sort("kills", -1).limit(10)
    msg = "⚔️ Top 10 Killers:\n\n"

    for idx, user in enumerate(top_users, start=1):
        try:
            chat = await context.bot.get_chat(user["user_id"])
            username = f"@{chat.username}" if chat.username else chat.first_name
        except:
            username = "Unknown"

        msg += f"{idx}. {username}: {user.get('kills', 0)} kills\n"

    await update.message.reply_text(msg)
