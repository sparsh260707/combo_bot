from telegram import Update
from telegram.ext import ContextTypes

async def own(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎨 Create your own sticker pack using this command! (Work in progress)")
