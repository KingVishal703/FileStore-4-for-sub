# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#

import asyncio
import os
import random
import sys
import time
import string
import string as rohit
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
from pyrogram.errors import FloodWait, UserIsBlocked, InputUsrDeactivated, UserNotParticipant
from bot import Bot
from config import *
from helper_func import *
from database.database import *

# File auto-delete time in seconds (Set your desired time in seconds here)
FILE_AUTO_DELETE = TIME  # Example: 3600 seconds (1 hour)
TUT_VID = f"{TUT_VID}"

@Bot.on_message(filters.command("start") & filters.private)
async def start_handler(client: Client, message: Message):
    id = message.from_user.id

    # Force subscribe check
    if not await subscribed1(client, message) or not await subscribed2(client, message) or not await subscribed3(client, message) or not await subscribed4(client, message):
        buttons = []
        if FORCE_SUB_CHANNEL1: buttons.append([InlineKeyboardButton("• ᴊᴏɪɴ ᴄʜ1 •", url=client.invitelink1)])
        if FORCE_SUB_CHANNEL2: buttons.append([InlineKeyboardButton("• ᴊᴏɪɴ ᴄʜ2 •", url=client.invitelink2)])
        if FORCE_SUB_CHANNEL3: buttons.append([InlineKeyboardButton("• ᴊᴏɪɴ ᴄʜ3 •", url=client.invitelink3)])
        if FORCE_SUB_CHANNEL4: buttons.append([InlineKeyboardButton("• ᴊᴏɪɴ ᴄʜ4 •", url=client.invitelink4)])
        try:
            if len(message.command) > 1:
                buttons.append([InlineKeyboardButton("ʀᴇʟᴏᴀᴅ", url=f"https://t.me/{client.username}?start={message.command[1]}")])
        except:
            pass
        return await message.reply_photo(
            photo=FORCE_PIC,
            caption=FORCE_MSG.format(
                first=message.from_user.first_name,
                last=message.from_user.last_name,
                username='@' + message.from_user.username if message.from_user.username else None,
                mention=message.from_user.mention,
                id=id
            ),
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # Add user to DB
    if not await present_user(id):
        try: await add_user(id)
        except: pass

    # Token Verification
    if id in ADMINS:
        verify_status = {'is_verified': True, 'verify_token': None, 'verified_time': time.time(), 'link': ""}
    else:
        verify_status = await get_verify_status(id)
        if TOKEN:
            if verify_status['is_verified'] and VERIFY_EXPIRE < (time.time() - verify_status['verified_time']):
                await update_verify_status(id, is_verified=False)

            if "verify_" in message.text:
                _, token = message.text.split("_", 1)
                if verify_status['verify_token'] != token:
                    return await message.reply("Invalid or expired token. Use /start to retry.")
                await update_verify_status(id, is_verified=True, verified_time=time.time())
                return await message.reply(
                    f"✅ Token verified successfully!\nAccess granted for {get_exp_time(VERIFY_EXPIRE)}.",
                    quote=True
                )

            if not verify_status['is_verified']:
                token = ''.join(random.choices(rohit.ascii_letters + rohit.digits, k=10))
                await update_verify_status(id, verify_token=token, link="")
                link = await get_shortlink(SHORTLINK_URL, SHORTLINK_API, f"https://telegram.dog/{client.username}?start=verify_{token}")
                btn = [
                    [InlineKeyboardButton("• ᴏᴘᴇɴ ʟɪɴᴋ •", url=link)],
                    [InlineKeyboardButton("• ᴛᴜᴛᴏʀɪᴀʟ •", url=TUT_VID)],
                ]
                return await message.reply(
                    f"<b>Your token expired!</b>\n\n🔁 Please verify again to access files.\n\n⏳ Validity: {get_exp_time(VERIFY_EXPIRE)}",
                    reply_markup=InlineKeyboardMarkup(btn)
                )

    # If start contains encoded file ID
    if len(message.text) > 7:
        try:
            base64_string = message.text.split(" ", 1)[1]
            decoded = await decode(base64_string)
            parts = decoded.split("-")

            if len(parts) == 3:
                start = int(int(parts[1]) / abs(client.db_channel.id))
                end = int(int(parts[2]) / abs(client.db_channel.id))
                ids = range(start, end + 1)
            else:
                ids = [int(int(parts[1]) / abs(client.db_channel.id))]
        except Exception as e:
            return await message.reply("❌ Error decoding file ID.")

        temp = await message.reply("<b>🔄 Please wait...</b>")
        try:
            msgs = await get_messages(client, ids)
        except:
            return await message.reply("❌ Error fetching message.")
        finally:
            await temp.delete()

        sent_msgs = []
        for msg in msgs:
            caption = msg.video.file_name + "\n\n<b>📤 Uploaded by @Hotvking</b>" if msg.video else ""
            try:
                copy = await msg.copy(chat_id=id, caption=caption, parse_mode=ParseMode.HTML, protect_content=PROTECT_CONTENT)
                sent_msgs.append(copy)
            except FloodWait as e:
                await asyncio.sleep(e.x)
                copy = await msg.copy(chat_id=id, caption=caption, parse_mode=ParseMode.HTML, protect_content=PROTECT_CONTENT)
                sent_msgs.append(copy)
            except:
                pass

        if FILE_AUTO_DELETE > 0:
            notice = await message.reply(
                f"<b>🕐 File will be auto-deleted in {get_exp_time(FILE_AUTO_DELETE)}. Save it before that!</b>"
            )
            await asyncio.sleep(FILE_AUTO_DELETE)
            for sm in sent_msgs:
                try: await sm.delete()
                except: pass
            try:
                reload_url = f"https://t.me/{client.username}?start={message.command[1]}"
                await notice.edit(
                    "<b>✅ File auto-deleted!\nClick below to get it again 👇</b>",
                    reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ɢᴇᴛ ᴀɢᴀɪɴ", url=reload_url)]])
                )
            except:
                pass
        return

    # Default welcome message
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("• ᴍᴏʀᴇ ᴄʜᴀɴɴᴇʟs •", url="https://t.me/All_One_Channel")],
        [InlineKeyboardButton("• ᴀʙᴏᴜᴛ", callback_data="about"), InlineKeyboardButton("ʜᴇʟᴘ •", callback_data="help")]
    ])
    await message.reply_photo(
        photo=START_PIC,
        caption=START_MSG.format(
            first=message.from_user.first_name,
            last=message.from_user.last_name,
            username='@' + message.from_user.username if message.from_user.username else None,
            mention=message.from_user.mention,
            id=id
        ),
        reply_markup=reply_markup
                    )


