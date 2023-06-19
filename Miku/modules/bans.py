import time , os
from Miku import app,BOT_ID,MENTION_BOT
from config import SUPREME_USERS as CHAD
from pyrogram import filters, enums
from Miku.modules.pyro.status import (
    bot_admin,
    bot_can_ban,
    user_admin,
    user_can_ban )
from Miku.modules.pyro.extracting_id import get_id_reason_or_rank,extract_user_id
from pyrogram.errors import BadRequest 
from pyrogram.types import ChatPermissions, Message 
from datetime import datetime, timedelta
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


async def until_date(message : Message, time_val):   
    possible = ["m","h","d","w"]
    try:
        exact = time_val[0]
        date = time_val[1]   
    except IndexError:
        await message.reply_text("**Invalid Syntax**")
        return None    
    if time_val[1] not in possible:
        await message.reply_text("**This Type Of Time Isn't Supported.**")
        return None
    if not exact.isdigit():
        await message.reply_text("**Invalid time amount specified**")
        return None 
    exact = int(exact)
    if date == "m":
        until = datetime.now() + timedelta(minutes=exact)
    if date == "h":
       until = datetime.now() + timedelta(hours=exact)  
    if date == "d":
       until = datetime.now() + timedelta(days=exact) 
    if date == "w":
       until = datetime.now() + timedelta(days=exact*7) 
      
    return until

@app.on_message(filters.command(["kickme","banme"]) & filters.group)
@bot_admin
@bot_can_ban
async def _kickme(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id 
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await message.reply_text("**Honestly You Are An Admin.**")
        return
    if message.command[0] == "kickme":
        try:
            await app.ban_chat_member(chat_id, user_id)
            await app.unban_chat_member(chat_id, user_id)
            await message.reply_text(f"**Kicked Out. {message.from_user.mention}**")
        except Exception as error:
            await message.reply_text(error)
    if message.command[0] == "banme":
        try:
            await app.ban_chat_member(chat_id, user_id)            
            await message.reply_text("**Banned !\nUser: {message.from_user.mention}\nAdmin: {MENTION_BOT}**")
        except Exception as error:
            await message.reply_text(error)
       
         
@app.on_message(filters.command(["ban","sban","dban"]) & filters.group)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _ban(_, message):
    user_id , reason = await get_id_reason_or_rank(message, sender_chat=True)
    chat_id = message.chat.id
    if not user_id:
        await message.reply_text("**Specify An User.**")
        return 
    if user_id == BOT_ID:
        await message.reply_text("**I Can't Ban Myself.**")
        return 
    if user_id in CHAD:
        await message.reply_text("**This Is An Alpha User.**")
        return
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        return await message.reply_text(f"**{message.from_user.mention} Can't Ban An Admin.**")
    try :
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )
    unban_btn  = InlineKeyboardMarkup([[InlineKeyboardButton("♠ UnBan ♠",callback_data=f"unbanUser_{user_id}")],[InlineKeyboardButton("❌ Close", callback_data="admin_close")]])
    if message.command[0] == "ban":
        await app.ban_chat_member(chat_id, user_id)
        await message.reply_text(f"**Banned !\nUser: {mention}\nAdmin: {message.from_user.mention if message.from_user else 'Anon'}**",reply_markup=unban_btn)        
    if message.command[0] == "sban":
        await message.delete()
        await message.reply_to_message.delete()
        await app.ban_chat_member(chat_id, user_id)
    if message.command[0] == "dban":
        await message.reply_to_message.delete()
        await pgram.ban_chat_member(chat_id, user_id)
        await message.reply_text(f"**Banned !\nUser: {mention}\nAdmin: {message.from_user.mention if message.from_user else 'Anon'}**",reply_markup=unban_btn)    
    
            
