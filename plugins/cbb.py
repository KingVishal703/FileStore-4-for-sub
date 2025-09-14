#
# Copyright (C) 2025 by Codeflix-Bots
# Released under MIT License
#

from pyrogram import filters
from bot import Bot
from config import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import (
    add_user, del_user, full_userbase, present_user,
    db_set_pending_plan, db_get_pending_plan, db_clear_pending_plan, db_set_premium_expiry
)
from time import time


# ---------- Plans Keyboard ----------
plans_keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton("₹10 - 7 दिन", callback_data="plan_10")],
    [InlineKeyboardButton("₹30 - 30 दिन", callback_data="plan_30")],
    [InlineKeyboardButton("₹60 - 90 दिन", callback_data="plan_60")]
])


# ---------- Main Callback Handler ----------
@Bot.on_callback_query()
async def callback_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id

    # --- Help / About / Start / Close ---
    if data == "help":
        await query.message.edit_text(
            text=HELP_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                    InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')
                ]]
            )
        )

    elif data == "about":
        await query.message.edit_text(
            text=ABOUT_TXT.format(first=query.from_user.first_name),
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                    InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')
                ]]
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

    # --- Plan Selection ---
    elif data == "choose_plan":
        await query.message.edit_text("प्लान चुनें:", reply_markup=plans_keyboard)

    elif data.startswith("plan_"):
        plan = data.split("_")[1]
        await db_set_pending_plan(user_id, plan)

        text = (
            f"आपने ₹{plan} वाला प्लान चुना है। कृपया नीचे दिए गए UPI ID या QR Code से payment करें:\n\n"
            f"💳 UPI ID: <code>{UPI_ID}</code>\n"
            f"🖼 QR Code: {QR_CODE_URL}\n\n"
            "Payment करने के बाद नीचे 'Payment Confirm' बटन दबाएं।"
        )
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("✅ Payment Confirm", callback_data=f"user_confirm_{plan}")],
            [InlineKeyboardButton("🔙 Back", callback_data="choose_plan")]
        ])
        await query.message.edit_text(text, reply_markup=buttons)

    elif data.startswith("user_confirm_"):
        await query.message.edit_text("कृपया अपने payment का screenshot या UTR ID भेजें, जिसे admin verify करेंगे।")

    elif data == "back_to_plan":
        await query.message.edit_text("प्लान चुनें:", reply_markup=plans_keyboard)

    # --- Admin Confirm / Reject ---
    elif data.startswith("confirm_") or data.startswith("reject_"):
        target_user = int(data.split("_")[1])

        if data.startswith("confirm_"):
            plan = await db_get_pending_plan(target_user)
            if not plan:
                await query.answer("User का कोई pending plan नहीं है।", show_alert=True)
                return

            expires = int(time()) + PREMIUM_DURATION.get(plan, 7 * 86400)
            await db_set_premium_expiry(target_user, expires)
            await db_clear_pending_plan(target_user)

            await query.answer("✅ User का प्रीमियम कन्फर्म हो गया!", show_alert=True)
            await query.edit_message_reply_markup(None)
            await client.send_message(
                target_user,
                f"🎉 आपका प्रीमियम सक्रिय कर दिया गया है {PREMIUM_DURATION.get(plan)//86400} दिनों के लिए।"
            )

        elif data.startswith("reject_"):
            await db_clear_pending_plan(target_user)
            await query.answer("❌ Payment proof reject कर दिया गया।", show_alert=True)
            await query.edit_message_reply_markup(None)
            await client.send_message(
                target_user,
                "❌ आपका भुगतान सत्यापित नहीं हो सका है। कृपया पुनः प्रयास करें।"
            )


# ---------- Payment Proof Handler ----------
@Bot.on_message(filters.private & filters.text)
async def payment_proof_handler(client, message):
    user_id = message.from_user.id
    plan = await db_get_pending_plan(user_id)

    if not plan:
        await message.reply("कृपया पहले प्रीमियम प्लान चुनें।")
        return

    caption = f"📩 Payment proof from user: <code>{user_id}</code>\n💰 Plan: ₹{plan}"
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Confirm ✅", callback_data=f"confirm_{user_id}")],
        [InlineKeyboardButton("Reject ❌", callback_data=f"reject_{user_id}")]
    ])

    if message.photo:
        await client.send_photo(
            ADMIN_ID,
            photo=message.photo.file_id,
            caption=caption,
            reply_markup=buttons
        )
    else:
        full_caption = f"{caption}\n\n📝 Message:\n{message.text}"
        await client.send_message(
            ADMIN_ID,
            full_caption,
            reply_markup=buttons
        )

    await message.reply("✅ Payment proof admin को भेज दिया गया है। कृपया response का इंतजार करें।")
