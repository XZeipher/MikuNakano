from Miku import app,BOT_ID,BOT_NAME
from config import SUPPORT_CHAT
from pyrogram import filters
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Miku.modules.pyro.status import user_admin
from .mongo.actions_db import *
from .pyro.decorators import control_user,command

@app.on_message(command(commands=["addaction","rmaction"]))
@control_user()
@user_admin
async def _mm(_, message):
    chat_id = message.chat.id
    check = await isEnbale(chat_id)
    if message.command[0] == "addaction":
        if check:
            return await message.reply_text("**Chat Actions Is Already Enabled In This Group.**")
        await add_action(chat_id)
        return await message.reply_text("**Enabled Chat Actions.**")
    if message.command[0] == "rmaction":
        if not check:
            return await message.reply_text("**Chat Actions Is Already Disabled In This Group.**")
        await rm_action(chat_id)
        return await message.reply_text("**Disabled Chat Actions.**")
    

btn = InlineKeyboardMarkup([[InlineKeyboardButton("Close ❌",callback_data="admin_close")]])
        
@app.on_chat_member_updated()
async def _cmu(_,cmu):
    chat_id = cmu.chat.id
    old_user = cmu.old_chat_member
    new_user = cmu.new_chat_member
    check = await isEnbale(chat_id)
    if not check:
        return
    if cmu.from_user.id == BOT_ID:
        return 
    try:
        if old_user.status == ChatMemberStatus.ADMINISTRATOR:
            if new_user.status == ChatMemberStatus.MEMBER:
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Demoted An Admin\n• Demoted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
        
        if old_user.status != ChatMemberStatus.ADMINISTRATOR and new_user.status == ChatMemberStatus.ADMINISTRATOR:  
            if not new_user.custom_title:      
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Promoted An User\n• Promoted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)         
            if new_user.custom_title:
                await _.send_message(chat_id,f"**{BOT_NAME}\n• Promoted An User\n• Promoted: {new_user.user.mention}\n• Title: {new_user.custom_title}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)  
          
        if old_user.status != ChatMemberStatus.RESTRICTED and new_user.status == ChatMemberStatus.RESTRICTED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• Muted An User\n• Muted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
        if old_user.status == ChatMemberStatus.RESTRICTED and new_user.status != ChatMemberStatus.RESTRICTED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• UnMuted An User\n• UnMuted: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)

        if old_user.status != ChatMemberStatus.BANNED and new_user.status == ChatMemberStatus.BANNED:
            await _.send_message(chat_id,f"**{BOT_NAME}\n• Banned An User\n• Banned: {new_user.user.mention}\n• Admin: {cmu.from_user.mention}**",reply_markup=btn)
    except Exception as e:
        pass

