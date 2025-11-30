import os
from telegram import Update
from telegram.ext import CallbackContext
# Assuming these are available from helpers.py and imported in main.py
from helpers import get_user, users 

# Load the owner ID from environment variables
# IMPORTANT: The OWNER_ID must be set in your .env file
try:
    # It's crucial to load OWNER_ID from the environment and ensure it's an integer
    OWNER_ID = int(os.getenv("OWNER_ID")) 
except (TypeError, ValueError):
    # Fallback/Error handling if OWNER_ID is not set or invalid
    OWNER_ID =8379938997

async def transfer_balance(update: Update, context: CallbackContext):
    """
    Allows the bot owner to manually add or remove coins from a user's balance.
    Command format: /transfer <amount> (in reply to a user) or /transfer <user_id> <amount>
    Use negative amount to remove coins (e.g., -500).
    """
    
    # 1. Owner Check
    if update.effective_user.id != OWNER_ID:
        await update.message.reply_text("🚫 This command is reserved for the bot owner only.")
        return

    # 2. Argument Parsing (Target and Amount)
    args = context.args
    target_user_id = None
    amount = None

    if update.message.reply_to_message:
        # Case 1: Reply to a user. Format: /transfer <amount>
        if len(args) == 1:
            try:
                amount = int(args[0])
                target_user_id = update.message.reply_to_message.from_user.id
            except ValueError:
                await update.message.reply_text("❌ Invalid amount provided. Usage: `/transfer <amount>` (in reply). Amount must be a number.")
                return
        else:
            await update.message.reply_text("❌ Missing amount. Usage: `/transfer <amount>` (in reply).")
            return
            
    elif len(args) == 2:
        # Case 2: User ID provided. Format: /transfer <user_id> <amount>
        try:
            target_user_id = int(args[0])
            amount = int(args[1])
        except ValueError:
            await update.message.reply_text("❌ Invalid user ID or amount. Usage: `/transfer <user_id> <amount>`.")
            return
            
    else:
        # Invalid arguments
        await update.message.reply_text("❌ Invalid usage. Use: `/transfer <amount>` (in reply) or `/transfer <user_id> <amount>`.")
        return

    # 3. Execution
    try:
        # Get target user's current data (ensure they exist in DB)
        target_user = get_user(target_user_id)
        
        # Update balance in DB using $inc
        users.update_one(
            {"user_id": target_user_id},
            {"$inc": {"balance": amount}}
        )
        
        # Get new balance for confirmation message
        updated_user = get_user(target_user_id)
        new_balance = updated_user['balance']
        
        action = "added to" if amount >= 0 else "removed from"
        
        # Send confirmation
        await update.message.reply_text(
            f"✅ *Success!* \n"
            f"${abs(amount)} has been *{action}* user `{target_user_id}`'s balance (Name: {target_user.get('username', 'N/A')}).\n"
            f"New Balance: ${new_balance}",
            parse_mode="Markdown"
        )
        
    except Exception as e:
        print(f"Transfer error for user {target_user_id}: {e}")
        await update.message.reply_text("❌ An error occurred during the transfer. The target user might not be registered in the economy yet.")
