from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, users

async def revive(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.reply_to_message:
        return await update.message.reply_text("⚠️ Reply to the user you want to revive.")

    target_id = update.message.reply_to_message.from_user.id
    target = get_user(target_id)

    if not target.get("killed", False):
        return await update.message.reply_text("❌ This user is not killed!")

    if target["balance"] < 200:
        return await update.message.reply_text("❌ User does not have 200 coins to revive!")

    new_balance = target["balance"] - 200
    users.update_one({"user_id": target_id}, {"$set": {"balance": new_balance, "killed": False}})

    await update.message.reply_text(
        f"❤️ {update.message.reply_to_message.from_user.first_name} has been revived!\n"
        f"💰 200 coins deducted\n📌 New Balance: {new_balance}"
    )
