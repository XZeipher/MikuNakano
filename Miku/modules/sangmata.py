from Miku import ubot, app, BOT_ID
from pyrogram import *
import time

DICT = {}

@ubot.on_message(filters.command("check_name") & filters.group)
async def userbot(client, message):
    global user_id
    user_id = message.reply_to_message.from_user.id
    DICT[user_id] = {'text': None}
    await client.send_message(300860929, user_id)

@ubot.on_message(filters.private & filters.user(300860929) & filters.text)
async def newtext(client, message):
    if not DICT[user_id]:
        return
    DICT[user_id]['text'] = message.text

@app.on_message(filters.command("check_name") & filters.group)
async def pyrobot(client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text("**Reply To A User To Get Previous Names.**")
    if replied.from_user.id == BOT_ID:
        return await message.reply_text("**You Can't Extract My Name.**")
    c = await message.reply_text("**wait a moment...**")
    time.sleep(3)
    if not DICT[user_id]:
        return await c.edit_text("**Not Found.**")
    await c.edit_text(DICT[user_id]['text'])
    DICT.pop(user_id)
