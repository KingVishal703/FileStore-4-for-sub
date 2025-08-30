#(©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, DISABLE_CHANNEL_BUTTON, AUTO_POST_CHANNEL
from helper_func import encode
import os

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    try:
        # copy video to DB channel
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print("DB copy error:", e)
        return await reply_text.edit_text("Something went Wrong..!")

    # generate sharable link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )

    await reply_text.edit(
        f"<b>Here is your link</b>\n\n{link}",
        reply_markup=reply_markup,
        disable_web_page_preview=True
    )

    # try to auto-post in channel
    try:
        thumb_path = None
        if message.video and message.video.thumbs:   # agar video ka thumbnail available hai
            thumb_path = await message.download(file_name="thumb.jpg")
        
        if thumb_path:
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=thumb_path,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
            os.remove(thumb_path)  # clean up temp file
        else:
            await client.send_message(
                chat_id=AUTO_POST_CHANNEL,
                text=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
    except Exception as e:
        print("Auto post failed:", e)

    if not DISABLE_CHANNEL_BUTTON:
        await post_message.edit_reply_markup(reply_markup)
