import os
import time
import random
import psutil
import strings
import platform
from pyrogram import filters , __version__ as pyro , Client , enums 
from Miku import app,StartTime,BOT_NAME,get_readable_time,BOT_USERNAME
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery 
from .pyro.decorators import control_user
                       
STATS_MSG="""
────「 Miku Nakano 遠ゲ 」────

• Uptime : {}
• Bot : {} MB
• Ram : {}%
• Disk : {}%
• Processor : {}
• Server : {}
"""

@app.on_callback_query(filters.regex("friday_back"))
@control_user()
async def Friday(_, callback_query : CallbackQuery):
    query= callback_query.message
    first_name=callback_query.from_user.first_name
    uptime= get_readable_time((time.time() - StartTime))
    await query.edit_caption(strings.PM_START_TEXT.format(BOT_NAME,mention,uptime,platform.python_version(),pyro),
    reply_markup=InlineKeyboardMarkup(strings.START_BUTTONS))

@app.on_callback_query(filters.regex("Friday_st"))
@control_user()
async def Fridays(client, callback_query : CallbackQuery):    
    uptime= get_readable_time((time.time() - StartTime))   
    ram = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    process = psutil.Process(os.getpid())
    processor = platform.processor()
    server = platform.system()
    mb= round(process.memory_info()[0] / 1024 ** 2)
    await client.answer_callback_query(
    callback_query.id,
    text=STATS_MSG.format(uptime,mb,ram,disk,processor,server),
    show_alert=True
)


@app.on_callback_query(filters.regex("admin_close"))
@control_user()
async def _close(client : Client, query: CallbackQuery):
    chat_id = query.message.chat.id
    user_id = query.from_user.id
    member = await client.get_chat_member(chat_id,user_id)
    if member.privileges:
            await query.message.delete()
            try:
                await query.message.reply_to_message.delete()
            except:
                pass
    else:
        await client.answer_callback_query(
        query.id,
        text = "You Don't Have Permission To Do This.",
        show_alert = True)
