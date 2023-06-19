from Miku import app,BOT_ID
from config import SUPREME_USERS , SUPREME_USERS as CHAD
from pyrogram import filters, enums 
from pyrogram.errors import BadRequest 
from Miku.modules.pyro.status import (
    user_admin,
    user_has_permission,
    bot_admin,
    )
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Miku.modules.mongo.approve_db import approved_users,isApproved
from pyrogram.types import ChatPermissions
from Miku.modules.bans import until_date 
from Miku.modules.mongo.antiflood_db import *           
from .pyro.decorators import control_user,command
from .pyro.misc import remove_markdown
from Miku.utils.filter_groups import flood_watcher

@app.on_message(command(commands=("setflood")))
@control_user()
@user_admin
@bot_admin
async def _setflood(_, message):
    args = message.text.split()
    chat_id = message.chat.id
    chat_title = message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_restrict_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,message.from_user.id,"can_restrict_members",bot=False)
    if not bpermission:
        return await message.reply(btxt)   
    if not upermission:
        return await message.reply(utxt)
    usage = "**Usage : /setflood [on/off]**"
    if len(args) < 2:
        return await message.reply_text(usage)
    status = args[1].lower()
    if status in ["off","no","0"]:          
        await set_flood(chat_id=chat_id,flood_val=False)
        return await message.reply_text("**AntiFlood has been disabled in this chat.**")
    elif status.isdigit():
        value = int(status)
        if value < 3:
            return await message.reply_text("**Value Must be greater then 3.**")
        await set_flood(chat_id,value)
        return await message.reply_text(f"**AntiFlood Updated to {value}.**") 
    else:
        return await message.reply_text("**Not Valid Integer.**")
        
            
@app.on_message(command(commands=("setfloodmode")))
@control_user()
@user_admin
@bot_admin
async def _setfloodmode(_, message):   
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("Kick",callback_data="floodkick"),InlineKeyboardButton("Mute", callback_data="floodmute")],
    [InlineKeyboardButton("tmute",callback_data="floodtmute"), InlineKeyboardButton("tban",callback_data="floodtban")],
    [InlineKeyboardButton("Ban",callback_data="floodban")]
    ])
    return await message.reply_text("**Choose An AntiFlood Mode.**",reply_markup=btn)     
 
@app.on_message(command(commands=("flood"))) 
@control_user()
@user_admin
async def _flood(_, message):
    chat_id = message.chat.id
    status = await get_flood(chat_id)
    if status is False :
        return await message.reply_text("**I'm Not Controlling Flood In This Chat.**")
    flood_limit = await get_flood_limit(chat_id)
    flood_mode,until_date = await get_antiflood_settings(chat_id) 
    if flood_mode == 1:
        mode = "Ban"
    if flood_mode == 2:
        mode = "Mute"
    if flood_mode == 3:
        mode = "Kick"
    if flood_mode == 4:
        mode = "Temp Ban"
    if flood_mode == 5:
        mode = "Temp Mute"
 
    msg = f"""
**♠ Current AntiFlood Settings of {message.chat.title} ♠**

**Limit :** `{flood_limit}`
**Mode :** `{mode}`
**Time :** `{str(until_date)}`
"""  
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("❌ Close",callback_data="admin_close")]])
    return await message.reply_text(msg, reply_markup=btn)       
       
@app.on_callback_query(filters.regex(pattern=r"^(floodkick|floodmute|floodban)$"))
@control_user()
async def _anticq(_, query):
    chat_id = query.message.chat.id  
    user_id = query.from_user.id  
    chat_title = query.message.chat.title
    data = query.data    
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_restrict_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,query.from_user.id,"can_restrict_members",bot=False)
    if not upermission:
        return await query.answer(await remove_markdown(utxt),show_alert=True)   
    if not bpermission:
        return await query.answer(await remove_markdown(btxt),show_alert=True)
    if data == "floodban":
        type = "Ban"
        id = 1
    if data == "floodmute":
        type = "Mute"
        id = 2
    if data == "floodkick":
        type = "Kick" 
        id = 3
    await set_antiflood_mode(chat_id,id)             
    return await query.message.edit_text(f"**Flood type set to - {type}**")    