#=====================================================================================##

WAIT_MSG = "<b>Working....</b>"

REPLY_ERROR = "<code>Use this command as a reply to any telegram message without any spaces.</code>"

#=====================================================================================##


@Bot.on_message(filters.command('users') & filters.private & filters.user(ADMINS))
async def get_users(client: Bot, message: Message):
    msg = await client.send_message(chat_id=message.chat.id, text=WAIT_MSG)
    users = await full_userbase()
    await msg.edit(f"{len(users)} users are using this bot")

@Bot.on_message(filters.private & filters.command('broadcast') & filters.user(ADMINS))
async def send_text(client: Bot, message: Message):
    if message.reply_to_message:
        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

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
                pass
            total += 1

        status = f"""<b><u>ʙʀᴏᴀᴅᴄᴀꜱᴛ...</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply(REPLY_ERROR)
        await asyncio.sleep(8)
        await msg.delete()

# broadcast with auto-del

@Bot.on_message(filters.private & filters.command('dbroadcast') & filters.user(ADMINS))
async def delete_broadcast(client: Bot, message: Message):
    if message.reply_to_message:
        try:
            duration = int(message.command[1])  # Get the duration in seconds
        except (IndexError, ValueError):
            await message.reply("<b>Please provide a valid duration in seconds.</b> Usage: /dbroadcast {duration}")
            return

        query = await full_userbase()
        broadcast_msg = message.reply_to_message
        total = 0
        successful = 0
        blocked = 0
        deleted = 0
        unsuccessful = 0

        pls_wait = await message.reply("<i>Broadcast with auto-delete processing....</i>")
        for chat_id in query:
            try:
                sent_msg = await broadcast_msg.copy(chat_id)
                await asyncio.sleep(duration)  # Wait for the specified duration
                await sent_msg.delete()  # Delete the message after the duration
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
                pass
            total += 1

        status = f"""<b><u>Broadcast with Auto-Delete...</u>

Total Users: <code>{total}</code>
Successful: <code>{successful}</code>
Blocked Users: <code>{blocked}</code>
Deleted Accounts: <code>{deleted}</code>
Unsuccessful: <code>{unsuccessful}</code></b>"""

        return await pls_wait.edit(status)

    else:
        msg = await message.reply("Please reply to a message to broadcast it with auto-delete.")
        await asyncio.sleep(8)
        await msg.delete()
