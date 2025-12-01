from telegram import Update
from telegram.ext import CallbackContext
from helpers.economy_helper import get_user, user_db
import os

OWNER_ID = int(os.getenv("OWNER_ID", 8379938997))

async def transfer_balance(update: Update, context: CallbackContext):
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("🚫 This command is reserved for the bot owner only.")
        return

    args = context.args
    target_user_id = None
    amount = None

    if update.message.reply_to_message:
        if len(args) == 1:
            try:
                amount = int(args[0])
                target_user_id = update.message.reply_to_message.from_user.id
            except ValueError:
                await update.message.reply_text("❌ Invalid amount.")
                return
        else:
            await update.message.reply_text("❌ Missing amount.")
            return
    elif len(args) == 2:
        try:
            target_user_id = int(args[0])
            amount = int(args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID or amount.")
            return
    else:
        await update.message.reply_text("❌ Invalid usage.")
        return

    # Execute DB update
    get_user(target_user_id)  # ensure user exists
    user_db.update_one(
        {"user_id": target_user_id},
        {"$inc": {"balance": amount}}
    )
    new_balance = get_user(target_user_id)['balance']
    action = "added to" if amount >= 0 else "removed from"
    await update.message.reply_text(
        f"✅ ${abs(amount)} has been {action} user `{target_user_id}`'s balance.\n"
        f"New Balance: ${new_balance}",
        parse_mode="Markdown"
    )