@app.on_callback_query(filters.regex(pattern=r"^(floodtmute|floodtban)$"))
@control_user()
async def _anticqm(_, query):
    chat_id = query.message.chat.id  
    user_id = query.from_user.id  
    data = query.data  
    chat_title = query.message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_restrict_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,query.from_user.id,"can_restrict_members",bot=False)
    if not upermission:
        return await query.answer(await remove_markdown(utxt),show_alert=True)   
    if not bpermission:
        return await query.answer(await remove_markdown(btxt),show_alert=True) 
    if data == "floodtban":
        mid = 4
    elif data == "floodtmute":
        mid = 5      
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("5 Minutes", callback_data =f"valtype_5m_id_{mid}"), InlineKeyboardButton("6 Hours",callback_data =f"valtype_6h_id_{mid}")],[InlineKeyboardButton("3 Days",callback_data =f"valtype_3d_id_{mid}"),InlineKeyboardButton("1 Week",callback_data =f"valtype_1w_id_{mid}")],[InlineKeyboardButton("Cancel", callback_data="admin_close")]])
    return await query.message.edit_text("**Choose Time**", reply_markup=btn) 

@app.on_callback_query(filters.regex(pattern=r"valtype_(.*)"))
@control_user()
async def _timecq(_, query):   
    chat_id = query.message.chat.id
    data = query.data.split("_")
    chat_title = query.message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_restrict_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,query.from_user.id,"can_restrict_members",bot=False)
    if not upermission:
        return await query.answer(await remove_markdown(utxt),show_alert=True)   
    if not bpermission:
        return await query.answer(await remove_markdown(btxt),show_alert=True)
    val = data[1]
    id = int(data[3])
    await set_antiflood_mode(chat_id,id,val)
    if id == 4:
        text = "**Sending More Messages Then Flood Limit Will Result In Ban.**"
    elif id == 5:
        text = "**Sending More Messages Then Flood Limit Will Result In Mute.**"
    return await query.message.edit_text(text)

# DICT = {}
# flood_limit = 0

# @pgram.on_message(
#     ~filters.service 
#     & ~filters.me
#     & filters.group
#     & filters.chat(-1001689743399),
#     group=11)
# async def _check_flood(_, message):
#     global DICT, flood_limit
#     chat_id = message.chat.id
#     user = message.from_user
#     print(DICT,flood_limit)
#     if not await get_flood(chat_id):
#         return
    
#     xx = await _.get_chat_member(chat_id, user.id)
#     if xx.privileges or user.id in SUPREME_USERS or await isApproved(chat_id, user.id):
#         flood_limit = 0
#         return
    
#     if chat_id not in DICT:
#         DICT[chat_id] = user.id
#         flood_limit = 1
#     elif DICT[chat_id] == user.id:
#         flood_limit += 1
#     else:
#         DICT[chat_id] = user.id
#         flood_limit = 1
    
#     limit = await get_flood_limit(chat_id)
#     flood_mode, until_time = await get_antiflood_settings(chat_id)
    
#     if flood_limit >= limit:
#         print(limit)
#         try:
#             if flood_mode == 1:
#                 await _.ban_chat_member(chat_id, user.id)
#                 return await message.reply_text(f"ʏᴇᴀʜ, ɪ ᴀɪɴ'ᴛ ɢᴏɴɴᴀ ʟᴇᴀᴠᴇ ʏᴏᴜʀ ғʟᴏᴏᴅɪɴɢ ʙᴇ!\n{user.mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ!")
#             elif flood_mode == 2:
#                 await _.restrict_chat_member(chat_id, user.id, ChatPermissions())
#                 await message.reply_text(f"ʏᴇᴀʜ, ɪ ᴀɪɴ'ᴛ ɢᴏɴɴᴀ ʟᴇᴀᴠᴇ ʏᴏᴜʀ ғʟᴏᴏᴅɪɴɢ ʙᴇ!\n{user.mention} ʜᴀs ʙᴇᴇɴ ᴍᴜᴛᴇᴅ!")
#             elif flood_mode == 3:
#                 await _.ban_chat_member(chat_id, user.id)
#                 await _.unban_chat_member(chat_id, user.id)
#                 await message.reply_text(f"ʏᴇᴀʜ, ɪ ᴀɪɴ'ᴛ ɢᴏɴɴᴀ ʟᴇᴀᴠᴇ ʏᴏᴜʀ ғʟᴏᴏᴅɪɴɢ ʙᴇ!\n{user.mention} ʜᴀs ʙᴇᴇɴ ᴋɪᴄᴋᴇᴅ!")
#             elif flood_mode == 4:
#                 until = await until_date(message, until_time)
#                 await _.ban_chat_member(chat_id, user.id, until_date=until)
#                 return await message.reply_text(f"ʏᴇᴀʜ, ɪ ᴀɪɴ'ᴛ ɢᴏɴɴᴀ ʟᴇᴀᴠᴇ ʏᴏᴜʀ ғʟᴏᴏᴅɪɴɢ ʙᴇ!\n{user.mention} ʜᴀs ʙᴇᴇɴ ʙᴀɴɴᴇᴅ ғᴏʀ {until_time}!")
#             elif flood_mode == 5:
#                 until = await until_date(message, until_time)
#                 await _.restrict_chat_member(chat_id, user.id, ChatPermissions(), until_date=until)
#                 await message.reply_text(f"ʏᴇᴀʜ, ɪ ᴀɪɴ'ᴛ ɢᴏɴɴᴀ ʟᴇᴀᴠᴇ ʏᴏᴜʀ ғʟᴏᴏᴅɪɴɢ ʙᴇ!\n{user.mention} ʜᴀs ʙᴇᴇɴ ᴍᴜᴛᴇᴅ ғᴏʀ {until_time}!")
#             flood_limit = 0
            
