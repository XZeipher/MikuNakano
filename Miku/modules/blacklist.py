from pyrogram import filters,enums
from Miku import app,db
from config import SUPREME_USERS,SUPREME_USERS as CHAD
from Miku.modules.mongo.approve_db import approved_users , isApproved
from Miku.modules.pyro.status import user_admin,user_can_del
from Miku.modules.mongo.blacklist_db import *
from Miku.utils.filter_groups import blacklist_watcher

@app.on_message(filters.command('addblacklist') & filters.group)
@user_admin
@user_can_del
async def _addblacklist(_, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("**Usage :** `/addblacklist <text>`")
    word = args[1].lower()
    check = await is_blacklisted(chat_id,word)
    if not check:
        await add_blacklist(chat_id,word)
        return await message.reply_text("**Blacklisted : {}.**".format(word))
    return await message.reply_text("**{} Is Already Blacklisted.**".format(word))

@app.on_message(filters.command('rmblacklist') & filters.group)
@user_admin
@user_can_del
async def _addblacklist(_, message):
    chat_id = message.chat.id
    args = message.text.split()
    if len(args) < 2:
        return await message.reply_text("**Usage :** `/rmblacklist <text>`")
    word = args[1].lower()
    check = await is_blacklisted(chat_id,word)
    print(check)
    if check:
        await rm_blacklist(chat_id,word)
        return await message.reply_text("**{} Removed From Blacklist.**".format(word))
    return await message.reply_text("**{} Isn't Blacklisted.**".format(word))


@app.on_message(filters.command("blacklists") & filters.group)
@user_admin
async def _get_blackisted(_, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    words = await get_blacklist(chat_id)
    if not words:
        return await message.reply_text(f"**There Is No Blacklisted Word In {chat_title}**")
    msg = f"**Blacklisted Words In {chat_title}**\n"
    for mm in words:
        msg += f"• `{mm}`\n"
    return await message.reply_text(msg)


@app.on_message(filters.command("unblacklistall") & filters.group)
async def _get_blackisted(_, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    user = message.from_user
    if user.status != enums.ChatMemberStatus.OWNER and user.id not in SUPREME_USERS:
        return await message.reply_text("**Only Owner Can Use This Command.**")
    words = await get_blacklist(chat_id)
    if not words:
        return await message.reply_text(f"**There Is No Blacklisted Words In {chat_title}**")
    await un_blacklistall(chat_id)
    return await message.reply_text("**UnBlacklisted All Words.**")
       
    

@app.on_message(filters.group, group=blacklist_watcher)
async def _delstick(_, message):
    chat_id = message.chat.id
    list1 = await get_blacklist(chat_id)
    
    if not list1:
        return 
    user = message.from_user
    xx = await _.get_chat_member(chat_id,message.from_user.id)        
    if (xx.privileges) or (user.id in SUPREME_USERS) or (await isApproved(chat_id,user.id)): 
        return    
    text = message.text or message.caption
    if text:
        word = message.text.split() if message.text else message.caption.split() 
        for _ in word:
            if _.lower() in list1:
                try:
                    await message.delete()
                except:
                    pass 
            
__help__ = """
**Blacklisted words can't be used in group by normal users.**

**Commands**

♠ `/addblacklist <text>` - add words in blacklist.
♠ `/rmblacklist - <text>` - remove blacklisted word.
♠ `/unblacklistall` - unblacklist all blacklisted words ( owner only )
♠ `/blacklists` - get all blacklisted words.
♠ `/blacklistchat` - blacklist any chat. ( dev only )
♠ `/blacklistchats` - get all blacklisted chats. ( dev only )

"""
__mod_name__ = "Blacklists"
