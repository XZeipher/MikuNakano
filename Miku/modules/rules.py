from Miku import app,BOT_USERNAME
from pyrogram import filters , Client
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton 
from pyrogram.errors import BadRequest 
from Miku.modules.pyro.status import user_admin,user_can_change_info 
from Miku.modules.mongo.rules_db import *


@Client.on_message(filters.command("setrules") & filters.group)
@user_admin
@user_can_change_info
async def _setrules(_, message):
    chat_id = message.chat.id
    check = await is_rules(chat_id) 
    if check:
        return await message.reply_text("**The Group Rules Has Already Been Set. Do /rmrules To Remove.**")
    if len(message.command) < 2:
        return await message.reply_text("**Give Me Some Text To Set As Group Rules**")
    rules = message.text.split(None,1)[1]
    await set_rules(chat_id,rules)
    await message.reply_text("**Successfully Set Rules Of This Group.**")


@Client.on_message(filters.command("rmrules") & filters.group)
@user_admin
@user_can_change_info
async def _rmrules(_, message):
    chat_id = message.chat.id
    check = await is_rules(chat_id) 
    if not check :
       await message.reply_text("**You Haven't Set Rules For This Group How Can I Remove It.**")
    await clear_rules(chat_id)
    return await message.reply_text("**Removed Group Rules Successfully.**")
    
@Client.on_message(filters.command("rules") & filters.group)
async def _getrules(_, message):
    chat_id = message.chat.id
    check = await is_rules(chat_id) 
    if not check :
       await message.reply_text("**You Haven't Set Rules For This Chat.**")
    btn = InlineKeyboardMarkup([[InlineKeyboardButton(text="**Rules**", url=f"t.me/{BOT_USERNAME}?start={chat_id}")]])                                    
    return await message.reply_text("**Click Below Button To See Chat Rules.**",reply_markup=btn)

async def send_rules(message, chat_id, from_pm=False):
    user_id = message.from_user.id
    try:
        chat = await app.get_chat(chat_id)
    except BadRequest :
        await app.send_message(
                user_id,
                "**The Rules For This Chat Hasn't Been Set Properly! Ask Admins To\nFix This.\nMaybe They Forgot The Hyphen In ID**")
            
    rules = await get_rules(chat_id)    
    text = f"**The Rules For {chat.title} Are :\b\n{rules}**"
    if from_pm and rules:
        await app.send_message(
            user_id, text,disable_web_page_preview=True
        )
    elif from_pm:
        await app.send_message(user_id,"**The Group Admins Haven't Set Any Rules Yet. \nThis Probably Doesn't Mean Its Lawless Though...!**")
    elif rules == None:
        await app.send_message( user_id,"**The Group Admins Haven't Set Any Rules Yet. \nThis Probably Doesn't Mean Its Lawless Though...!**")

            
