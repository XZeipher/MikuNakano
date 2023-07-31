import os
from Miku import app, db, BOT_ID, ubot
from config import OWNER_ID, SUPREME_USERS, SUPREME_USERS as CHAD, DEV_USERS
from pyrogram import filters, enums , Client as v
from Miku.modules.pyro.extracting_id import extract_user_id
from Miku.modules.mongo.afk_db import is_user_afk
from pyrogram.errors import BadRequest
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from Miku.modules.mongo.users_info_db import *
from Miku.modules.mongo.gbans_db import is_gbanned_user, get_gban_reason

btn = InlineKeyboardMarkup([[InlineKeyboardButton("➕ Add Me To Your Group ➕", url="https://t.me/MikuNakanoXBot?startgroup=true")]])

@v.on_message(filters.command("info") & filters.private)
async def _info(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        user_id = message.from_user.id

    msg = await message.reply("**Miku Initialisation.....**")
    try:
        user = await _.get_users(user_id)
    except Exception as e:
        if user_id:
            return await msg.edit("**Provide Username Or Tag The User!**")
        mx = message.text.split(maxsplit=1)[1]
        if not mx.startswith("@"):
            return await msg.edit("**Provide Username Or Tag The User!**")
        if mx.startswith("@"):
            user = await ubot.get_users(mx)
            user_id = user.id
        if message.reply_to_message:
            username = message.reply_to_message.username
            user = await ubot.get_users(username)
            user_id = user.id

    text = "━━━━━━ [INFORMATION] ━━━━━━━\n"
    text += f"**• ID :** `{user_id}`\n"
    text += f"**• First Name :** `{user.first_name}`\n"
    if user.last_name:
        text += f"**• Last Name :** `{user.last_name}`\n"
    if user.username:
        text += f"**• Username :** @{user.username}\n"
    text += f"**• Profile :** {user.mention}\n"
    text += f"**• Premium :** {user.is_premium}\n"
    text += f"**• Gbanned :** {str(await is_gbanned_user(user_id))}\n"

    if message.chat.type != enums.ChatType.PRIVATE:
        ptext = "**• Status :** `{}`\n"

        if await is_user_afk(user_id):
            text += ptext.format("Afk")
        else:
            try:
                member = await _.get_chat_member(message.chat.id, user_id)
                if member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                    text += ptext.format("Not Here")
                if member.status == enums.ChatMemberStatus.MEMBER:
                    text += ptext.format("Member")
                if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                    text += ptext.format("Administrator")
            except BadRequest:
                text += ptext.format("Not Here")

    try:
        mm = await _.get_chat_member(message.chat.id, user_id)
        if mm.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and mm.custom_title:
            text += f"**• Title :** `{mm.custom_title}`\n"
    except:
        pass

    reason = await get_gban_reason(user_id)
    if reason:
        text += f"**• Gban Reason :** `{reason}`\n"

    if user.status:
        text += f"**• Last Seen :** `{user.status}`\n"

    if user_id == OWNER_ID:
        text += "\n**Creator Alpha Coder !!!**"
    elif user_id in SUPREME_USERS:
        text += "\n**This Is Bot Admin**"
    elif user_id in CHAD:
        text += "\n**This Is Sun User**"
    elif user_id == 2027056490 or user_id == 6396522589:
        text += "\n**Alpha's Daughter!!!**"

    if user.photo:
        pic = await _.download_media(user.photo.big_file_id)
        await _.send_photo(message.chat.id, photo=pic, caption=text, reply_markup=btn)
        os.remove(pic)
    else:
        await _.send_message(message.chat.id, text, reply_markup=btn)

    await msg.delete()
@v.on_message(filters.command("info") & filters.group,group=69)
async def _info(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        user_id = message.from_user.id

    msg = await message.reply("**Miku Initialisation.....**")
    try:
        user = await _.get_users(user_id)
    except Exception as e:
        if user_id:
            return await msg.edit("**Provide Username Or Tag The User!**")
        mx = message.text.split(maxsplit=1)[1]
        if not mx.startswith("@"):
            return await msg.edit("**Provide Username Or Tag The User!**")
        if mx.startswith("@"):
            user = await ubot.get_users(mx)
            user_id = user.id
        if message.reply_to_message:
            username = message.reply_to_message.username
            user = await ubot.get_users(username)
            user_id = user.id

    text = "━━━━━━ [INFORMATION] ━━━━━━━\n"
    text += f"**• ID :** `{user_id}`\n"
    text += f"**• First Name :** `{user.first_name}`\n"
    if user.last_name:
        text += f"**• Last Name :** `{user.last_name}`\n"
    if user.username:
        text += f"**• Username :** @{user.username}\n"
    text += f"**• Profile :** {user.mention}\n"
    text += f"**• Premium :** {user.is_premium}\n"
    text += f"**• Gbanned :** {str(await is_gbanned_user(user_id))}\n"

    if message.chat.type != enums.ChatType.PRIVATE:
        ptext = "**• Status :** `{}`\n"

        if await is_user_afk(user_id):
            text += ptext.format("Afk")
        else:
            try:
                member = await _.get_chat_member(message.chat.id, user_id)
                if member.status in [enums.ChatMemberStatus.LEFT, enums.ChatMemberStatus.BANNED]:
                    text += ptext.format("Not Here")
                if member.status == enums.ChatMemberStatus.MEMBER:
                    text += ptext.format("Member")
                if member.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER]:
                    text += ptext.format("Administrator")
            except BadRequest:
                text += ptext.format("Not Here")

    try:
        mm = await _.get_chat_member(message.chat.id, user_id)
        if mm.status in [enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.OWNER] and mm.custom_title:
            text += f"**• Title :** `{mm.custom_title}`\n"
    except:
        pass

    reason = await get_gban_reason(user_id)
    if reason:
        text += f"**• Gban Reason :** `{reason}`\n"

    if user.status:
        text += f"**• Last Seen :** `{user.status}`\n"

    if user_id == OWNER_ID:
        text += "\n**Creator Alpha Coder !!!**"
    elif user_id in SUPREME_USERS:
        text += "\n**This Is Bot Admin**"
    elif user_id in CHAD:
        text += "\n**This Is Sun User**"
    elif user_id == 2027056490 or user_id == 6396522589:
        text += "\n**Alpha's Daughter!!!**"

    if user.photo:
        pic = await _.download_media(user.photo.big_file_id)
        await _.send_photo(message.chat.id, photo=pic, caption=text, reply_markup=btn)
        os.remove(pic)
    else:
        await _.send_message(message.chat.id, text, reply_markup=btn)

    await msg.delete()

@v.on_message(filters.command("ginfo"))
async def _ginfo(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Give me Chat ID or Username to fetch info!**")

    arg = message.command[1]
    chat_id = int(arg) if arg.isdigit() else str(arg)

    try:
        chat = await _.get_chat(chat_id)
        administrators = []

        async for m in _.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            administrators.append(m)
    except:
        return await message.reply_text("**Failed Maybe I Am Banned Or Chat Deleted!**")

    text = f"**ID :** `{chat.id}`\n"
    text += f"**Title :** `{chat.title}`\n"
    text += f"**Type :** `{str(chat.type)[9:]}`\n"
    text += f"**Restrictions :** `{chat.is_restricted}`\n"
    text += f"**Scam :** `{chat.is_scam}`\n"

    if chat.username:
        text += f"** Username :** @{chat.username}\n"

    text += f"**Admins :** `{len(administrators)}`\n"
    text += f"**Users :** `{chat.members_count}`\n\n"
    text += f"**Admins :-\n**"

    for i in administrators:
        if i.user.is_bot or i.user.is_deleted:
            continue
        text += f"\n• {i.user.mention}"

    await message.reply_text(text, reply_markup=btn)

@v.on_message(filters.command("gifid"))
async def _ginfo(_, message):
    replied = message.reply_to_message
    if replied and replied.animation:
        return await message.reply_text(f"**• ID :** `{replied.animation.file_id}`")
    return await message.reply_text("**Reply To Gif**")

@v.on_message(filters.command("setme") & filters.group)
async def _setme(_, message):
    user_id = message.from_user.id
    replied = message.reply_to_message
    if replied:
        user_id = replied.from_user.id
    if user_id in [777000, 1087968824]:
        return await message.reply_text("**Error Unauthorised!**")
    try:
        info = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("**Provide Text To Update Info.**")
    if len(info) > 70:
        return await message.reply_text(f"**Info needs to be under 70 characters. You are sending {len(info)} characters!**")
    await set_me(user_id, info)
    return await message.reply_text("**Info Updated!**")

@v.on_message(filters.command("me"))
async def _me(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        user_id = message.from_user.id
    mention = (await _.get_users(user_id)).mention
    info = await get_me(user_id)
    if not info:
        return await message.reply_text(f"**{mention} hasn't set an info about themselves!**")
    return await message.reply_text(f"**{mention} :**\n`{info}`")

@v.on_message(filters.command("setbio") & filters.group)
async def _setme(_, message):
    user_id = message.from_user.id
    replied = message.reply_to_message
    if replied:
        user_id = replied.from_user.id
    if user_id in [777000, 1087968824]:
        return await message.reply_text("**Error Unauthorised!**")
    try:
        bio = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply_text("**Provide Text To Update Info.**")
    if len(bio) > 70:
        return await message.reply_text(f"**The Bio needs to be under 70 characters. You gave {len(bio)} characters!**")
    await set_bio(user_id, bio)
    return await message.reply_text("**Info Updated!**")

@v.on_message(filters.command("bio"))
async def _me(_, message):
    user_id = await extract_user_id(message)
    if not user_id:
        user_id = message.from_user.id
    mention = (await _.get_users(user_id)).mention
    bio = await get_bio(user_id)
    if not bio:
        return await message.reply_text(f"**{mention} hasn't set an info message about themselves!**")
    return await message.reply_text(f"**{mention} :**\n`{bio}`")
