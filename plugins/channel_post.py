# (©)Codexbotz

import asyncio
from io import BytesIO
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, AUTO_POST_CHANNEL, DISABLE_CHANNEL_BUTTON, DEFAULT_THUMBNAIL
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(
    ['start', 'id', 'users', 'broadcast', 'batch', 'genlink', 'stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)

    # --- Copy message to bot's DB channel ---
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went wrong..!")
        return

    # --- Generate link ---
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # Edit reply message
    try:
        await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)
    except:
        pass  # ignore MessageNotModified

    # --- Thumbnail handling ---
    thumbnail_bytes = None
    use_url = False

    if message.video:
        try:
            # Take the last thumbnail (usually highest resolution)
            if message.video.thumbs:
                thumb_file_path = await client.download_media(message.video.thumbs[-1].file_id)
                with open(thumb_file_path, "rb") as f:
                    thumbnail_bytes = BytesIO(f.read())
                    thumbnail_bytes.name = "thumbnail.jpg"
        except Exception as e:
            print("Thumbnail download failed:", e)
            thumbnail_bytes = None

    # If thumbnail not found, fallback to default
    if thumbnail_bytes is None:
        thumbnail_bytes = DEFAULT_THUMBNAIL  # URL
        use_url = True

    # --- Auto post to channel ---
    try:
        if use_url:
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=thumbnail_bytes,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
        else:
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=thumbnail_bytes,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
    except Exception as e:
        print("Auto post failed:", e)

    # Edit post message with button if enabled
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except:
            pass
