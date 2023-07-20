from pyrogram import filters
from Miku import app
from config import SUPPORT_CHAT
from Miku.modules.mongo.users_db import *
from Miku.modules.mongo.chats_db import *

LOG = "@MikuLog"
us = """
#MIKU
#NEW_USER

New User Started The Bot

ID: {}
User: {}
"""
ch = """
#MIKU
#NEWGROUP        

Bot Has Been Added To New Group
                 
Group Name: {}              
ID:  {}               
Username: {}             
"""

@app.on_message(filters.command("start"))
async def private_handle(client, message):
    user_id = message.from_user.id
    users = await get_served_users()  
    try:
        if user_id not in users:
            mention = message.from_user.mention  
            await add_served_user(user_id)
            await client.send_message(LOG, us.format(user_id, mention))
        else:
            pass
    except Exception as e:
        await client.send_message(LOG, str(e))  

@app.on_message(filters.group)
async def group_handle(client, message):  
    chat_id = message.chat.id
    chats = await get_served_chats()  
    try:
        if chat_id not in chats:
            group = message.chat  
            await add_served_chat(chat_id)
            await client.send_message(LOG, ch.format(group.title, group.id, group.username))
        else:
            pass
    except Exception as a:
        await client.send_message(LOG, str(a))  
