import time
import os
from Miku import app,LOG,BOT_ID,get_readable_time
from pyrogram import filters,enums, Client 
from Miku.modules.pyro.status import (
    bot_admin,
    user_admin,
    user_has_permission)
from Miku.modules.pyro.extracting_id import (
    extract_user_id,
    get_id_reason_or_rank,
    get_user_id )

from pyrogram.enums import MessageEntityType, ChatMemberStatus
from pyrogram.types import ChatPrivileges, InlineKeyboardMarkup, InlineKeyboardButton ,CallbackQuery
from pyrogram.errors import BadRequest
from config import SUPREME_USERS as CHAD
from .pyro.decorators import control_user,command

COMMANDERS = [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]




DEMOTE = ChatPrivileges(
        can_change_info=False,
        can_invite_users=False,
        can_delete_messages=False,
        can_restrict_members=False,
        can_pin_messages=False,
        can_promote_members=False,
        can_manage_chat=False,
        can_manage_video_chats=False,
    )
    

    
@app.on_message(command(commands=("bots")))
@control_user()                  
@user_admin
async def _botlist(_, message):       
    chat_title = message.chat.title 
    chat_id = message.chat.id 
    repl = await message.reply("**Initialising Bots For This Chat...**")                                        
    header = f"**× Bots\n\n**"    
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BOTS):
        header += f"**• {m.user.mention}\n**"
    await repl.edit(f"{header}\n\n")

        
@app.on_message(command(commands=["promote","fullpromote"]))
@control_user()
@user_admin
@bot_admin                  
async def _promote(_, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_promote_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,message.from_user.id,"can_promote_members",bot=False)
    if not bpermission:
        return await message.reply(btxt)
    if not upermission:
        return await message.reply(utxt)
    mm = await get_id_reason_or_rank(message)
    user_id = mm[0]
    title = mm[1]    
    from_user = message.from_user 
    bot = await _.get_chat_member(chat_id, BOT_ID)
    chat = message.chat.title    
   
    if not user_id:
        await message.reply_text("**Specify An User To Promote.**")
        return
    if user_id == BOT_ID:
        await message.reply_text("**Sorry But I Can't Promote Myself.**")
        return 
    meme = await _.get_chat_member(chat_id,user_id)
    if meme.privileges:
        await message.reply_text("**User Is Already An Admin So Can't Promote Him/Her Again.**")
        return
    user_mention = (await app.get_users(user_id)).mention
    btn = InlineKeyboardMarkup([[InlineKeyboardButton(text="Close ❌", callback_data=f"puserclose_{from_user.id}")]])   
    if message.command[0] == "promote":
        POWER = ChatPrivileges(
            can_change_info=False,
            can_invite_users=bot.privileges.can_invite_users,
            can_delete_messages=bot.privileges.can_delete_messages,
            can_restrict_members=False,
            can_pin_messages=False,
            can_promote_members=False,
            can_manage_chat=bot.privileges.can_manage_chat,
            can_manage_video_chats=bot.privileges.can_manage_video_chats,
            )         
        msg = f"**× Appointed !\n\n• User : {user_mention}\n• Admin : {from_user.mention}**"

    elif message.command[0] == "fullpromote":   
        POWER = ChatPrivileges(
            can_change_info=bot.privileges.can_change_info,
            can_invite_users=bot.privileges.can_invite_users,
            can_delete_messages=bot.privileges.can_delete_messages,
            can_restrict_members=bot.privileges.can_restrict_members,
            can_pin_messages=bot.privileges.can_pin_messages,
            can_promote_members=bot.privileges.can_promote_members,
            can_manage_chat=bot.privileges.can_manage_chat,
            can_manage_video_chats=bot.privileges.can_manage_video_chats, 
             )                    
        msg = f"**× Fully Appointed !\n\n• User : {user_mention}\n• Admin : {from_user.mention}\n**" 
    
    try:
        await app.promote_chat_member(chat_id, user_id,POWER)           
        if title != None:
            await app.set_administrator_title(chat_id, user_id,title)
        return await message.reply_text(msg,reply_markup=btn)    
    except BadRequest as excp:
        await message.reply_text(f"**{excp.message}.**")
           
    except Exception as e :
        return await message.reply_text(e)
            

