import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import RPCError
from PIL import Image, ImageDraw, ImageFont
import io

from bot import Bot
from config import ADMINS, AUTO_POST_CHANNEL
from helper_func import encode

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message):
    reply_text = await message.reply_text("Processing your video...", quote=True)
    
    # Generate unique link for the video
    converted_id = message.message_id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    reply_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]
    ])

    # Extract thumbnail
    thumbnail = None
    try:
        if getattr(message, "video", None) and message.video.thumbs:
            # Get first thumbnail
            thumb_file_id = message.video.thumbs[0].file_id
            thumb_photo = await client.download_media(thumb_file_id)
            thumbnail = Image.open(thumb_photo)
        elif getattr(message, "photo", None):
            photo_file_id = message.photo.file_id
            photo_bytes = await client.download_media(photo_file_id)
            thumbnail = Image.open(photo_bytes)
    except Exception as e:
        print("Thumbnail extraction failed:", e)
    
    # fallback image
    if not thumbnail:
        thumbnail = Image.open(io.BytesIO(await client.download_media("https://telegra.ph/file/0c6f1a29e9d92b7d8e8a1.jpg")))

    # Add overlay text
    draw = ImageDraw.Draw(thumbnail)
    font = ImageFont.load_default()
    text = "🎬 New Video Uploaded!"
    width, height = thumbnail.size
    text_width, text_height = draw.textsize(text, font=font)
    draw.rectangle(((0, height - 30), (width, height)), fill=(0,0,0,128))
    draw.text(((width - text_width)//2, height - 25), text, font=font, fill="white")

    # Save to bytes
    image_bytes = io.BytesIO()
    thumbnail.save(image_bytes, format="PNG")
    image_bytes.seek(0)

    # Send image to auto-post channel
    try:
        await client.send_photo(
            chat_id=AUTO_POST_CHANNEL,
            photo=image_bytes,
            caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
            reply_markup=reply_markup
        )
    except Exception as e:
        print("Auto post failed:", e)

    await reply_text.edit(f"✅ Video processed!\n\nLink: {link}", reply_markup=reply_markup)
