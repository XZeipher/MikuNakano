import time 
import asyncio
from Miku import app,get_readable_time
from pyrogram import filters, enums 
from Miku.modules.pyro.status import user_admin
from pyrogram.errors import FloodWait 

SPAM_CHATS = []

@app.on_message(filters.command(["tagall", "all"]) | filters.command("@all", "") & filters.group)
@user_admin
async def tag_all_users(_,message): 
    replied = message.reply_to_message  
    if len(message.command) < 2 and not replied:
        await message.reply_text("**Reply To Message.**") 
        return                  
    if replied:
        SPAM_CHATS.append(message.chat.id)
        start = time.time()        
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id): 
            if message.chat.id not in SPAM_CHATS:
                break       
            usernum += 1
            alpha = ""
            usertxt += f"[{alpha}](tg://user?id={m.user.id})"
            if usernum == 5:
                await replied.reply_text(usertxt)
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""
        end = get_readable_time((time.time() - start))
        await message.reply_text(f"**Mention Completed In** `{end}`")
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass
    else:
        text = message.text.split(None, 1)[1]
        
        SPAM_CHATS.append(message.chat.id)
        start = time.time()
        usernum= 0
        usertxt = ""
        async for m in app.get_chat_members(message.chat.id):       
            if message.chat.id not in SPAM_CHATS:
                break 
            usernum += 1
            alpha = ""
            usertxt += f"[{alpha}](tg://user?id={m.user.id})"
            if usernum == 5:
                await app.send_message(message.chat.id,f'{text}\n{usertxt}')
                await asyncio.sleep(2)
                usernum = 0
                usertxt = ""            
        end = get_readable_time((time.time() - start))
        await message.reply_text(f"**Mention Completed In** `{end}`")                
        try :
            SPAM_CHATS.remove(message.chat.id)
        except Exception:
            pass        
           


@app.on_message(filters.command("cancel") & filters.group)
@user_admin
async def cancelcmd(_, message):
    chat_id = message.chat.id
    if chat_id in SPAM_CHATS:
        try :
            SPAM_CHATS.remove(chat_id)
        except Exception:
            pass   
        return await message.reply_text("**Mention Cancelled.**")     
                                     
    else :
        await message.reply_text("**Mention Not Started.**")  
        return       
    
__help__ = """
**Tag Everyone In Chats.**

**Command**

 `/tagall` : mention everyone by tagging them.
 `/cancel` : cancel current mention process.
"""
__mod_name__ = "Tag-All"
    
