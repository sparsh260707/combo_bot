from telegram import Update
from telegram.ext import ContextTypes, CommandHandler
import random
import time

# 10 Couple GIFs
COUPLE_GIFS = [
    "https://media.giphy.com/media/3oKIPwoeGErMmaI43C/giphy.gif",
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
    "https://media.giphy.com/media/3oz8xKaR836UJOYeOc/giphy.gif",
    "https://media.giphy.com/media/l41YtZOb9EUABnuqA/giphy.gif",
    "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif",
    "https://media.giphy.com/media/l0ExncehJzexFpRHq/giphy.gif",
    "https://media.giphy.com/media/26FPnsRww4p3jJ6k0/giphy.gif",
    "https://media.giphy.com/media/3o6Zt481isNVuQI1l6/giphy.gif",
    "https://media.giphy.com/media/xT0xeJpnrWC4XWblEk/giphy.gif"
]

# Couples storage: key = (user1_id, user2_id), value = timestamp
couples = {}

# Function to clean expired couples (older than 24 hours)
def clean_expired_couples():
    now = time.time()
    expired = [pair for pair, ts in couples.items() if now - ts > 86400]
    for pair in expired:
        del couples[pair]

async def couple(update: Update, context: ContextTypes.DEFAULT_TYPE):
    clean_expired_couples()

    chat = update.effective_chat
    # Get all chat members (only works if bot is admin in group)
    members = []
    try:
        async for member in context.bot.get_chat_administrators(chat.id):
            # Exclude bots
            if not member.user.is_bot:
                members.append(member.user)
        async for member in context.bot.get_chat_members(chat.id):
            if not member.user.is_bot:
                members.append(member.user)
    except:
        await update.message.reply_text("Bot needs to be admin or cannot fetch members 😅")
        return

    # Remove duplicates
    members = list({m.id: m for m in members}.values())

    if len(members) < 2:
        await update.message.reply_text("Group me kam se kam 2 members hone chahiye 😅")
        return

    # Try to pick random pair who is not already couple
    attempts = 0
    max_attempts = 50
    while attempts < max_attempts:
        user1, user2 = random.sample(members, 2)
        pair_key = tuple(sorted([user1.id, user2.id]))
        if pair_key not in couples:
            # New couple
            couples[pair_key] = time.time()
            break
        attempts += 1
    else:
        # All pairs already exists → pick random existing couple
        pair_key = random.choice(list(couples.keys()))
        user1 = next((u for u in members if u.id == pair_key[0]), None)
        user2 = next((u for u in members if u.id == pair_key[1]), None)
        couples[pair_key] = time.time()  # refresh timestamp

    # Random GIF
    gif_url = random.choice(COUPLE_GIFS)

    # Caption with clickable IDs
    caption = (
        f"💑 𝑻𝒐𝒅𝒂𝒚'𝒔 𝒄𝒐𝒖𝒑𝒍𝒆 💑\n\n"
        f"<b><a href='tg://user?id={user1.id}'>{user1.first_name}</a></b> 💖 "
        f"<b><a href='tg://user?id={user2.id}'>{user2.first_name}</a></b>\n\n"
        f"Today's couple! 🔥"
    )

    await update.message.reply_animation(
        animation=gif_url,
        caption=caption,
        parse_mode="HTML"
    )

# --------------------------
# Add this handler in main.py
# application.add_handler(CommandHandler("couple", couple))
