from pyrogram import filters,enums
from Miku import pgram
from config import SUPREME_USERS
from Miku.modules.pyro.status import user_admin
from Miku.modules.pyro.extracting_id import extract_user_id
from Miku.modules.tagall import SPAM_CHATS
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 
from Miku.modules.mongo.approve_db import *
from .pyro.decorators import control_user,command

@app.on_message(command(commands=("approve")))
@control_user()
@user_admin
async def _approve(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**Specify An User.**")
    
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        return await message.reply_text("**This Is An Admin.**")       
    check_user = await isApproved(chat_id,user_id)
    if check_user:
        return await message.reply_text(f"**{member.user.mention} Is Already Approved.**")
    await approve_user(chat_id, user_id)
    return await message.reply_text(f"**{member.user.mention} Has Been Approved {message.chat.title}!**")              


@app.on_message(command(commands=("disapprove")))
@control_user()
@user_admin
async def _approve(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)
    if not user_id:
        await message.reply_text("**Specify An User.**")
    
    member = await _.get_chat_member(chat_id,user_id)      
    if member.privileges:
        return await message.reply_text("**This Is An Admin.**")       
    check_user = await isApproved(chat_id,user_id)
    if not check_user:
        return await message.reply_text(f"**{member.user.mention} Isn't Approved Yet!**")
    await disapprove_user(chat_id, user_id)
    await message.reply_text(f"**{member.user.mention} Is No Longer Approved In {message.chat.title}**")              

@app.on_message(command(commands=("approved")))
@control_user()
@user_admin
async def _approvedlist(_, message):
    chat_id = message.chat.id
    list1 = await approved_users(chat_id)
    if not list:
        return await message.reply_text("**There Is No Approved User.**")
    text = "**♠ Approved Users ♠\n**"
    for i in list1:
        try:
            member = await _.get_chat_member(chat_id,int(i))
            text += f"• {member.user.mention}\n"
        except:
            pass
    await message.reply_text(text)   

@app.on_message(command(commands=("approval")))
@control_user()
@user_admin
async def _approval(_, message):
    chat_id = message.chat.id
    user_id = await extract_user_id(message)    
    if not user_id:
        return await message.reply_text("**Specify An User.**")
    try :
        m = await _.get_chat_member(chat_id,user_id)
    except Exception as e:
        print(e)
        return await message.reply_text("**User Isn't Here**")
    check_user = await isApproved(chat_id,user_id)
    if check_user:
        return await message.reply_text(f"**{m.user.mention} Is An Approved User.**")
    
    return await message.reply_text(f"**{m.user.mention} Isn't An Approved User.**") 

@app.on_message(filters.command("disapproveall") & filters.group)
@control_user()                  
async def _disappall(_, message):
    user_id = message.from_user.id
    chat_id = message.chat.id
    m = await _.get_chat_member(chat_id,user_id)
    if m.status != enums.ChatMemberStatus.OWNER:
        return await message.reply_text("**Only Owner Of This Group Can Use This Command.**")
    list1 = await approved_users(chat_id)
    if list1 is None:
        return await message.reply_text("**There Aren't Any Approved Users In This Chat.**")
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("DisApprove-All", callback_data="unaproveall")],[InlineKeyboardButton("❌ Close",callback_data="admin_close")]])
    await message.reply_text("Are You Sure?",reply_markup=btn)

@app.on_callback_query(filters.regex("unaproveall"))
@control_user()                  
async def _unappall(_, query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    m = await _.get_chat_member(chat_id,user_id)
    if m.status != enums.ChatMemberStatus.OWNER or user_id not in SUPREME_USERS:
        return await query.answer("Only Owner Can Use It.",show_alert=True)
    list1 = await approved_users(chat_id)
    SPAM_CHATS.append(chat_id)
    return await query.message.edit_text("**DisApproval Started. Use /cancel to cancel this process.**")
    for user in list1:
        if chat_id not in SPAM_CHATS:
            break 
        await disapprove_user(chat_id,int(user))
    return await query.message.edit_text("**DisApproved All Users.**")
     
        

__help__ = """
**Approval System For Group Safety.**

**Commands**
 
♠ `/approve <user>`: approved user antiflood won't be applied.
♠ `/disapprove <user>`: disapprove user antiflood will be applied on them.
♠ `/approved`: list of approved users.
♠ `/approval <user>`: check the approval status of an user.
♠ `/disapproveall`: disapprove all users. (owner only)

"""

__mod_name__ = "Approve"
