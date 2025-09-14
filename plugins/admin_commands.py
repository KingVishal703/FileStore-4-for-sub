from pyrogram import filters
from database.database import db_set_premium_expiry
from time import time
from config import PREMIUM_DURATION, ADMIN_ID

@Bot.on_message(filters.command("setpremium") & filters.user(ADMIN_ID))
async def admin_setpremium(client, message):
    args = message.text.split()
    if len(args) != 3:
        await message.reply("Usage: /setpremium <user_id> <plan(10|30|60)>")
        return
    
    user_id = int(args[1])
    plan = args[2]
    if plan not in PREMIUM_DURATION:
        await message.reply("Invalid plan. Use 10, 30, or 60.")
        return
    
    expires = int(time()) + PREMIUM_DURATION[plan]
    await db_set_premium_expiry(user_id, expires)
    await message.reply(f"User {user_id} को {PREMIUM_DURATION[plan]//86400} दिनों के लिए premium दे दिया गया है।")
    await client.send_message(user_id, f"आपको admin द्वारा {PREMIUM_DURATION[plan]//86400} दिनों के लिए premium दिया गया है।")
