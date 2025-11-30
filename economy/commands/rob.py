from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, is_group_open, users
import random


async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Economy open check
    if not is_group_open(chat_id):
        return await update.message.reply_text(
            "❌ Bhai ruk ja… Economy commands abhi band hai is group me!"
        )

    msg = update.message

    # Must reply to someone
    if not msg.reply_to_message:
        return await msg.reply_text(
            "⚠️ Rob karna hai? Pahle jisko lutna hai uske message ka reply karo!"
        )

    robber = update.effective_user
    robber_id = robber.id
    target = msg.reply_to_message.from_user
    target_id = target.id

    # BOT ID
    BOT_ID = context.bot.id

    # 1️⃣ Bot ko rob se bachao
    if target_id == BOT_ID:
        return await msg.reply_text(
            "🤖 Bot ko rob?\nBhai main digital ATM nahi hoon 😎\nTu loot nahi sakta mujhe!"
        )

    # 2️⃣ Self-rob
    if robber_id == target_id:
        return await msg.reply_text(
            "❌ Khud ko rob? 😂\nBhai apne hi jeb me haath dalke kya nikaal lega?"
        )

    # Fetch data
    target_data = get_user(target_id)
    robber_data = get_user(robber_id)

    # 3️⃣ If target is killed
    if target_data.get("killed", False):
        return await msg.reply_text(
            f"💀 {target.first_name} toh already swarg me hai bhai 😭\n"
            "Swarg me paise nahi milte… kisi aur ko rob kar!"
        )

    # 4️⃣ If target has no money
    target_balance = target_data.get("balance", 0)
    if target_balance <= 0:
        return await msg.reply_text(
            f"😒 {target.first_name} ke jeb me to hawa chal rahi hai bhai!\n"
            "Rob karne layak kuch nahi mila. Koi aur dhoond 😎"
        )

    # 5️⃣ Rob amount (25% to 45%)
    amount = random.randint(int(target_balance * 0.25), int(target_balance * 0.45))

    # Update DB
    users.update_one({"user_id": robber_id}, {"$inc": {"balance": amount}})
    users.update_one({"user_id": target_id}, {"$inc": {"balance": -amount}})

    # 6️⃣ SUCCESS MESSAGE (OP STYLE)
    return await msg.reply_text(
        f"🤑 *Rob Successful!*\n"
        f"🔥 {robber.first_name} ne style me {target.first_name} ka jeb saaf kar diya! 😈\n"
        f"💸 Loot: +{amount}\n"
        f"😭 {target.first_name} ka loss: -{amount}\n"
        "Bhai asli gangsta move tha ye 😎💰"
    )
