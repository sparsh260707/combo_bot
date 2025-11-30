import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_URI = os.getenv("MONGO_URI")

# NEW
ASSISTANT_SESSION = os.getenv("ASSISTANT_SESSION")   # Music ke liye (user session)
OPENAI_KEY = os.getenv("OPENAI_KEY")                # Chat ke liye
DOWNLOADS_DIR = os.getenv("DOWNLOADS_DIR", "downloads")
