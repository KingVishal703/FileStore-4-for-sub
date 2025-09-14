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
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(
            chat_id=client.db_channel.id,
            disable_notification=True
        )
    except Exception as e:
        print("DB copy failed:", e)
        await reply_text.edit_text("Something went wrong..!")
        return

    # --- Generate link ---
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # --- Extract video title (first 2 lines only) ---
    title_text = ""
    if message.caption:
        lines = message.caption.split("\n")
        title_text = "\n".join(lines[:2])  # only first 2 lines

    # --- Inline buttons ---
    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🎬 Watch Video", url=link)],
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # --- Thumbnail handling ---
    thumbnail_bytes = None
    use_url = False

    if message.video:
        try:
            if message.video.thumbs:
                # Highest resolution thumb
                thumb_file_path = await client.download_media(message.video.thumbs[-1].file_id)
                with open(thumb_file_path, "rb") as f:
                    thumbnail_bytes = BytesIO(f.read())
                    thumbnail_bytes.name = "thumbnail.jpg"
        except Exception as e:
            print("Thumbnail download failed:", e)
            thumbnail_bytes = None

    # If no thumbnail found, fallback to default URL
    if thumbnail_bytes is None:
        thumbnail_bytes = DEFAULT_THUMBNAIL  # URL
        use_url = True

    # --- Auto post to channel ---
    try:
        caption_text = (
            f"🎬 <b>New Video Uploaded!</b>\n\n{title_text}\n\n"
            f"🔗 <b>Link:</b> {link}\n\n"
            "⚠️ Bot ko bas ek bar verify kar lo aur pure din (24 hr) free mein videos ka maja lo\n\n"
            "✅ How to Verify Bot -"
        )

        await client.send_photo(
            chat_id=AUTO_POST_CHANNEL,
            photo=thumbnail_bytes,  # BytesIO ya URL dono chalega
            caption=caption_text,
            reply_markup=reply_markup,
            has_spoiler=True
        )

    except Exception as e:
        print("Auto post failed:", e)

    # --- Edit DB channel post with buttons (optional) ---
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except Exception as e:
            print("Edit buttons failed:", e)
