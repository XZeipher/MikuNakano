from io import BytesIO 
from Miku import app
from config import DEV_USERS
from pyrogram import filters 
from Miku.modules.mongo.blacklistChat_db import *

@app.on_message(filters.command("blacklistchat"))
async def _blchat(_, message):
    if message.from_user.id not in DEV_USERS:
        return
    if len(message.command) < 2:
        return await message.reply_text("**Provide Chat ID.**")
    chat_id = int(message.command[1])
    await add_blacklistchat(chat_id)
    title = await _.get_chat(chat_id)
    return await message.reply_text(f"**Added {title} In Blacklist.**")  
 

@app.on_message(filters.command("blacklistchats"))
async def _blacklist_chats(_, message):
    if message.from_user.id not in DEV_USERS:
        return
    chats = await get_blacklist_chat()
    if not chats:
        return await message.reply_text("**There Is No Blacklisted Chats.**")
    msg = "**  Blacklisted Chats **\n"
    for i in chats:
        try:
            chat = await _.get_chat(int(i))
            msg += f"• {chat.title} - {chat.id}\n"
        except:
            pass
    with BytesIO(str.encode(msg)) as output:
        output.name = "blackchats.txt"
        await message.reply_document(            
            document = output,
            caption="**Blacklisted Chats.**")
        
                  

    
