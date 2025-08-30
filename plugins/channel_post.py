# (©)Codexbotz
import asyncio
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import FloodWait
from bot import Bot
from config import ADMINS, CHANNEL_ID, DISABLE_CHANNEL_BUTTON, AUTO_POST_CHANNEL, DEFAULT_IMAGE
from helper_func import encode
import os

@Bot.on_message(filters.private & filters.user(ADMINS) & ~filters.command(['start', 'id','users','broadcast','batch','genlink','stats']))
async def channel_post(client: Client, message):
    reply_text = await message.reply_text("Please Wait...!", quote=True)
    
    # 1️⃣ Thumbnail decide karna
    thumbnail = None
    if message.video and message.video.thumbs:
        # Pehla thumbnail
        thumbnail = await message.download(file_name="temp_thumb.jpg")
    elif message.photo:
        thumbnail = await message.download(file_name="temp_thumb.jpg")
    else:
        # Agar video/photo me thumbnail na ho to default image use karo
        thumbnail = DEFAULT_IMAGE

    try:
        # 2️⃣ Message copy karna db_channel me (sirf store karne ke liye)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except FloodWait as e:
        await asyncio.sleep(e.x)
        post_message = await message.copy(chat_id=client.db_channel.id, disable_notification=True)
    except Exception as e:
        print(e)
        await reply_text.edit_text("Something went wrong while storing the video..!")
        return

    # 3️⃣ Link generate karna
    converted_id = post_message.id * abs(client.db_channel.id)
    string = f"get-{converted_id}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"

    # 4️⃣ Share button
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])

    # 5️⃣ Reply user ko
    await reply_text.edit(f"<b>Here is your link</b>\n\n{link}", reply_markup=reply_markup, disable_web_page_preview=True)

    # 6️⃣ Auto post channel me sirf image + link
    try:
        await client.send_photo(
            chat_id=AUTO_POST_CHANNEL,
            photo=thumbnail,
            caption=f"🎬 <b>New Video Uploaded!</b>\n\n🔗 <b>Link:</b> {link}",
            reply_markup=reply_markup
        )
    except Exception as e:
        print("Auto post failed:", e)

    # 7️⃣ Edit reply markup (optional)
    if not DISABLE_CHANNEL_BUTTON:
        try:
            await post_message.edit_reply_markup(reply_markup)
        except:
            pass

    # 8️⃣ Temporary thumbnail file delete kar do
    if os.path.exists("temp_thumb.jpg"):
        os.remove("temp_thumb.jpg")
