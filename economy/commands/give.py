from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, users

async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to someone to give coins!")

    if len(context.args) == 0:
        return await update.message.reply_text("❌ Usage: /give <amount>")

    try:
        amount = int(context.args[0])
    except:
        return await update.message.reply_text("❌ Amount must be a number!")

    giver = get_user(update.effective_user.id)
    receiver_id = update.message.reply_to_message.from_user.id
    receiver = get_user(receiver_id)

    if giver["balance"] < amount:
        return await update.message.reply_text("❌ You don't have enough coins!")

    # Update balances
    users.update_one({"user_id": giver["user_id"]}, {"$inc": {"balance": -amount}})
    users.update_one({"user_id": receiver_id}, {"$inc": {"balance": amount}})

    await update.message.reply_text(f"💸 You sent {amount} coins to {receiver['user_id']}!")
