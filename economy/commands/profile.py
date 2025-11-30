from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user

async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)

    await update.message.reply_text(
        f"👤 Profile\n"
        f"💰 Balance: ${user['balance']}\n"
        f"⚔️ Kills: {user['kills']}\n"
        f"❤️ Status: {'Dead' if user.get('killed') else 'Alive'}"
    )
