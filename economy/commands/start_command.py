from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from helpers import users     # <- yaha se users set import

BOT_IMAGE_URL = "https://files.catbox.moe/z1skp4.jpg"


# /start command
async def start_command(update: Update, context: CallbackContext):
    chat = update.effective_chat
    user = update.effective_user

    # ---------------------- GROUP START ----------------------
    if chat.type in ["group", "supergroup"]:
        return await update.message.reply_text(
            f"👋 **Hello {user.first_name}!**\n"
            f"Thanks for using Akeno in this group 💙\n\n"
            f"Use /help to see all commands!",
            parse_mode="Markdown"
        )

    # ---------------------- DM START ----------------------
    # ⬇️ YAHI ADD KARNA HAI
    users.add(user.id)

    text = (
        f"⬤ 𖦹 {user.first_name} - ᴄᴜᴛɪᴇ, ꜱᴀꜱꜱʏ, ᴀ ʟɪᴛᴛʟᴇ ᴡɪʟᴅ ᴀɴᴅ ɢᴀᴍᴇ ᴘᴀʀᴛɴᴇʀ 🤍\n\n"
        "⬤ ᴊᴜꜱᴛ ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴇɴᴊᴏʏ ᴄʜᴀᴛꜱ & ɢᴀᴍᴇꜱ ᴡɪᴛʜ ᴍᴇ!\n\n"
        "☑ Choose an option below:"
    )

    keyboard = [
        [InlineKeyboardButton("💬 Talk to 𝐀𝐤e𝐧o", callback_data="talk")],
        [
            InlineKeyboardButton("🧸 Friends", url="https://t.me/mich_family_group"),
            InlineKeyboardButton("🎮 Games", callback_data="games")
        ],
        [InlineKeyboardButton("👻 Meet me here", url="https://t.me/mich_family_group")],
        [InlineKeyboardButton("👥 Add me to your group", url="https://t.me/?startgroup=true")],
        [InlineKeyboardButton("🔑 Owner Panel", url="https://t.me/INTROVERT_HU_YRR")]
    ]

    await update.message.reply_photo(
        photo=BOT_IMAGE_URL,
        caption=text,
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )


# ------------------- Callback query handler -------------------
async def button_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    data = query.data

    if data == "talk":
        await query.answer()
        return await query.message.reply_text("💬 Akeno is here… bolo cutie ❤️✨")

    if data == "games":
        await query.answer()
        return await query.message.reply_text(
            "💰 *Akeno Economy Guide*\n\n"
            "🔹 /bal — Check balance\n"
            "🔹 /rob — Rob someone\n"
            "🔹 /kill — Kill someone\n"
            "🔹 /revive — Revive\n"
            "🔹 /give — Gift money\n"
            "🔹 /protect — Buy protection\n"
            "🔹 /transfer — Owner only\n\n"
            "🎮 Earn, Gift & Rule the Economy!",
            parse_mode="Markdown"
        )
