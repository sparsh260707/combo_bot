from telegram import Update
from telegram.ext import ContextTypes
from helpers import get_user, is_group_open, users


async def kill(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Group open check
    if not is_group_open(chat_id):
        return await update.message.reply_text(
            "❌ Bhai ruk ja… Economy commands abhi band hai is group me!"
        )

    msg = update.message

    # Must reply to someone
    if not msg.reply_to_message:
        return await msg.reply_text(
            "⚠️ Kisi ko kill karna hai? Uske message ka reply karo pehle!"
        )

    killer = update.effective_user
    killer_id = killer.id
    target_user = msg.reply_to_message.from_user
    target_id = target_user.id

    # BOT ID
    BOT_ID = context.bot.id

    # 1️⃣ Bot ko kill se bachao
    if target_id == BOT_ID:
        return await msg.reply_text(
            "🤖 Bot ko kill?\nBhai zara aukaat check karo 😎\nMain immortal hoon!"
        )

    # 2️⃣ Killer tries to kill themselves
    if killer_id == target_id:
        return await msg.reply_text(
            "❌ Apne aap ko kill? 😂\nBhai kya chal raha dimaag me? Thoda pani pi le 😎"
        )

    # Fetch target data from DB
    target_data = get_user(target_id)

    # 3️⃣ Already killed
    if target_data.get("killed", False):
        return await msg.reply_text(
            f"⚠️ {target_user.first_name} toh pehle se swarg me VIP pass lekar baitha hai 😭\n"
            "Pehle revive karo fir dubara baja dena 😎"
        )

    # Now perform kill
    users.update_one({"user_id": killer_id}, {"$inc": {"kills": 1}})
    users.update_one({"user_id": target_id}, {"$set": {"balance": 0, "killed": True}})

    # 4️⃣ SUCCESS – our style OP message
    return await msg.reply_text(
        f"⚔️ *Scene Over!* \n"
        f"🔥 {killer.first_name} ne {target_user.first_name} ko ek hi vaar me uda diya! 😈\n"
        f"💸 Balance clean → 0\n"
        f"💀 Status → KILLED\n"
        "Bhai OP kill tha ye! 😎"
    )