@app.on_message(filters.command("tban") & filters.group)
@bot_admin
@user_admin
@bot_can_ban
@user_can_ban
async def _tban(_, message):
    user_id , reason = await get_id_reason_or_rank(message, sender_chat=True)
    chat_id = message.chat.id
    if not user_id:
        await message.reply_text("**Specify An User.**")
        return 
    if user_id == BOT_ID:
        await message.reply_text("**I Can't Ban Myself.**")
        return 
    if user_id in CHAD:
        await message.reply_text("**This Is An Alpha User.**")
        return
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await message.reply_text(f"**{message.from_user.mention} Can't Ban An Admin.**")
    try :
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )    
    if not reason:
        return await message.reply_text("**You haven't Specified Time.**")
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""
    print(time_val)
    bantime = await until_date(message,time_val)
    if bantime == None:
        return 
    unban_btn  = InlineKeyboardMarkup([[InlineKeyboardButton("♠ UnBan ♠",callback_data=f"unbanUser_{user_id}")],[InlineKeyboardButton("❌ Close", callback_data="admin_close")]])
    await _.ban_chat_member(chat_id, user_id,until_date=bantime)
    await message.reply_text(f"""
    **Temp Banned !**
**Chat:** **{message.chat.title}**
**User:** **{mention}**
**Ban Time:** `{time_val}`    
    """,reply_markup=unban_btn)
         
 
@app.on_callback_query(filters.regex(pattern=r"unbanUser_(.*)"))
async def _unbamcb(_,query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    mention = (await _.get_users(user_id)).mention
    id = query.data.split("_")
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await _.unban_chat_member(chat_id,int(id[1]))
        await query.message.edit_text(f"**UnBanned Successfully Now They Can Join.**")
               
@app.on_message(filters.command("tmute") & filters.group)
@bot_admin
@user_admin
@bot_can_ban
@user_can_ban
async def _tmute(_, message):
    user_id , reason = await get_id_reason_or_rank(message, sender_chat=True)
    chat_id = message.chat.id
    if not user_id:
        await message.reply_text("**Specify An User.**")
        return 
    if user_id == BOT_ID:
        await message.reply_text("**I Can't Ban MySelf.**")
        return 
    if user_id in CHAD:
        await message.reply_text("**This Is An Alpha User.**")
        return
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await message.reply_text(f"**{message.from_user.mention} Can't Ban An Admin.**")
    try :
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )    
    if not reason:
        return await message.reply_text("**You haven't Specified Time.**")
    split_reason = reason.split(None, 1)
    time_val = split_reason[0].lower()
    reason = split_reason[1] if len(split_reason) > 1 else ""  
    mutetime = await until_date(message,time_val)
    if mutetime == None:
        return 
    unban_btn  = InlineKeyboardMarkup([[InlineKeyboardButton("♠ UnBan ♠",callback_data=f"unmuteUser_{user_id}")],[InlineKeyboardButton("❌ Close", callback_data="admin_close")]])
    await _.restrict_chat_member(chat_id, user_id,ChatPermissions(),until_date=mutetime)
    await message.reply_text(f"""
**Muted !**
**Chat:** **{message.chat.title}**
**User:** **{mention}**
**Mute Time:** `{time_val}`    
    """,reply_markup=unban_btn)

