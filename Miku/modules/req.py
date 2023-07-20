from pyrogram import *
from Miku import app
from pyrogram.types import *
from pyrogram.raw import *
from pyrogram import __version__ as pyro_version

CHANNEL = "@ocean_request_channel"
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
accept = """
**Request Details**
┏━━━━━━━━━━━━━━━━━━━
┣━➤「Tracking ID」: `{}`
┣━➤「Requested」: {}
┣━➤「Requested By」: {}
┣━➤「Status」: accepted 
┗━━━━━━━━━━━━━━━━━━━"""
reject = """
**Request Details** 
┏━━━━━━━━━━━━━━━━━━━
┣━➤「Tracking ID」: `{}`
┣━➤「Requested」: {}
┣━➤「Requested By」: {}
┣━➤「Status」: rejected
┗━━━━━━━━━━━━━━━━━━━"""
unable = """
**Request Details** 
┏━━━━━━━━━━━━━━━━━━━
┣━➤「Tracking ID」: `{}`
┣━➤「Requested」: {}
┣━➤「Requested By」: {}
┣━➤「Status」: unavailable
┗━━━━━━━━━━━━━━━━━━━"""
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
            InlineKeyboardButton("Unavailable", callback_data=f"unable_{msg_id}")
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
        "requested_by": user.mention,
        "username": user.username
    }

@app.on_callback_query(filters.regex(r"^(accept|reject|unable)$"))
async def handle_callback(client, callback_query):
    user_id = callback_query.from_user.id
    

    data = callback_query.data
    action, msg_id = data.split("_")

    if action == "accept":
        if user_id not in ids:
            await callback_query.answer("You can't use this action.", show_alert=True)
            xd.clear()
            return
        first_id = next(iter(xd))
        log_id = xd[first_id]['log_message'].id
        mention = xd[first_id]['requested_by']
        request = xd[first_id]['requested']
        username = xd[first_id]['username']
        await client.edit_message_text(CHANNEL, log_id,
            f"**ACCEPTED\n**"
            f"┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣━➤「Tracking ID」: {first_id}\n"
            f"┣━➤「Requested By」: {mention}\n"
            f"┣━➤「Requested」: {request}\n"
            f"┗━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(username, accept.format(first_id, request, mention))
        xd.clear()
    elif action == "reject":
        if user_id not in ids:
            await callback_query.answer("You can't use this action.", show_alert=True)
            xd.clear()
            return
        first_id = next(iter(xd))
        log_id = xd[first_id]['log_message'].id
        mention = xd[first_id]['requested_by']
        request = xd[first_id]['requested']
        username = xd[first_id]['username']
        await client.edit_message_text(CHANNEL, log_id,
            f"**REJECTED\n**"
            f"┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣━➤「Tracking ID」: {first_id}\n"
            f"┣━➤「Requested By」: {mention}\n"
            f"┣━➤「Requested」: {request}\n"
            f"┗━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(username, reject.format(first_id, request, mention))
        xd.clear()
    elif action == "unable":
        if user_id not in ids:
            await callback_query.answer("You can't use this action.", show_alert=True)
            xd.clear()
            return
        first_id = next(iter(xd))
        log_id = xd[first_id]['log_message'].id
        mention = xd[first_id]['requested_by']
        request = xd[first_id]['requested']
        username = xd[first_id]['username']
        await client.edit_message_text(CHANNEL, log_id,
            f"**UNAVAILABLE\n**"
            f"┏━━━━━━━━━━━━━━━━━━━\n"
            f"┣━➤「Tracking ID」: {first_id}\n"
            f"┣━➤「Requested By」: {mention}\n"
            f"┣━➤「Requested」: {request}\n"
            f"┗━━━━━━━━━━━━━━━━━━━"
        )
        await client.send_message(username, unable.format(first_id, request, mention))
        xd.clear()
