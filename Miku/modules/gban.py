import time 
import asyncio
from Miku import app,BOT_ID,get_readable_time
from config import SUPREME_USERS
from pyrogram import filters
from io import BytesIO
from Miku.modules.pyro.extracting_id import get_id_reason_or_rank,extract_user_id
from Miku.modules.mongo.chats_db import get_served_chats
from pyrogram.errors import Unauthorized, FloodWait 
from Miku.modules.mongo.gbans_db import *


@app.on_message(filters.command("gban"))
async def _gban(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return await message.reply_text("**You Don't Have Access To This Command.**")
    user_id,reason = await get_id_reason_or_rank(message)
    from_user = message.from_user
    if not user_id:
        return await message.reply_text("**Specify An User.**")    
    if not reason:
        return await message.reply_text("**Provide A Reason.**")
    if user_id in [from_user.id, BOT_ID] or user_id in SUPREME_USERS:
        return await message.reply_text("**This Is An Alpha User.**")
    user = await _.get_users(user_id)
    start_time = time.time()
    chats = await get_served_chats()
    msg = await message.reply(f"**Initialising Gban On User ID :** `{user_id}`\n**Kicking Out From {chats} Chats**")
    await add_gban_user(user_id,reason)
    number_of_chats = 0
    for chat in chats:
        try:
            await _.ban_chat_member(chat, user_id)
            number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass
    try:
        await _.send_message(user_id,f"**You Have been Gbanned By {from_user.mention}\nYou Can Appeal This Gban From @MikuNakanoXSupport**")            
    except Unauthorized:
        pass
    gban_time = get_readable_time((time.time() - start_time))
    await msg.edit(f"**♠ Global Ban ♠\n• Banned : {user.mention}\n• Chats :** `{number_of_chats}`")
    
    
@app.on_message(filters.command("ungban"))
async def _ungban(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return await message.reply_text("**You Don't Have Access To This Command.**")
    user_id = await extract_user_id(message)
    if not user_id:
        return await message.reply_text("**Specify An User.**")    
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return await message.reply_text("**This User Isn't Gbanned.**")    
    await remove_gban_user(user_id)
    start_time = time.time()
    chats = await get_served_chats() 
    number_of_chats = 0
    for chat in chats:
        try:
            await _.unban_chat_member(chat, user_id)
            number_of_chats += 1
            await asyncio.sleep(1)
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except Exception:
            pass   
    ungban_time = get_readable_time((time.time() - start_time))
    await message.reply_text(f"**Removed Global Ban From User ID :** `{user_id}`")
    
@app.on_message(filters.command("gbanlist"))
async def _gbanlist(_, message):
    if message.from_user.id not in SUPREME_USERS:
        return await message.reply_text("**You Don't Have Access To This Command.**")
    gbanlist = await get_gbans_list()
    if not gbanlist:
        return await message.reply_text("**There Is No Gbannned Users.**")
    msg = "**♠ Global Ban List ♠\n**"
    for i in gbanlist:
        user = await _.get_users(int(i))
        msg += f"• {user.mention} - {user.id}\n"
    with BytesIO(str.encode(msg)) as output:
        output.name = "gbanlist.txt"
        await message.reply_document(            
            document = output,
            caption="**Gban List.**")
