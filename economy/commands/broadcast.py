from telegram import Update
from telegram.ext import ContextTypes

# helpers me already saved list — user IDs, group IDs
from helpers import users, groups  

import asyncio

OWNER_ID = 8379938997  # <-- apna real owner id daalna

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    # --- Owner Check ---
    if user_id != OWNER_ID:
        return await update.message.reply_text("⛔ Yeh command sirf owner ke liye reserved hai!")

    # --- No Message Provided ---
    if not context.args:
        return await update.message.reply_text("⚠️ Usage: /broadcast <message>")

    # --- Message Combine ---
    text = " ".join(context.args)

    sent = 0
    failed = 0

    # ----- Send to all start users -----
    for uid in users:
        try:
            await context.bot.send_message(uid, text)
            await asyncio.sleep(0.05)
            sent += 1
        except:
            failed += 1

    # ----- Send to all group chats -----
    for gid in groups:
        try:
            await context.bot.send_message(gid, text)
            await asyncio.sleep(0.05)
            sent += 1
        except:
            failed += 1

    # ----- Reply with summary -----
    return await update.message.reply_text(
        f"📢 **Broadcast Completed**\n\n"
        f"✅ Sent: {sent}\n"
        f"❌ Failed: {failed}",
        parse_mode="Markdown"
    )
