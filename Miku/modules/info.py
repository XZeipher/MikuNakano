import random
import os
from Miku import app
from pyrogram import filters, enums
from unidecode import unidecode
from Miku.modules.pyro.status import user_admin, user_can_change_info
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from Miku.utils.info_data import miku
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery


async def check_temp(chat_id, pfp, name, chat_title, user_id, username):
    chat_title = unidecode(chat_title).upper()
    welpic = await miku(pfp=pfp, chat=chat_title, id=user_id)
    return welpic


@app.on_message(filters.command("info") & filters.group)
async def inform(_, msg):
    chat_id = msg.chat.id
    chat_title = msg.chat.title
    m = msg.from_user
    name = m.first_name
    username = m.username
    mention = m.mention
    user_id = m.id
    try:
        user_photo = m.photo.big_file_id
        pic = await _.download_media(m.photo.big_file_id, file_name=f"pp{user_id}.png")
    except AttributeError:
        pic = "./Miku/resources/profilepic.png"
        welpic = await check_temp(chat_id, pic, name, chat_title, user_id, username)
        await _.send_photo(chat_id, welpic)
        os.remove(welpic)
        if user_photo:
            os.remove(pic)
