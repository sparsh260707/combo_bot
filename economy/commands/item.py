from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user

async def item(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    if "items" not in user or len(user["items"]) == 0:
        await update.message.reply_text(f"❛ {update.effective_user.first_name} has no items yet 😢")
    else:
        item_list = "\n".join(user["items"])
        await update.message.reply_text(f"📦 Your Items:\n{item_list}")