@app.on_callback_query(filters.regex(pattern=r"unmuteUser_(.*)"))
async def _unbamcb(_,query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    mention = (await _.get_users(user_id)).mention
    id = query.data.split("_")
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        try:
            await _.unban_chat_member(chat_id,int(id[1]))
            await query.message.edit_text(f"**UnMuted Successfully Now They Can Chat.**")   
        except:
            await _.answer_callback_query(query.id,text="User Isn't Muted.",show_alert=True)      

@app.on_message(filters.command("unban") & filters.group)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _unban(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    admin = message.from_user.mention
    user = await extract_user_id(message)
    if (replied
        and replied.sender_chat 
        and replied.sender_chat != chat_id):
        await message.reply_text("**You Can't UnBan Channel.**")
        return
    if not user:
        await message.reply_text("**Specify An User.**")
        return 
    member = await _.get_chat_member(chat_id,user)      
    if member.status != enums.ChatMemberStatus.BANNED:
        await message.reply_text("**User Isn't Banned.**")
    else :
        try:
            await app.unban_chat_member(chat_id,user)
            umention = member.mention
            await message.reply_text(f"**UnBanned {umention} Successfully.**")
        except BadRequest as ok:
            await message.reply_text(ok)
        
@app.on_message(filters.command(["kick","dkick","skick","punch"]) & filters.group)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _kick(_, message):
    chat_id = message.chat.id    
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**Specify An User.**")
        return 
    if user_id == BOT_ID:
        await message.reply_text("**I Can't Kick MySelf.**")
        return 
    if user_id in CHAD:
        await message.reply_text("**This Is An Alpha User.**")
        return 
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await message.reply_text(f"**message.from_user.mention} Can't Kick An Admin.**")
        return 
    try:
        mention = (await app.get_users(user_id)).mention
    except IndexError:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )    
    text = f"**Kicked Out. {mention}**"
      
    if message.command[0] in ["kick","punch"]:
        try:
            await app.ban_chat_member(chat_id,user_id) 
            await app.unban_chat_member(chat_id,user_id)
            await message.reply_text(text)
        except BadRequest as err :
            await message.reply_text(err)
    if message.command[0] == "dkick":  
        try:
            await message.reply_to_message.delete()
            await app.ban_chat_member(chat_id,user_id) 
            await app.unban_chat_member(chat_id,user_id)
            await message.reply_text(text)
        except BadRequest as err :
            await message.reply_text(err) 
    if message.command[0] == "skick":
        try:
            await message.reply_to_message.delete()
            await message.delete()
            await app.ban_chat_member(chat_id,user_id) 
            await app.unban_chat_member(chat_id,user_id)            
        except BadRequest as err :
            await message.reply_text(err)        
     
@app.on_message(filters.command(["mute","dmute","smute"]) & filters.group)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _kick(_, message):
    chat_id = message.chat.id    
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**Specify An User.**")
        return 
    if user_id == BOT_ID:
        await message.reply_text("**I Can't Mute MySelf.**")
        return 
    if user_id in CHAD:
        await message.reply_text("**This Is An Alpha User.**")
        return 
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        await message.reply_text(f"message.from_user.mention} Can't Mute An Admin.**")
        return 
    user = await _.get_chat_member(chat_id,user_id)   
    if user.status == enums.ChatMemberStatus.RESTRICTED:
        await message.reply_text("**This User Is Already Muted.**")
        return  
    try:
        mention = user.mention
    except:
        mention = (
            message.reply_to_message.sender_chat.title
            if message.reply_to_message
            else "Anon"
        )    
    text = f"**Muted. {mention}**"
      
    if message.command[0] == "mute":
        try:
            await app.restrict_chat_member(chat_id,user_id,ChatPermissions())             
            await message.reply_text(text)
        except BadRequest as err :
            await message.reply_text(err)
    if message.command[0] == "dmute":  
        if not message.reply_to_message:
            await message.reply_text("**Reply To User.**")
        else:
            try:
                await message.reply_to_message.delete()
                await app.restrict_chat_member(chat_id,user_id,ChatPermissions())
                await message.reply_text(text)
            except BadRequest as err :
                await message.reply_text(err) 
    if message.command[0] == "smute":
        if not message.reply_to_message:
            await message.reply_text("**Reply To User.**")
        else:
            try:
                await message.delete()
                await message.reply_to_message.delete()
                await app.restrict_chat_member(chat_id,user_id,ChatPermissions())            
            except BadRequest as err :
                await message.reply_text(err)        
     
    
@app.on_message(filters.command("unmute") & filters.group)
@bot_admin
@bot_can_ban
@user_admin
@user_can_ban
async def _unmute(_, message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    admin = message.from_user.mention
    user_id = await extract_user_id(message)
    if (replied
        and replied.sender_chat 
        and replied.sender_chat != chat_id):
        await message.reply_text("**You Can't UnMute A Channel.**")
        return
    if not user:
        await message.reply_text("**Specify An User.**")
        return 
    user = await _.get_chat_member(chat_id,user_id)   
    if user.status != enums.ChatMemberStatus.RESTRICTED:
        await message.reply_text("**This User Isn't Muted.**")
    else :
        try:
            await app.unban_chat_member(chat_id,user)
            umention = user.mention
            await message.reply_text(f"**UnMuted. {umention}**")
        except BadRequest as ok:
            await message.reply_text(ok)
    


@app.on_message(filters.command("users") & filters.group)
@user_admin
async def _list(_, message):
    msg = await message.reply("**Importing Data....**")
    count = await app.get_chat_members_count(message.chat.id)
    title = message.chat.title 
    mentions = f"**Users In {title}\n**"
    async for member in app.get_chat_members(message.chat.id):
        mentions += (
            f"\nDeleted Accounts {member.user.id}"
            if member.user.is_deleted
            else f"\n{member.user.mention} {member.user.id}"
            )
    
    with open("userslist.txt", "w+") as file:
        file.write(mentions)
    await app.send_document(
        message.chat.id,
        "userslist.txt",
        caption=f"**Total Users In {title} Is {count}.**"       
    )
    await msg.delete()
    os.remove("userslist.txt")      


__help__ = """
**⸢ᴄᴀɴ ᴏɴʟʏ ʙᴇ ᴜsᴇᴅ ɪɴ ɢʀᴏᴜᴘs.⸥**

「𝗖𝗢𝗠𝗠𝗔𝗡𝗗𝗦」 :
═───────◇───────═
๏ /kickme : ᴘᴜɴᴄʜs ᴛʜᴇ ᴜsᴇʀ ᴡʜᴏ ɪssᴜᴇᴅ ᴛʜᴇ ᴄᴏᴍᴍᴀɴᴅ
「𝗔𝗗𝗠𝗜𝗡𝗦 𝗢𝗡𝗟𝗬」
๏ /ban ᴏʀ /dban <ᴜsᴇʀʜᴀɴᴅʟᴇ> : ʙᴀɴs ᴀ ᴜsᴇʀ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
๏ /sban <ᴜsᴇʀʜᴀɴᴅʟᴇ> : sɪʟᴇɴᴛʟʏ ʙᴀɴ ᴀ ᴜsᴇʀ. ᴅᴇʟᴇᴛᴇs ᴄᴏᴍᴍᴀɴᴅ, ʀᴇᴘʟɪᴇᴅ ᴍᴇssᴀɢᴇ ᴀɴᴅ ᴅᴏᴇsɴ'ᴛ ʀᴇᴘʟʏ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
๏ /tban <ᴜsᴇʀʜᴀɴᴅʟᴇ> x(m/h/d) : ʙᴀɴs ᴀ ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). ᴍ = ᴍɪɴᴜᴛᴇs, ʜ = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs.
๏ /listbans : ʟɪsᴛ ᴏғ ʙᴀɴɴᴇᴅ ᴜsᴇʀs ɪɴ ᴀ ᴄʜᴀᴛ.
๏ /unban <ᴜsᴇʀʜᴀɴᴅʟᴇ> :  ᴜɴʙᴀɴs a user. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
๏ /punch <ᴜsᴇʀʜᴀɴᴅʟᴇ> :  Punches a user out of the group, (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ)
๏ /mute or /dmute <ᴜsᴇʀʜᴀɴᴅʟᴇ> : sɪʟᴇɴᴄᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ.
๏ /tmute <userhandle> x(m/h/d) : ᴍᴜᴛᴇs a ᴜsᴇʀ ғᴏʀ x ᴛɪᴍᴇ. (ᴠɪᴀ ʜᴀɴᴅʟᴇ, ᴏʀ ʀᴇᴘʟʏ). m = ᴍɪɴᴜᴛᴇs, h = ʜᴏᴜʀs, ᴅ = ᴅᴀʏs.
๏ /unmute <userhandle> : ᴜɴᴍᴜᴛᴇs ᴀ ᴜsᴇʀ. ᴄᴀɴ ᴀʟsᴏ ʙᴇ ᴜsᴇᴅ ᴀs ᴀ ʀᴇᴘʟʏ, ᴍᴜᴛɪɴɢ ᴛʜᴇ ʀᴇᴘʟɪᴇᴅ ᴛᴏ ᴜsᴇʀ. 
═───────◇───────═
"""
__mod_name__ = "𝙱ᴀɴs"