@app.on_message(command(commands=("demote")))
@control_user()
@user_admin
@bot_admin  
async def _demote(_, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_promote_members")
    upermission,utxt = await user_has_permission(chat_title,chat_id,message.from_user.id,"can_promote_members",bot=False)
    if not bpermission:
        return await message.reply(btxt)
    if not upermission:
        return await message.reply(utxt)
    user_id = await extract_user_id(message) 
       
    if not user_id:
        await message.reply_text("**Specify An User To Demote.**")
        return
    if user_id == BOT_ID:
        await message.reply_text("**Sorry But I Can't Demote Myself.**")
        return 
    xx = await _.get_chat_member(chat_id,user_id)
    if not xx.privileges:    
        await message.reply_text("**User Isn't An Admin.**")
        return
    
    user_mention = xx.user.mention
    try : 
        await app.promote_chat_member(chat_id,user_id,DEMOTE)
        await message.reply_text(f"**Demoted {user_mention}**")
    except BadRequest as excp:
        await message.reply_text(f"**{excp.message}.**")           


@app.on_message(command(commands=("invitelink")))
@control_user()                  
@user_admin
@bot_admin
async def _invitelink(_,message):
    chat_id = message.chat.id
    BOT = await app.get_chat_member(chat_id, BOT_ID)

    if message.chat.username  :
        await message.reply_text(f"https://t.me/{message.chat.username}")  

    elif message.chat.type in [enums.ChatType.SUPERGROUP,enums.ChatType.CHANNEL] :
        if BOT.privileges.can_invite_users:
            link = await app.export_chat_invite_link(chat_id)
            await message.reply_text(link)                        
        else:
            await message.reply_text(
                "**I Don't Have Permission To Extract Invite Links.**",
            )    
    else:
        await message.reply_text(
            "**I Can Only Give Invite Links Of Group And Channels.**",
        )


                               
@app.on_message(command(commands=["setgtitle","setgdesc","title"]))
@control_user()
@user_admin
@bot_admin
async def g_title_desc(_,message):  
    chat_id = message.chat.id
    replied = message.reply_to_message
    chat_title = message.chat.title
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_change_info")
    upermission,utxt = await user_has_permission(chat_title,chat_id,message.from_user.id,"can_change_info",bot=False)
    if not bpermission:
        return await message.reply(btxt)
    if not upermission:
        return await message.reply(utxt)
    if message.command[0] == "setgtitle":       
        if len(message.command) < 2:
            await message.reply_text(f"**{mention} Give Me A Text To Add It As Group Title.**")  
            return
        elif replied:
        	get_new_title = replied.text
        else:
            get_new_title = message.text.split(None,1)[1]
            try:                    
                await app.set_chat_title(chat_id,get_new_title)      
                await message.reply_text(f"**Successfully Set Group Title To : {get_new_title}**")
            except BadRequest as excp:
                await message.reply_text(f"**{excp.message}.**")
                return
    if message.command[0] == "setgdesc":
        tesc = message.text.split(None, 1)
        if len(tesc) >= 2:
            desc = tesc[1]
        if replied:
        	desc = replied.text
        else:
            return await message.reply_text("**Empty Description.**")
        try:
            if len(desc) > 255:
                return await message.reply_text("**Description Must Be Under 255 Characters.**")
            await app.set_chat_description(chat_id, desc)
            await message.reply_text(f"**Successfully Set Description In {chat_title}.**")
        except BadRequest as excp:
            await message.reply_text(f"**{excp.message}.**")
    if message.command[0] == "title":
        if not replied:
            await message.reply_text("**Reply To An Admin To Set Title.**")
            return
        if len(message.command) < 2:
            await message.reply_text("**Give A Title Too.**")
            return
        try:
            title = message.text.split(None, 1)[1]
            await app.set_administrator_title(chat_id, replied.from_user.id,title)
            await message.reply_text(f"**Successfully Set {replied.from_user.mention} Title To {title}.**")
        except BadRequest as excp:
            await message.reply_text(f"**{excp.message}.**")
        except Exception as e:
           await message.reply_text(e)
        
            
            
     
    
                                   
@app.on_message(command(commands=["setgpic","delgpic"]))
@control_user()
@user_admin
@bot_admin
async def g_pic(_,message):
    chat_id = message.chat.id
    replied = message.reply_to_message
    bpermission,btxt = await user_has_permission(chat_title,chat_id,BOT_ID,"can_change_info")
    upermission,utxt = await user_has_permission(chat_title,chat_id,message.from_user.id,"can_change_info",bot=False)
    if not bpermission:
        return await message.reply(btxt)
    if not upermission:
        return await message.reply(utxt)  
    if message.command[0] == "setgpic":
        if replied :            
            if (replied.photo or replied.sticker) and not replied.sticker.is_animated:
                text = await message.reply_text("**Processing...**")  
                g_pic = await replied.download()       
                try:                    
                    await app.set_chat_photo(chat_id, photo=g_pic)
                    await text.delete()
                    await message.reply_text("**Successfully Set Group Pic.**")
                    
                except Exception as error:
                    await message.reply_text(error)

                os.remove(g_pic)

            else:
                await message.reply_text("**Reply To An Image.**")
        else:
            await message.reply_text("**Reply To An Image.**")
 
    if message.command[0] == "delgpic":
        try:
            await app.delete_chat_photo(chat_id)
            await message.reply_text("**Successfully Removed Group Pic.**")
        except Exception as e:
            await message.reply_text(e)
        


@app.on_message(command(commands=["adminlist","admins"]))
@control_user()                  
async def _adminlist(_, message):  
    if message.chat.type == enums.ChatType.PRIVATE:
        return await message.reply("**This Command Is Only Usable In Groups Not Private.**")
    repl = await message.reply(
            "**Initialising Admins...**",
            
        )    
    chat_name = message.chat.title 
    chat_id = message.chat.id 
    administrators = []
    async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
        if m.user.is_bot:
            pass
        else:
            administrators.append(m)
    text = f"**♣ Admins ♣"
    custom_admin_list = {}
    normal_admin_list = []   
    for admin in administrators:
            user = admin.user
            status = admin.status
            custom_title = admin.custom_title
            if user.is_deleted:
                name = "**Deleted Accounts.**"
            else:
                name = f"**{user.mention}**"            
            if status == ChatMemberStatus.OWNER:
                text += "**\n♠ Admins**"
                text += f"**\n • {name}\n**"
                if custom_title:
                    text += f"**♦ {custom_title}\n**"
            if status == ChatMemberStatus.ADMINISTRATOR:
                if custom_title:
                    try:
                        custom_admin_list[custom_title].append(name)
                    except KeyError:
                        custom_admin_list.update({custom_title: [name]})
                else:
                    normal_admin_list.append(name)
    text += "**\n ♣ Admins ♣**"
    for admin in normal_admin_list:
        text += f"**\n • {admin}**"
    for admin_group in custom_admin_list.copy():
        if len(custom_admin_list[admin_group]) == 1:
            text += f"**\n • {custom_admin_list[admin_group][0]} | {admin_group} **"
                
            custom_admin_list.pop(admin_group)
    text += "\n"
    for admin_group, value in custom_admin_list.items():
        text += f"**\n{admin_group} **"
        for admin in value:
            text += f"**\n • {admin}**"
        text += "\n"
    try:
        await repl.edit_text(text)
    except BadRequest:
        return
            
__help__ = """
**Here is The Help For Admins**

**Commands**
♠ `/promote <ᴜsᴇʀ>` - Promote an user.
♠ `/fullpromote <ᴜsᴇʀ>` - Promote an user with full rights.
♠ `/demote <ᴜsᴇʀ>` - Demote an user.
♠ `/setgtitle <ᴛɪᴛʟᴇ>` - Set the group title.
♠ `/setgpic <ʀᴇᴘʟʏ to image>` - Set the group pfp.
♠ `/delgpic <ʀᴇᴘʟʏ to image>` - Remove the group pfp.
♠ `/setgdesc <ᴛᴇxᴛ>` - Set the group description.
♠ `/adminlist` - List of admins in the chat.
♠ `/bots` - List of bots in the chat.
♠ `/invitelink` - Get invite link of groups.
"""
__mod_name__ = "Admins"
