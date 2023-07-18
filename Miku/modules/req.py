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

xd = {}
administrators = []
ids = []

@app.on_message(filters.group & filters.command("request"))
async def requests(client, message):
    msg_id = message.id
    user = await client.get_users(message.from_user.id)
    if len(message.text.split()) < 2:
        return await message.reply_text("**Wrong format!**")
    anime = " ".join(message.text.split()[1:])
    try:
        chat = await client.get_chat(CHANNEL)
        administrators.clear()

        async for m in client.get_chat_members(CHANNEL, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(m)
        ids.clear()
        for i in administrators:
            userid = i.user.id
            ids.append(userid)

    except Exception as e:
        return await message.reply_text(str(e))

    log_butt = [
        [
            InlineKeyboardButton("Accept", callback_data=f"accept_{msg_id}"),
            InlineKeyboardButton("Reject", callback_data=f"reject_{msg_id}"),
        ],
        [
            InlineKeyboardButton("Requested Message", url=f"{message.link}")
        ],
    ]
    log_message = await client.send_message(CHANNEL, LOG.format(req_id=msg_id, tracking_id=msg_id, requested_by=user.mention, requested=anime), reply_markup=InlineKeyboardMarkup(log_butt))
    req_butt = [
        [
            InlineKeyboardButton("Request Log", url=f"t.me/c/{str(log_message.chat.id)[4:]}/{log_message.id}")
        ],
    ]

    req_message = await message.reply_text(REQ.format(req_id=msg_id, tracking_id=msg_id, requested_by=user.mention, requested=anime), reply_markup=InlineKeyboardMarkup(req_butt))
    xd[msg_id] = {
        "log_message": log_message,
        "requested": anime,
        "requested_by": user.mention
    }

@app.on_callback_query()
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    if user_id not in ids:
        await callback_query.answer("You can't use this action.", show_alert=True)
        return

    data = callback_query.data
    action, msg_id = data.split("_")

    if action == "accept":
        log_message = xd[msg_id]["log_message"]
        await log_message.edit_text(
            f"ACCEPTED\n"
            f"┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣━➤「Tracking ID」: {mag_id}\n"
            f"┣━➤「Requested By」: {xd[msg_id]['requested_by']}\n"
            f"┣━➤「Requested」: {xd[msg_id]['requested']}\n"
            f"┗━━━━━━━━━━━━━━━━━━━"
        )
        xd.pop(msg_id)
    elif action == "reject":
        log_message = xd[msg_id]["log_message"]
        await log_message.edit_text(
            f"REJECTED\n"
            f"┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣━➤「Tracking ID」: {msg_id}\n"
            f"┣━➤「Requested By」: {xd[msg_id]['requested_by']}\n"
            f"┣━➤「Requested」: {xd[msg_id]['requested']}\n"
            f"┗━━━━━━━━━━━━━━━━━━━"
        )
        xd.pop(message_id)