#         except BadRequest as ecp:
#             await message.reply_text(f"Error : {ecp.message}")
#         except Exception as e:
#             await message.reply_text(str(e))
        


            
DB = {}  


def reset_flood(chat_id, user_id=0):
    for user in DB[chat_id].keys():
        if user != user_id:
            DB[chat_id][user] = 0


@app.on_message(
    ~filters.service & ~filters.me & ~filters.private & ~filters.channel & ~filters.bot,
    group=flood_watcher,
)
async def flood_control_func(_, message):
    print(DB)
    if not message.chat:
        return
    chat_id = message.chat.id
    user_id = message.from_user.id
    if not await get_flood(chat_id):
        return
    
    if chat_id not in DB:
        DB[chat_id] = {}
        
    if not message.from_user:
        reset_flood(chat_id)
        return

    user = message.from_user
    if user_id not in DB[chat_id]:
        DB[chat_id][user_id] = 0

    reset_flood(chat_id, user_id)

    xx = await _.get_chat_member(chat_id, user.id)
    if xx.privileges or user.id in SUPREME_USERS or await isApproved(chat_id, user.id):
        return
    limit = await get_flood_limit(chat_id)
    flood_mode, until_time = await get_antiflood_settings(chat_id)
    if DB[chat_id][user.id] >= limit:
        DB[chat_id][user.id] = 0
        try:
            if flood_mode == 1:
                await _.ban_chat_member(chat_id, user.id)
                return await message.reply_text(f"**{user.mention} Is Banned For Flooding.**")
            elif flood_mode == 2:
                await _.restrict_chat_member(chat_id, user.id, ChatPermissions())
                await message.reply_text(f"**{user.mention} Is Muted For Flooding.**")
            elif flood_mode == 3:
                await _.ban_chat_member(chat_id, user.id)
                await _.unban_chat_member(chat_id, user.id)
                await message.reply_text(f"**{user.mention} Is Kicked For Flooding.**")
            elif flood_mode == 4:
                until = await until_date(message, until_time)
                await _.ban_chat_member(chat_id, user.id, until_date=until)
                return await message.reply_text(f"**{user.mention} Is Banned For {until_time} For Flooding.**")
            elif flood_mode == 5:
                until = await until_date(message, until_time)
                await _.restrict_chat_member(chat_id, user.id, ChatPermissions(), until_date=until)
                await message.reply_text(f"**{user.mention} Is Muted For {until_time} For Flooding.**")
            
        except BadRequest as ecp:
            await message.reply_text(f"Error : {ecp.message}")
        except Exception as e:
            await message.reply_text(str(e))
    
    DB[chat_id][user.id] += 1            
    
        
__help__ = """
**AntiFlood Allows You To Take Action On Spammers.**

**Commands**

♠ `/flood` - get current flood settings.
♠ `/setflood <ɪɴᴛ/'ɴᴏ'/'ᴏғғ'>` - set flood limit example - /serflood 10.
♠ `/setfloodmode` - flood mode to ban , mute , kick user.

"""
__mod_name__ = "Anti-Flood"
    

  
