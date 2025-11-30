# helpers/economy_helper.py
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# ----------------- Collections -----------------
user_db = db["users"]
group_db = db["groups"]
couples_db = db["couples"]

# ----------------- Runtime sets -----------------
users = set()    # DM me start karne wale users
groups = set()   # jaha bot added hai

# ----------------- User Functions -----------------
def get_user(user_id: int):
    """Fetch user from DB or create new if doesn't exist."""
    user = user_db.find_one({"user_id": user_id})
    if not user:
        user_db.insert_one({
            "user_id": user_id,
            "balance": 0,
            "kills": 0,
            "killed": False,
        })
        user = user_db.find_one({"user_id": user_id})
    return user

def add_balance(user_id: int, amount: int):
    """Add balance to a user."""
    user = get_user(user_id)
    new_balance = user["balance"] + amount
    user_db.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
    return new_balance

def deduct_balance(user_id: int, amount: int):
    """Deduct balance from a user."""
    user = get_user(user_id)
    if user["balance"] >= amount:
        new_balance = user["balance"] - amount
        user_db.update_one({"user_id": user_id}, {"$set": {"balance": new_balance}})
        return True, new_balance
    return False, user["balance"]

def get_balance(user_id: int):
    """Return user's current balance."""
    user = get_user(user_id)
    return user["balance"]

# ----------------- Group Functions -----------------
def is_group_open(chat_id: int):
    """Check if economy is open in group."""
    group = group_db.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True

def set_group_status(chat_id: int, status: bool):
    """Set economy open/close status in group."""
    group_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"open": status}},
        upsert=True
    )

def add_group_id(chat_id: int):
    """Track which groups bot is added to."""
    groups.add(chat_id)

# ----------------- Utility Functions -----------------
def random_percentage():
    """Return random integer 1-100."""
    return random.randint(1, 100)
