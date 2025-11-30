from telegram import Update
from telegram.ext import ContextTypes

async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🛒 *Shop Items*\n"
        "• 🔫 Gun — $500\n"
        "• 🛡️ Shield — $300\n"
        "• 💊 Health Pack — $200\n\n"
        "Buy using: `/buy item_name`",
        parse_mode="Markdown"
    )
