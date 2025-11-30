from telegram import Update
from telegram.ext import ContextTypes
from helpers import set_group_status

async def close_economy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    set_group_status(chat_id, 0)
    await update.message.reply_text("❌ Economy commands are now CLOSED in this group!")
