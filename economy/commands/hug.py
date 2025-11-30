from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random

# 10 Hug GIFs
HUG_GIFS = [
    "https://media.giphy.com/media/l2QDM9Jnim1YVILXa/giphy.gif",
    "https://media.giphy.com/media/od5H3PmEG5EVq/giphy.gif",
    "https://media.giphy.com/media/xT0GqeSlGSRQutnC2g/giphy.gif",
    "https://media.giphy.com/media/wnsgren9NtITS/giphy.gif",
    "https://media.giphy.com/media/3ZnBrkqoaI2hq/giphy.gif",
    "https://media.giphy.com/media/49mdjsMrH7oze/giphy.gif",
    "https://media.giphy.com/media/svXXBgduBsJ1u/giphy.gif",
    "https://media.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif",
    "https://media.giphy.com/media/BXrwTdoho6hkQ/giphy.gif",
    "https://media.giphy.com/media/xT8qBepJQG8OZX9Ji0/giphy.gif"
]

async def hug(update: Update, context: ContextTypes.DEFAULT_TYPE):

    # Hugger (user sending command)
    hugger = update.effective_user
    hugger_name = hugger.first_name
    hugger_id = hugger.id

    # Target user (reply required)
    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
    elif context.args:
        await update.message.reply_text("Reply karke hug karo taaki ID mil sake! 🤗")
        return
    else:
        await update.message.reply_text("Kisko hug karna hai? Reply karo! 🫂")
        return

    target_name = target.first_name
    target_id = target.id

    # Random GIF
    gif_url = random.choice(HUG_GIFS)

    # Caption with clickable IDs
    caption = (
        f"<b><a href='tg://user?id={hugger_id}'>{hugger_name}</a></b> "
        f"hugs "
        f"<b><a href='tg://user?id={target_id}'>{target_name}</a></b> 🤗"
    )

    # Send GIF
    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )

# --------------------------
# Add this handler in main.py
# application.add_handler(CommandHandler("hug", hug))
