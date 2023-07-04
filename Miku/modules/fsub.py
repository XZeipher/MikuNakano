from Miku import app,BOT_ID
from config import SUPREME_USERS as CHAD
from pyrogram import filters, enums 
from Miku.modules.pyro.status import (
    user_admin,
    bot_admin,
    bot_can_ban )
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery ,ChatPermissions
from pyrogram.errors import BadRequest 
from Miku.modules.mongo.approve_db import approved_users
from Miku.modules.mongo.fsub_db import *
from Miku.utils.filter_groups import forsesub_watcher


@app.on_message(filters.command("fsub") & filters.group)
@user_admin
@bot_admin
@bot_can_ban
async def _force_sub(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split()
    user = await _.get_chat_member(chat_id,user_id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("**You Need To Be Group Creator To Use This Command.**")           
    if "OFF".lower() in args:
         await fsub_off(chat_id)
         return await message.reply_text("**Force Sub Disabled.**")
    elif len(args) < 2:
        return await message.reply_text("**Provide Me A Channel ID or Username To Activate Force Sub.**")
    ch = args[1]
    try:
        channel = await _.get_chat(ch)
    except:
        return await message.reply_text("**Invalid Channel.**")
    try:
        await _.get_chat_member(channel.id,BOT_ID)
    except BadRequest :
        return await message.reply_text("**Make Me Admin On That Channel.**")
    member = await _.get_chat_member(channel.id,BOT_ID)
    if member.status != ChatMemberStatus.ADMINISTRATOR:
        return await message.reply_text("**Make Me Admin On That Channel.**")

    await fsub_on(chat_id,channel.id)
    await message.reply_text(f"**Force Sub Enabled In @{channel.username}.**")

@app.on_message(filters.command("fsub_stats") & filters.group)
@user_admin
async def _force_stat(_, message):
    chat_id = message.chat.id
    status = await fsub_stat(chat_id)
    if status is True:
        channel = await _.get_chat(await get_channel(chat_id)) 
        return await message.reply_text(f"**Force Sub Is Currently Enabled And Muting Those Users Who Haven't Joined {channel.username}**")
    return await message.reply_text("**Force Sub Is Currently Disabled In This Chat.**")

@app.on_message(group=forsesub_watcher)
async def _mute(_, message):
    chat_id = message.chat.id
    if not await fsub_stat(chat_id):
        return
    if not message.from_user:
        return
    SUPREME = await approved_users(chat_id) + CHAD    
    async for m in _.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        SUPREME.append(m.user.id)
    if message.from_user.id in SUPREME:
        return 
    ch = await get_channel(chat_id)
    channel = await _.get_chat(ch)
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ",url=f"t.me/{channel.username}"), InlineKeyboardButton("Unmute", callback_data=f"fsubuser_{message.from_user.id}")]])
    msg = f"**Hey {message.from_user.mention}\n Subscribe To This Channel {channel.username} In Order To Unmute Yourself.**"
    await message.reply_text(msg,reply_markup=buttons)
    try:
        await _.restrict_chat_member(chat_id, message.from_user.id, ChatPermissions(can_send_messages=False))
    except Exception as e:
        await message.reply_text(e)
  
@app.on_callback_query(filters.regex(pattern=r"fsubuser_(.*)"))
async def ok(_, query : CallbackQuery):
    muted_user = int(query.data.split("_")[1])
    chat_id = query.message.chat.id
    ch = await get_channel(chat_id)
    members = []
    async for member in _.get_chat_members(ch):
        members.append(member.user.id)
    user_id = query.from_user.id
    if user_id != muted_user:
        await _.answer_callback_query(query.id,text="It's Not For You.",show_alert=True)
        return   
              
    if not muted_user in members:
        return await _.answer_callback_query(query.id,text="You Have To Join The Channel To Get Unmuted.",show_alert=True)
    
    try :
        await _.unban_chat_member(chat_id,muted_user)
    except Exception as er:
        print(er)
    await query.message.delete()    




