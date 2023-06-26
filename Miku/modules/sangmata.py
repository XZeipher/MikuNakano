from Miku import ubot, app, BOT_ID
from pyrogram import *
import time

FORWARD_CHAT_ID = -1001813613591

@ubot.on_message(filters.command("check_name") & filters.group)
async def userbot(client, message):
    global chat_id
    chat_id = message.chat.id
    user_id = message.reply_to_message.from_user.id
    await client.send_message(5422359176, user_id)


@ubot.on_message(filters.private & filters.user(5422359176) & filters.text)
async def newtext(client, message):
    bruh = message.text
    await client.forward_messages(chat_id=FORWARD_CHAT_ID, from_chat_id=message.chat.id, message_ids=message.message_id)


@app.on_message(filters.command("check_name") & filters.group)
async def pyrobot(client, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text("**Reply To A User To Get Previous Names.**")
    if replied.from_user.id == BOT_ID:
        return await message.reply_text("**You Can't Extract My Name.**")
