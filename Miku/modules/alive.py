import asyncio
import random
from sys import version_info
from pyrogram import __version__ as pver
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Miku import BOT_NAME, BOT_USERNAME, app
from config import SUPPORT_CHAT, UPDATES_CHANNEL, OWNER_ID
from .pyro.decorators import control_user, command

ALIVE_PIC = [
    "https://telegra.ph/file/699acc7d35ae0f6395c3b.jpg",
    "https://telegra.ph/file/f1e9b94decb547cb45cab.jpg",
    "https://telegra.ph/file/c5b6c0a3a6832efc08e5b.jpg",
    "https://telegra.ph/file/1dbcdedfc78d0318a288b.jpg",
    "https://telegra.ph/file/ac522b519f77a1054e9e9.jpg"
]
ALIVE_TEXT = """**Hey I Am {}
 ━━━━━━━━━━━━━━━━━━━
 » My Love : {}
 » ★ Artificial Robot To Manage Groups
 » ★ Pyrogram : {}
 » Thanks For Adding Me Here ❤️
 ━━━━━━━━━━━━━━━━━━━**"""

btn = [
    [
        InlineKeyboardButton(text="Updates 💻", url=f"https://t.me/{UPDATES_CHANNEL}"),
        InlineKeyboardButton(text="Support 🏥", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        InlineKeyboardButton(
            text="🖤 System Stats 🖤",
            callback_data="Friday_st",
        ),
    ],
    [
        InlineKeyboardButton(
            text="➕ Add Me To Your Group ➕",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

@Client.on_message(command(commands=("alive")))
@Client.on_message(filters.regex("awake"))
@control_user()
async def restart(_, message):
    mention = (await _.get_users(int(OWNER_ID))).mention
    
    accha = await message.reply("⚡")
    await asyncio.sleep(1)
    await accha.edit("**Awakening...**")
    await accha.delete()
    await asyncio.sleep(0.1)
    await message.reply_photo(
        random.choice(ALIVE_PIC),
        caption=ALIVE_TEXT.format(BOT_NAME, mention, pver),
        reply_markup=InlineKeyboardMarkup(btn),
    )
