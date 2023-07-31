from Miku import app
from config import SUDO_USERS,DEV_USERS,SUPREME_USERS
from pyrogram import filters ,Client
from Miku.modules.pyro.extracting_id import extract_user_id
from Miku.modules.mongo.sudo_db import *
from Miku.modules.pyro.extracting_id import extract_user_id



@Client.on_message(filters.command("addmoon") & filters.user(DEV_USERS))
async def _addsudo(_, message):
    
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")

    sudo_users = await get_sudo_list()
    if user_id in sudo_users :
        return await message.reply_text("**User Already In Moon.**") 
    if  user_id in DEV_USERS:
        return await message.reply_text("**This Is An Sun User.**") 
    await add_sudo(user_id)
    if not user_id in SUDO_USERS:
        SUDO_USERS.append(user_id)
        SUPREME_USERS.append(user_id)
    return await message.reply_text("**Added In Moon Users.**")

@Client.on_message(filters.command("rmmoon") & filters.user(DEV_USERS))
async def _rmsudo(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")
    sudo_users = await get_sudo_list()
    if user_id not in sudo_users :
        return await message.reply_text("**This User Isn't Moon User.**")  
    await del_sudo(user_id)
    if user_id in SUDO_USERS:
        SUDO_USERS.remove(user_id)
        SUPREME_USERS.remove(user_id)
    return await message.reply_text("**Removed From Moon Users.**")  



@Client.on_message(filters.command("moonlist"))
async def _rmsudo(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return 
    if not SUDO_USERS:
        return await message.reply_text("**There Is No Moon Users.**")
    msg = "**♠ Moon Users ♠\n**"
    for m in set(SUDO_USERS):
        try:
            mention = (await _.get_users(int(m))).mention 
            msg += f"• {mention}\n"
        except Exception as e:
            print(e)
    await message.reply_text(msg)

@Client.on_message(filters.command("sunlist"))
async def _devlist(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return 
    msg = "**♠ Sun Users ♠\n**"
    for m in set(DEV_USERS):
        try:
            mention = (await _.get_users(m)).mention
            msg += f"• {mention}\n"
        except Exception as e:
            print(e)
    return await message.reply_text(msg)
 


