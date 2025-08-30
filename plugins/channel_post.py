from io import BytesIO
from pyrogram import filters, Client
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from config import ADMINS, AUTO_POST_CHANNEL, DISABLE_CHANNEL_BUTTON
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start','id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message: Message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    # Generate link for video
    converted_id = message.id * 123456  # simple unique multiplier
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    try:
        # Thumbnail handling
        if message.video and message.video.thumbs:
            thumb_file = await client.download_media(message.video.thumbs[0].file_id, in_memory=True)
            thumb_bytes = BytesIO(thumb_file)
            thumb_bytes.name = "thumbnail.jpg"
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo=thumb_bytes,
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
        else:
            # Default image if no thumbnail
            await client.send_photo(
                chat_id=AUTO_POST_CHANNEL,
                photo="https://telegra.ph/file/0c6f1a29e9d92b7d8e8a1.jpg",
                caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
                reply_markup=reply_markup
            )
    except Exception as e:
        print("Auto post failed:", e)
