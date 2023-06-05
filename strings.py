from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Miku import BOT_NAME,BOT_USERNAME,app
from config import OWNER_ID, SUPPORT_CHAT,UPDATES_CHANNEL


PM_START_TEXT = """
────「 {} 」────
Hola! {} ,
I am an Anime themed advance group management bot with a lot of Sexy Features ✨
➖➖➖➖➖➖➖➖➖➖➖➖➖
‣ Uptime: {}
‣ Python: {}
‣ Pyrogram: {}
➖➖➖➖➖➖➖➖➖➖➖➖➖
‣ Keep Your Group Secure From Spammers by Adding me ✨
"""

SUPPORT_SEND_MSG = """
**Miku Nakano !**
**Python Version:** `{}`
**Pyrogram Version:** `{}`
**UpTime:** `{}`
"""

LOG_MSG = "Miku Starting 🍦🍦🍦🍦"

HELP_STRINGS = f"""**
Click on below buttons to access commands of {BOT_NAME}.**
"""

START_BUTTONS = [
    [
        InlineKeyboardButton(text="**Commands ⚙️**", callback_data="help_back"),
        InlineKeyboardButton(text="**Support 💕**", url=f"t.me/{SUPPORT_CHAT}")
    ], 
    [
       InlineKeyboardButton("**System Stats 🖥**",callback_data="Friday_st")
    ],
    [
        InlineKeyboardButton(
            text="**Add Me To Your Groups.**",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],     
]
GRP_START = [
    [
        InlineKeyboardButton(text="**Updates 💌**", url=f"t.me/{UPDATES_CHANNEL}"),
        InlineKeyboardButton(text="**Support 💕**", url=f"t.me/{SUPPORT_CHAT}")
    ], 
    [
       InlineKeyboardButton("**System Stats 🖥**",callback_data="Friday_st")
    ],
]
BACK_BTN = [[InlineKeyboardButton("🔙",callback_data="friday_back")]]
