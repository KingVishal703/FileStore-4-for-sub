import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait

from bot import Bot
from config import ADMINS, DISABLE_CHANNEL_BUTTON, AUTO_POST_CHANNEL
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(
    ['start', 'id', 'users', 'broadcast', 'batch', 'genlink', 'stats']
))
async def channel_post(client: Client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)

    # 1️⃣ Copy message to db_channel
    try:
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        await reply_text.edit_text(f"Something went Wrong..!\n{e}")
        return

    # 2️⃣ Generate unique link
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # 3️⃣ Create share button
    reply_markup = InlineKeyboardMarkup(
        [[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]]
    )
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    # 4️⃣ Use video thumbnail (without downloading full video)
    thumb_file_id = None
    try:
        if message.video and message.video.thumbs:
            # Telegram automatically provides File ID of thumbnail
            thumb_file_id = message.video.thumbs[-1].file_id  # highest quality thumbnail
        elif message.photo:
            thumb_file_id = message.photo.file_id
    except Exception as e:
        print("Thumbnail fetch failed:", e)
        thumb_file_id = None

    # 5️⃣ Auto post to channel
    try:
        if thumb_file_id:
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=thumb_file_id,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
        else:
            await client.send_message(
                chat_id=AUTO_POST_CHANNEL,
                text=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup,
                disable_web_page_preview=True
            )
    except Exception as e:
        print("Auto post failed:", e)

    # 6️⃣ Edit buttons on copied message if needed
    try:
        if not DISABLE_CHANNEL_BUTTON and (post_message.reply_markup != reply_markup):
            await post_message.edit_reply_markup(reply_markup)
    except Exception:
        pass
