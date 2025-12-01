import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters
)

# -------------------- LOAD ENV --------------------
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID", 0))
MONGO_URI = os.getenv("MONGO_URI")
API_ID = int(os.getenv("API_ID", 0))
API_HASH = os.getenv("API_HASH")
SESSION_STRING = os.getenv("SESSION_STRING", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# -------------------- HELPERS --------------------
from helpers.economy_helper import (
    get_user, user_db, add_group_id, users, groups,
    add_balance, deduct_balance, get_balance,
    is_group_open, set_group_status
)

from helpers.music_helper import app as music_app, pytgcalls, download_audio, play_music
from helpers.chat_helper import ai_reply

# -------------------- COMMANDS --------------------
from economy.commands.start_command import start_command, button_handler
from economy.commands.group_management import register_group_management
from economy.commands.economy_guide import economy_guide
from economy.commands.transfer_balance import transfer_balance
from economy.commands.claim import claim
from economy.commands.own import own
from economy.commands.crush import crush
from economy.commands.love import love
from economy.commands.slap import slap
from economy.commands.items import items
from economy.commands.item import item
from economy.commands.give import give
from economy.commands.daily import daily
from economy.commands.rob import rob
from economy.commands.protect import protect
from economy.commands.toprich import toprich
from economy.commands.topkill import topkill
from economy.commands.kill import kill
from economy.commands.revive import revive
from economy.commands.open_economy import open_economy
from economy.commands.close_economy import close_economy
from economy.commands.punch import punch
from economy.commands.hug import hug
from economy.commands.couple import couple
from economy.commands.mine import mine
from economy.commands.farm import farm
from economy.commands.crime import crime
from economy.commands.heal import heal
from economy.commands.shop import shop
from economy.commands.buy import buy
from economy.commands.sell import sell
from economy.commands.profile import profile
from economy.commands.bank import bank
from economy.commands.deposit import deposit
from economy.commands.withdraw import withdraw

# -------------------- ECONOMY --------------------
async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    name = update.effective_user.first_name

    if update.message.reply_to_message:
        target = update.message.reply_to_message.from_user
        user_id = target.id
        name = target.first_name

    user = get_user(user_id)
    rank_data = list(user_db.find().sort("balance", -1))
    ids = [u["user_id"] for u in rank_data]
    rank = ids.index(user_id) + 1 if user_id in ids else len(ids) + 1
    status = "☠️ Dead" if user.get("killed") else "Alive"

    await update.message.reply_text(
        f"👤 𝐍𝐚𝐦𝐞: {name}\n"
        f"💰 𝐁𝐚𝐥𝐚𝐧𝐜𝐞: ${user['balance']}\n"
        f"🏆 𝐆𝐥𝐨𝐛𝐚𝐥 𝐑𝐚𝐧𝐤: #{rank}\n"
        f"❤️ 𝐒𝐭𝐚𝐭𝐮𝐬: {status}\n"
        f"⚔️ 𝐊𝐢𝐥𝐥s: {user['kills']}"
    )

async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = get_user(update.effective_user.id)
    reward = 200
    add_balance(user["user_id"], reward)
    await update.message.reply_text(f"💼 You worked and earned {reward} coins!")

# -------------------- MUSIC --------------------
async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Please provide a YouTube URL.")
    url = context.args[0]
    msg = await update.message.reply_text("⏳ Downloading audio...")
    file_path = download_audio(url)
    await msg.edit_text(f"✅ Audio downloaded!\nUse /join to play in VC.")
    context.chat_data["last_song"] = file_path

async def join(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if "last_song" not in context.chat_data:
        return await update.message.reply_text("❌ First use /play with a YouTube URL.")
    file_path = context.chat_data["last_song"]
    await update.message.reply_text("🎧 Joining voice chat...")
    await play_music(chat_id, file_path)
    await update.message.reply_text("🎶 Now playing in VC!")

# -------------------- CHAT --------------------
async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        return await update.message.reply_text("❌ Please provide a message.")
    user_text = " ".join(context.args)
    reply = ai_reply(user_text)
    await update.message.reply_text(reply)

# -------------------- AUTH --------------------
async def test_restart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return await update.message.reply_text("⛔ You are not authorized.")
    await update.message.reply_text("🔄 Restarting bot...")
    os._exit(1)

# -------------------- TRACK USERS --------------------
async def track_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat
    if chat.type in ["group", "supergroup"]:
        add_group_id(chat.id)

# -------------------- ERROR HANDLER --------------------
async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print(f"⚠️ Error: {context.error}")
    if isinstance(update, Update) and update.effective_message:
        await update.effective_message.reply_text("❌ Something went wrong!")

# -------------------- MAIN --------------------
def main():
    # Start Music Client
    music_app.start()
    pytgcalls.start()

    # Start Telegram Bot
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_error_handler(error_handler)

    # Track users
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, track_users))

    # START
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Restart
    app.add_handler(CommandHandler("test", test_restart))

    # Economy Commands
    economy_commands = [
        ("balance", balance), ("work", work), ("economy", economy_guide),
        ("transfer", transfer_balance), ("claim", claim), ("own", own),
        ("crush", crush), ("love", love), ("slap", slap),
        ("items", items), ("item", item), ("give", give), ("daily", daily),
        ("rob", rob), ("protect", protect), ("toprich", toprich),
        ("topkill", topkill), ("kill", kill), ("revive", revive),
        ("open", open_economy), ("close", close_economy)
    ]
    for cmd, handler in economy_commands:
        app.add_handler(CommandHandler(cmd, handler))

    # Hidden Commands
    hidden_cmds = [
        ("mine", mine), ("farm", farm), ("crime", crime), ("heal", heal),
        ("shop", shop), ("buy", buy), ("sell", sell),
        ("profile", profile), ("bank", bank), ("deposit", deposit),
        ("withdraw", withdraw)
    ]
    for cmd, handler in hidden_cmds:
        app.add_handler(CommandHandler(cmd, handler))

    # Fun Commands
    fun_commands = [("punch", punch), ("hug", hug), ("couple", couple)]
    for cmd, handler in fun_commands:
        app.add_handler(CommandHandler(cmd, handler))

    # Group management
    register_group_management(app)

    # Music commands
    app.add_handler(CommandHandler("play", play))
    app.add_handler(CommandHandler("join", join))

    # Chat command
    app.add_handler(CommandHandler("chat", chat))

    print("🚀 Combo Bot Started Successfully!")
    app.run_polling()


if __name__ == "__main__":
    main()
