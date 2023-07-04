import asyncio
from Miku import app,BOT_ID
from config import DEV_USERS
from pyrogram import filters, Client ,enums
from Miku.modules.mongo.chats_db import get_served_chats,remove_served_chat
from pyrogram.types import Message , InlineKeyboardButton, InlineKeyboardMarkup 
from pyrogram.errors import BadRequest, Unauthorized


async def get_muted_chats(app: Client, message: Message, leave: bool = False):
    chat_id = message.chat.id
    chats = await get_served_chats()
    muted_chats, progress = 0, 0
    chat_list = []
    progress_message = None

    for chat in chats:
        if ((100 * chats.index(chat)) / len(chats)) > progress:
            progress_bar = f"**{progress}% Getting Muted Chats.**"
            if progress_message:
                try:
                    await app.edit_message_text(chat_id,progress_message.id,progress_bar)                       
                except:
                    pass
            else:
                progress_message = await app.send_message(chat_id, progress_bar)
            progress += 5
        
        await asyncio.sleep(0.1)
        try:
           await app.send_chat_action(chat, enums.ChatAction.TYPING) 
        except (BadRequest, Unauthorized):
            muted_chats += +1
            chat_list.append(cid)
    try:
        await progress_message.delete()
    except:
        pass
    if not leave:
        return muted_chats
    for muted_chat in chat_list:
        await asyncio.sleep(0.1)
        try:
            await app.leave_chat(muted_chat)
        except:
            pass
        await remove_served_chat(muted_chat) 
    return muted_chats

async def get_invalid_chats(app : Client,message : Message,remove: bool = False):
    chat_id = message.chat.id
    chats = await get_served_chats()
    kicked_chats, progress = 0, 0
    chat_list = []
    progress_message = None    
    for chat in chats:
        if ((100 * chats.index(chat)) / len(chats)) > progress:
            progress_bar = f"**{progress}% Getting Invalid Chats.**"
            if progress_message:
                try:
                    await app.edit_message_text(chat_id,progress_message.id,progress_bar)                       
                except:
                    pass
            else:
                progress_message = await app.send_message(chat_id, progress_bar)
            progress += 5
        
        await asyncio.sleep(0.1)
        try:
            await app.get_chat_member(chat,BOT_ID)
        except (BadRequest, Unauthorized):
            kicked_chats += 1
            chat_list.append(chat)
    try:
        await progress_message.delete()
    except:
        pass
    if not remove:
        return kicked_chats
    for muted_chat in chat_list:
        await asyncio.sleep(0.1)
        await remove_served_chat(muted_chat)
    return kicked_chats
            

@app.on_message(filters.command("dbcleanup") & filters.user(DEV_USERS))
async def _dbcleanup(_, message):
    txt = await message.reply("**Getting Invalid Chat Count...**")
    invalid_chats = await get_invalid_chats(_, message)
    btn = InlineKeyboardMarkup([[InlineKeyboardButton("Cleanup", callback_data="db_cleanup")],[InlineKeyboardButton("Leave Invalid Chat",callback_data="db_leave_chat")]])
    await txt.edit(f"**Invalid Chat :** `{invalid_chats}`",reply_markup=btn)
         

@app.on_callback_query(filters.regex("^(db_cleanup|db_leave_chat)$"))
async def _db_cleanup(_, query):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    if user_id not in DEV_USERS:
        return await _.answer_callback_query(query.id,text="You Aren't Sun User.",show_alert=True)
    if query.data == "db_cleanup":
        await _.edit_message_text(chat_id, query.message.id,"**DB Cleaning...**")
        invalid_chat_count = await get_invalid_chats(_, query.message, True)  
        await _.edit_message_text(chat_id, query.message.id,f"**Cleaned Chats :** `{invalid_chat_count}`")   
    elif query.data == "db_leave_chat":
        await _.edit_message_text(chat_id, query.message.id,"**Invalid Chats Leaving...**")
        chat_count = await get_muted_chats(_, query.message, True)
        await _.edit_message_text(chat_id, query.message.id,f"**Removed Chats :** `{chat_count}`")   
    
    
     
