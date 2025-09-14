#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import add_user, del_user, full_userbase, present_user

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "help":
        await query.message.edit_text(
            text=HELP_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                        InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')
                    ]
                ]
            )
        )
    elif data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
                ]
            )
        )
    elif data == "start":
        await query.message.edit_text(
            text=START_MSG.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                 InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
            ])
        )
    
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass



from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database import db_set_pending_plan
from config import PREMIUM_DURATION, UPI_ID, QR_CODE_URL, ADMIN_ID

plans_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("₹10 - 7 दिन", callback_data="plan_10")],
    [InlineKeyboardButton("₹30 - 30 दिन", callback_data="plan_30")],
    [InlineKeyboardButton("₹60 - 90 दिन", callback_data="plan_60")]
])

@Bot.on_callback_query()
async def cb_handler(client, query):
    data = query.data
    user_id = query.from_user.id

    if data == "choose_plan":
        await query.message.edit_text(
            "प्लान चुनें:",
            reply_markup=plans_keyboard
        )

    elif data.startswith("plan_"):
        plan = data.split("_")[1]
        await db_set_pending_plan(user_id, plan)

        text = (
            f"आपने ₹{plan} वाला प्लान चुना है। कृपया नीचे दिए गए UPI ID या QR Code से payment करें:

"
            f"UPI ID: `{UPI_ID}`

"
            f"या QR Code देखें:
"
            f"{QR_CODE_URL}

"
            "Payment करने के बाद नीचे 'Payment Confirm' बटन दबाएं।"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Payment Confirm", callback_data=f"confirm_{plan}")],
            [InlineKeyboardButton("Back", callback_data="choose_plan")]
        ])
        await query.message.edit_text(text, reply_markup=buttons)

    elif data.startswith("confirm_"):
        plan = data.split("_")[1]
        await query.message.edit_text("कृपया अपने payment का screenshot या UTR ID भेजें, जिसे admin verify करेंगे।")

    elif data == "back_to_plan":
        await query.message.edit_text("प्लान चुनें:", reply_markup=plans_keyboard)
