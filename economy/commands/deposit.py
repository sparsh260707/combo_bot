from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, users

async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("Usage: /deposit amount")

    amount = int(context.args[0])
    user = get_user(update.effective_user.id)

    if user["balance"] < amount:
        return await update.message.reply_text("❌ Not enough balance.")

    users.update_one({"user_id": user["user_id"]}, {
        "$inc": {"balance": -amount, "bank": amount}
    })

    await update.message.reply_text(f"🏦 Deposited **${amount}** to your bank!")
