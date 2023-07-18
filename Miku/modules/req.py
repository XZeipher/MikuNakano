from pyrogram import *
from Miku import app
from pyrogram.types import *
from pyrogram.raw import *
from pyrogram import __version__ as pyro_version

CHANNEL = "@mikulogsab"

REQ = """
**Your Request Received #{req_id}**
┏━━━━━━━━━━━━━━━━━━━
┣━➤「Tracking ID」: `{tracking_id}`
┣━➤「Requested By」: {requested_by}
┣━➤「Requested」: `{requested}`
┗━━━━━━━━━━━━━━━━━━━ 

**Note -** `It takes up to 72 hours to process your request`"""

LOG = """
**New Request Received #{req_id}**
┏━━━━━━━━━━━━━━━━━━━
┣━➤「Tracking ID」: `{tracking_id}`
┣━➤「Requested By」: {requested_by}
┣━➤「Requested」: `{requested}`
┗━━━━━━━━━━━━━━━━━━━
"""

request_messages = {}
administrators = []

@app.on_message(filters.group & filters.regex("\\#request"))
async def requests(client, message):
    user = await client.get_users(message.from_user.id)
    if len(message.text) < 3:
        return await message.reply_text("**Wrong format!**")
    anime = message.text.split(maxsplit=1)[1]
    try:
        chat = await client.get_chat(CHANNEL)
        administrators.clear()

        async for m in client.get_chat_members(CHANNEL, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(m)
    except:
        return await message.reply_text("**Failed Maybe I Am Banned Or Chat Deleted!**")

    log_butt = [
        [
            InlineKeyboardButton("Accept", callback_data=f"accept_{message.id}"),
            InlineKeyboardButton("Reject", callback_data=f"reject_{message.id}"),
        ],
        [
            InlineKeyboardButton("Requested Message", url=f"{message.link}")
        ],
    ]
    req_butt = [
        [
            InlineKeyboardButton("Request Log", url=f"https://t.me/c/{CHANNEL}/{message.id}")
        ],
    ]
    log_message = await client.send_message(CHANNEL, LOG.format(req_id=message.id, tracking_id=message.id, requested_by=user.mention, requested=anime), reply_markup=InlineKeyboardMarkup(log_butt))
    req_message = await message.reply_text(REQ.format(req_id=message.id, tracking_id=message.id, requested_by=user.mention, requested=anime), reply_markup=InlineKeyboardMarkup(req_butt))
    
    request_messages[message.id] = {
        "log_message": log_message,
        "req_message": req_message
    }

@app.on_callback_query()
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in administrators:
        await callback_query.answer("You can't use this action.", show_alert=True)
        return

    data = callback_query.data
    action, message_id = data.split("_")

    if action == "accept":
        await callback_query.answer("Request accepted.")
        log_message = request_messages[int(message_id)]["log_message"]
        await client.edit_message_text(log_message.chat.id, log_message.message_id, text=f"Request #{message_id} has been accepted.")
    elif action == "reject":
        await callback_query.answer("Request rejected.")
        log_message = request_messages[int(message_id)]["log_message"]
        await client.edit_message_text(log_message.chat.id, log_message.message_id, text=f"Request #{message_id} has been rejected.")
