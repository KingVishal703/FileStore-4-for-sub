# Don't Remove Credit @CodeFlix_Bots, @rohit_1888
# Ask Doubt on telegram @CodeflixSupport
#
# Copyright (C) 2025 by Codeflix-Bots@Github, < https://github.com/Codeflix-Bots >.
#
# This file is part of < https://github.com/Codeflix-Bots/FileStore > project,
# and is released under the MIT License.
# Please see < https://github.com/Codeflix-Bots/FileStore/blob/master/LICENSE >
#
# All rights reserved.
#


import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

#rohit_1888 on Tg

#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))
#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")
#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002392037274"))
# NAMA OWNER
OWNER = os.environ.get("OWNER", "@VKing7038")
#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", "5654093580"))
#Port
PORT = os.environ.get("PORT", "8030")
#Database
DB_URI = os.environ.get("MONGODB_URI", "mongodb+srv://timed29716:jzE1SqRNktFycmVo@cluster0.kco6t.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DATABASE_NAME", "Cluster0")

#Time in seconds for message delete, put 0 to never delete
TIME = int(os.environ.get("TIME", "2400"))


#force sub channel id, if you want enable force sub
FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "-1002160196977"))
#put 0 to disable
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "-1002394633791"))#put 0 to disable
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "-1002538118600"))#put 0 to disable
FORCE_SUB_CHANNEL4 = int(os.environ.get("FORCE_SUB_CHANNEL4", "-1002840913591"))#put 0 to disable

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "50"))

START_PIC = os.environ.get("START_PIC", "https://telegra.ph/file/ec17880d61180d3312d6a.jpg")
FORCE_PIC = os.environ.get("FORCE_PIC", "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg")

# Turn this feature on or off using True or False put value inside  ""
# TRUE for yes FALSE if no 
TOKEN = True if os.environ.get('TOKEN', "True") == "True" else False  #For Enable Token 

#TOKEN = False if os.environ.get('TOKEN', "FALSE") == 'FALSE' else False # For disable Token 

SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "linkcents.com")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "dcc4e31e2f3fd1cb80fbefb817bbe26cc46d7708")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 86400)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "False")
TUT_VID = os.environ.get("TUT_VID","https://t.me/hentai_Hanime_Update_Channel/72")


HELP_TXT = "<b><blockquote>ᴛʜɪs ɪs ᴀɴ ғɪʟᴇ ᴛᴏ ʟɪɴᴋ ʙᴏᴛ \n\n❏ ʙᴏᴛ ᴄᴏᴍᴍᴀɴᴅs\n├/start : sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ\n├/about : ᴏᴜʀ Iɴғᴏʀᴍᴀᴛɪᴏɴ\n└/help : ʜᴇʟᴘ ʀᴇʟᴀᴛᴇᴅ ʙᴏᴛ\n\n sɪᴍᴘʟʏ ᴄʟɪᴄᴋ ᴏɴ ʟɪɴᴋ ᴀɴᴅ sᴛᴀʀᴛ ᴛʜᴇ ʙᴏᴛ ᴊᴏɪɴ ʙᴏᴛʜ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ ᴛʜᴀᴛs ɪᴛ.....!\n\n ᴅᴇᴠᴇʟᴏᴘᴇᴅ ʙʏ <a href=https://t.me/+I70vh9FUF9NiY2E1>KingBots</a></blockquote></b>"

ABOUT_TXT = "<b><blockquote>◈ ᴄʀᴇᴀᴛᴏʀ: <a href=https://t.me/VKing7038>V W</a>\n◈ ꜰᴏᴜɴᴅᴇʀ ᴏꜰ : <a href=https://t.me/SpicyPulseHD>Spicy Pulse HD</a>\n◈ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/+292kQS3vAioyNDVl>ANIME WORLD</a>\n◈ sᴇʀɪᴇs ᴄʜᴀɴɴᴇʟ : <a href=https://t.me/>ᴡᴇʙsᴇʀɪᴇs ғʟɪx</a>\n◈ ᴅᴇᴠᴇʟᴏᴘᴇʀ : <a href=https://t.me/+-rDUKJoRiGYzOTI1></a></blockquote></b>"


START_MSG = os.environ.get("START_MESSAGE", "<b>ʜᴇʟʟᴏ {first}\n\n<blockquote> ɪ ᴀᴍ ғɪʟᴇ sᴛᴏʀᴇ ʙᴏᴛ, ɪ ᴄᴀɴ sᴛᴏʀᴇ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇs ɪɴ sᴘᴇᴄɪғɪᴇᴅ ᴄʜᴀɴɴᴇʟ ᴀɴᴅ ᴏᴛʜᴇʀ ᴜsᴇʀs ᴄᴀɴ ᴀᴄᴄᴇss ɪᴛ ғʀᴏᴍ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ.</blockquote></b>")
try:
    ADMINS=[5654093580]
    for x in (os.environ.get("ADMINS", "5654093580").split()):
        ADMINS.append(int(x))
except ValueError:
        raise Exception("Your Admins list does not contain valid integers.")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "ʜᴇʟʟᴏ {first}\n\n<b>ᴊᴏɪɴ ᴏᴜʀ ᴄʜᴀɴɴᴇʟs ᴀɴᴅ ᴛʜᴇɴ ᴄʟɪᴄᴋ ᴏɴ ʀᴇʟᴏᴀᴅ button ᴛᴏ ɢᴇᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛᴇᴅ ꜰɪʟᴇ.</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", "<b>• ʙʏ https://t.me/+gIQSxw-l1OYxOGY1</b>")

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "ʙᴀᴋᴋᴀ ! ʏᴏᴜ ᴀʀᴇ ɴᴏᴛ ᴍʏ ꜱᴇɴᴘᴀɪ!!"

ADMINS.append(OWNER_ID)
ADMINS.append(5654093580)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
   
