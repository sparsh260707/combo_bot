from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user

async def bank(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    bank_amount = user.get("bank", 0)

    await update.message.reply_text(
        f"🏦 *Bank Account*\n"
        f"💳 Balance in bank: **${bank_amount}**",
        parse_mode="none"
    )
