from pymongo import MongoClient
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import random

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
client = MongoClient(MONGO_URI)
db = client["economy_bot"]

# 👉 MongoDB Collections
user_db = db["users"]
group_db = db["groups"]
couples = db["couples"]

# 👉 Runtime sets (for broadcast)
users = set()    # DM me start karne wale users
groups = set()   # jaha bot added hai


# ----------------------- USER SYSTEM -----------------------
def get_user(user_id):
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


# ---------------------- GROUP ECONOMY ----------------------
def is_group_open(chat_id):
    group = group_db.find_one({"chat_id": chat_id})
    return group.get("open", True) if group else True


def set_group_status(chat_id, status: bool):
    group_db.update_one(
        {"chat_id": chat_id},
        {"$set": {"open": status}},
        upsert=True
    )


# ---------------------- BROADCAST SYSTEM ----------------------
# Track which groups bot is added to
def add_group_id(chat_id):
    groups.add(chat_id)


# ---------------------- RANDOM PERCENT ----------------------
def random_percentage():
    return random.randint(1, 100)
