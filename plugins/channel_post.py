# (©)Codexbotz

import asyncio
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, RPCError
from bot import Bot
from config import ADMINS, DISABLE_CHANNEL_BUTTON, AUTO_POST_CHANNEL
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    # Copy message to the bot's DB channel
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print("Copy failed:", e)
        await reply_text.edit_text("Something went wrong while copying the message!")
        return
    
    # Generate unique link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Edit reply text only if content/markup changed
    try:
        new_text = f"<b>Here is your link</b>\n\n{link}"
        if reply_text.text != new_text or reply_text.reply_markup != reply_markup:
            await reply_text.edit(
                text=new_text,
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
    except RPCError as e:
        print("Reply edit skipped:", e)

    # Auto post to channel with thumbnail
    try:
        # Use video thumbnail if exists
        thumbnail = None
        if message.media and getattr(message, "video", None) and message.video.thumbs:
            thumbnail = message.video.thumbs[0].file_id

        # Send video/photo to AUTO_POST_CHANNEL
        if getattr(message, "video", None):
            await client.send_video(
                chat_id=AUTO_POST_CHANNEL,
                video=message.video.file_id,
                thumb=thumbnail,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
        elif getattr(message, "photo", None):
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=message.photo.file_id,
                caption=f"🎬 <b>New Photo Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
        else:
            # fallback image if media type unknown
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo="https://telegra.ph/file/0c6f1a29e9d92b7d8e8a1.jpg",
                caption=f"🎬 <b>New Media Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )

    except Exception as e:
        print("Auto post failed:", e)

    # Edit post_message reply_markup only if changed
    try:
        if not DISABLE_CHANNEL_BUTTON and post_message.reply_markup != reply_markup:
            await post_message.edit_reply_markup(reply_markup)
    except Exception:
        pass
