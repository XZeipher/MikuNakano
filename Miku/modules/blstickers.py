from Miku import app
from config import SUPREME_USERS as CHAD
from pyrogram import filters,enums,Client
from Miku.modules.pyro.status import user_admin,bot_admin
from Miku.modules.mongo.approve_db import approved_users,isApproved
from Miku.modules.mongo.blacklistSticker_db import *
from Miku.utils.filter_groups import blacklist_sticker_watcher


@Client.on_message(filters.command("addblsticker") & filters.group)
@user_admin
@bot_admin
async def _addstick(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if not replied :
        return await message.reply_text("**Reply to Sticker.**")
    if replied and replied.sticker:
        set_name = replied.sticker.set_name                    
    else:
        return await message.reply_text("**Reply to Sticker.**")
    check = await isBlSticker(chat_id,set_name)
    if check :
        return await message.reply_text("**This Sticker Is Already Blacklisted.**")
    await addBlSticker(chat_id,set_name)
    return await message.reply_text("**Added In Blacklist.**")  
        
    
@Client.on_message(filters.command("unblsticker") & filters.group)
@user_admin
async def _unaddstick(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    if not replied :
        return await message.reply_text("**Reply to Sticker.**")
    if replied and replied.sticker:
        set_name = replied.sticker.set_name                    
    else:
        return await message.reply_text("**Reply to Sticker.**")
    check = await isBlSticker(chat_id,set_name)
    if check:
        await unBlSticker(chat_id,set_name)
        return await message.reply_text("**Removed Sticker From Blacklist.**")
    return await message.reply_text("**This Sticker Isn't Blacklisted.**")
    
@Client.on_message(filters.sticker & filters.group, group=blacklist_sticker_watcher)
async def _delstick(_, message):
    chat_id = message.chat.id
    user = message.from_user
    list1 = await blacklisted_stickers(chat_id) 
    if not list1:
        return 
    xx = await _.get_chat_member(chat_id,user.id)        
    if (xx.privileges) or (user.id in SUPREME_USERS) or (await isApproved(chat_id,user.id)):
        return       
    set_name = message.sticker.set_name 
    try:      
        if set_name in list1:
            return await message.delete()
    except:
        pass
        
        
   

    
