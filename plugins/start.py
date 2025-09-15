# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport

import asyncio
import random
import time
import string as rohit
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated
from bot import Bot
from config import *
from helper_func import *
from database.database import *

FILE_AUTO_DELETE = TIME
TUT_VID = str(TUT_VID)

#------------------ MAIN /start Handler -------------------
@Bot.on_message(filters.command('start') & filters.private)
async def start_command(client: Client, message: Message):
    user_id = message.from_user.id
    text = message.text or ""

    #------ Add User --------
    if not await present_user(user_id):
        try:
            await add_user(user_id)
        except:
            pass

    # Agar user ne simple /start likha hai (without link) → Welcome message
    if len(text.split()) == 1:
        buttons = [
            [InlineKeyboardButton("ʜᴇʟᴘ", callback_data="help"),
             InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data="about")],
            [InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="choose_plan")]
        ]
        return await message.reply_photo(
            photo=START_PIC,
            caption=START_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=('@' + message.from_user.username) if message.from_user.username else "",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Yaha se file link case handle hoga
    #---------------- Force Subscription Check -----------------
    try:
        await client.get_chat_member(FORCE_SUB_CHANNEL1, user_id)
        await client.get_chat_member(FORCE_SUB_CHANNEL2, user_id)
        await client.get_chat_member(FORCE_SUB_CHANNEL3, user_id)
        await client.get_chat_member(FORCE_SUB_CHANNEL4, user_id)
    except Exception:
        buttons = []
        for ch_num, inv_link in enumerate([
            getattr(client, "invitelink1", ""),
            getattr(client, "invitelink2", ""),
            getattr(client, "invitelink3", ""),
            getattr(client, "invitelink4", "")
        ], 1):
            if inv_link:
                buttons.append([InlineKeyboardButton(f"Join Channel {ch_num}", url=inv_link)])
        reload_btn = [InlineKeyboardButton("Reload 🔄", url=f"https://t.me/{client.username}?start={text.split()[1]}")]
        buttons.append(reload_btn)
        return await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username=('@' + message.from_user.username) if message.from_user.username else "",
                mention=message.from_user.mention,
                id=message.from_user.id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    #---------------- Verify / Premium Check -----------------
    verify_status = await get_verify_status(user_id)
    premium_expiry = await db_get_premium_expiry(user_id)
    now = int(time.time())
    verified = verify_status.get("is_verified", False) or (premium_expiry > now)

    # Agar user verified/premium nahi hai
    if not verified:
        token = ''.join(random.choices(rohit.ascii_letters + rohit.digits, k=10))
        await update_verify_status(user_id, verify_token=token, is_verified=False, verified_time=0, link="")
        link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f'https://telegram.dog/{client.username}?start=verify_{token}')
        buttons = [
            [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ •", url=link)],
            [InlineKeyboardButton("• ᴛᴜᴛᴏʀɪᴀʟ •", url=TUT_VID)],
            [InlineKeyboardButton("• ʙᴜʏ ᴘʀᴇᴍɪᴜᴍ •", callback_data="choose_plan")]
        ]
        return await message.reply_photo(
            photo=START_PIC,
            caption="⚠️ You are not verified!\n\nPlease verify yourself or buy premium to continue using the bot.",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    #---------------- File Handling (agar verified/premium hai) -----------------
    try:
        base64_string = text.split(" ", 1)[1]
        string = await decode(base64_string)
        argument = string.split("-")
        ids = []

        if len(argument) == 3:
            start = int(int(argument[1]) / abs(client.db_channel.id))
            end = int(int(argument[2]) / abs(client.db_channel.id))
            ids = range(start, end + 1) if start <= end else list(range(start, end - 1, -1))
        elif len(argument) == 2:
            ids = [int(int(argument[1]) / abs(client.db_channel.id))]

        temp_msg = await message.reply("<b>Please wait...</b>")
        messages = await get_messages(client, ids)
        await temp_msg.delete()

        for msg in messages:
            custom_text = "\n<b>📤 join mein channel 👉 @V_Anime_Hindi</b>"
            if msg.video and msg.video.file_name:
                caption = msg.video.file_name + custom_text
            elif msg.caption:
                caption = msg.caption + custom_text
            else:
                caption = custom_text

            reply_markup = msg.reply_markup if DISABLE_CHANNEL_BUTTON else None
            await msg.copy(
                chat_id=user_id,
                caption=caption,
                parse_mode=ParseMode.HTML,
                reply_markup=reply_markup,
                protect_content=PROTECT_CONTENT,
            )

    except Exception as e:
        print(f"Error while sending file: {e}")
        await message.reply("❌ Something went wrong while fetching your file.")
    
                        

#------ User Listing -----
@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text="<b>Working....</b>")
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

#------ Broadcast -----
@Bot.on_message(filters.command('broadcast') & filters.private & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = successful = blocked = deleted = unsuccessful = 0
        pls_wait = await message.reply("<i>ʙʀᴏᴀᴅᴄᴀꜱᴛ ᴘʀᴏᴄᴇꜱꜱɪɴɢ....</i>")
        for chat_id in query:
            try:
                await broadcast_msg.copy(chat_id)
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                await broadcast_msg.copy(chat_id)
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ...</u>
Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)
    else:
        msg = await message.reply("<code>Use this command as a reply to any telegram message without any spaces.</code>")
        await asyncio.sleep(8)
        await msg.delete()

#------ Broadcast with Auto-Delete -----
@Bot.on_message(filters.command('dbroadcast') & filters.private & filters.user(ADMINS))
async def delete_broadcast(client: Bot, message: Message):
    if message.reply_to_message:
        try:
            duration = int(message.command[1])
        except (IndexError, ValueError):
            await message.reply("<b>Please provide a valid duration in seconds.</b> Usage: /dbroadcast {duration}")
            return

        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = successful = blocked = deleted = unsuccessful = 0
        pls_wait = await message.reply("<i>Broadcast with auto-delete processing....</i>")
        for chat_id in query:
            try:
                sent_msg = await broadcast_msg.copy(chat_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                sent_msg = await broadcast_msg.copy(chat_id)
                await asyncio.sleep(duration)
                await sent_msg.delete()
                successful += 1
            except UserIsBlocked:
                await del_user(chat_id)
                blocked += 1
            except InputUserDeactivated:
                await del_user(chat_id)
                deleted += 1
            except:
                unsuccessful += 1
            total += 1
        status = (f"<b><u>Broadcast with Auto-Delete...</u>\n"
                  f"Total Users: <code>{total}</code>\n"
                  f"Successful: <code>{successful}</code>\n"
                  f"Blocked Users: <code>{blocked}</code>\n"
                  f"Deleted Accounts: <code>{deleted}</code>\n"
                  f"Unsuccessful: <code>{unsuccessful}</code></b>")
        return await pls_wait.edit(status)
    else:
        msg = await message.reply("Please reply to a message to broadcast it with auto-delete.")
        await asyncio.sleep(8)
        await msg.delete()

#------ Admin Set Premium -----
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
    expires = int(time.time()) + PREMIUM_DURATION[plan]
    await db_set_premium_expiry(user_id, expires)
    await message.reply(f"User {user_id} को {PREMIUM_DURATION[plan]//86400} दिनों के लिए premium दे दिया गया है।")
    await client.send_message(user_id, f"आपको admin द्वारा {PREMIUM_DURATION[plan]//86400} दिनों के लिए premium दिया गया है।")
