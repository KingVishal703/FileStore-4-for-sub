import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait, RPCError
from bot import Bot
from config import ADMINS, AUTO_POST_CHANNEL, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    # Generate unique link for the video
    converted_id = message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Edit reply with link
    try:
        await reply_text.edit(
            f"<b>Here is your link</b>\n\n{link}",
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    except RPCError:
        pass

    # Determine thumbnail
    thumbnail = None
    try:
        if getattr(message, "video", None) and message.video.thumbs:
            # Take first thumbnail from the video
            thumbnail = message.video.thumbs[0].file_id
        elif getattr(message, "photo", None):
            thumbnail = message.photo.file_id
    except Exception as e:
        print("Thumbnail extraction failed:", e)

    # fallback if no thumbnail found
    if not thumbnail:
        thumbnail = "https://telegra.ph/file/0c6f1a29e9d92b7d8e8a1.jpg"

    # Send image to auto-post channel
    try:
        await client.send_photo(
            chat_id=AUTO_POST_CHANNEL,
            photo=thumbnail,
            caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
            reply_markup=reply_markup
        )
    except Exception as e:
        print("Auto post failed:", e)
