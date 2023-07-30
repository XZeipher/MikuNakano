import re
import time

from pyrogram import filters , Client
from pyrogram.types import Message

from Miku import app,BOT_USERNAME,get_readable_time
from Miku.modules.mongo.afk_db import is_afk,remove_afk
from pyrogram.enums import MessageEntityType 
from Miku.utils.filter_groups import afk_watcher

un = None
@Client.on_message(
     ~filters.me & ~filters.bot & ~filters.via_bot,
    group=afk_watcher,
)
async def chat_watcher_func(_, message):
    global un
    if not un:
        un = (await _.get_me()).username
    if message.sender_chat:
        return
    userid = message.from_user.id
    user_name = message.from_user.mention
    ntg = message.text
    try:
        if ntg.split()[0].lower() in ["/afk", f"/afk@{un}".lower(),"brb"]:
            return
    except:
        pass

    msg = ""
    replied_user_id = 0

    verifier, reasondb = await is_afk(userid)
    if verifier:
        await remove_afk(userid)
        try:
            afktype = reasondb["type"]
            timeafk = reasondb["time"]
            data = reasondb["data"]
            reasonafk = reasondb["reason"]
            seenago = get_readable_time((int(time.time() - timeafk)))
            if afktype == "text":
                msg += f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`.\n"
            if afktype == "text_reason":
                msg += f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`\n**Reason:** `{reasonafk}`\n"
            if afktype == "animation":
                if str(reasonafk) == "None":
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`\n",
                    )
                else:
                    send = await message.reply_animation(
                        data,
                        caption=f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                    )
            if afktype == "photo":
                if str(reasonafk) == "None":
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`\n",
                    )
                else:
                    send = await message.reply_photo(
                        photo=f"downloads/{userid}.jpg",
                        caption=f"**{user_name[:25]} Is Back Online.\nYou Were Afk For** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                    )
        except:
            msg += f"**{user_name[:25]} Is Back Online.**\n"
        
    # Replied to a User which is AFK
    if message.reply_to_message:
        try:
            replied_first_name = (
                message.reply_to_message.from_user.mention
            )
            replied_user_id = message.reply_to_message.from_user.id
            verifier, reasondb = await is_afk(replied_user_id)
            if verifier:
                try:
                    afktype = reasondb["type"]
                    timeafk = reasondb["time"]
                    data = reasondb["data"]
                    reasonafk = reasondb["reason"]
                    seenago = get_readable_time(
                        (int(time.time() - timeafk))
                    )
                    if afktype == "text":
                        msg += f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n"
                    if afktype == "text_reason":
                        msg += f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n"
                    if afktype == "animation":
                        if str(reasonafk) == "None":
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                            )
                        else:
                            send = await message.reply_animation(
                                data,
                                caption=f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                            )
                    if afktype == "photo":
                        if str(reasonafk) == "None":
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                            )
                        else:
                            send = await message.reply_photo(
                                photo=f"downloads/{replied_user_id}.jpg",
                                caption=f"**{replied_first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                            )
                except Exception as e:
                    msg += f"**{replied_first_name} Is Afk**\n"
        except:
            pass

    # If username or mentioned user is AFK
    if message.entities:
        entity = message.entities
        j = 0
        for x in range(len(entity)):
            if (entity[j].type) == MessageEntityType.MENTION:
                found = re.findall("@([_0-9a-zA-Z]+)", message.text)
                try:
                    get_user = found[j]
                    user = await app.get_users(get_user)
                    if user.id == replied_user_id:
                        j += 1
                        continue
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user.id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n"
                        if afktype == "text_reason":
                            msg += f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason** `{reasonafk}`\n\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user.id}.jpg",
                                    caption=f"**{user.first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                                )
                    except:
                        msg += (
                            f"**{user.first_name[:25]} Is Afk.**\n"
                        )
            elif (entity[j].type) == MessageEntityType.TEXT_MENTION:
                try:
                    user_id = entity[j].user.id
                    if user_id == replied_user_id:
                        j += 1
                        continue
                    first_name = entity[j].user.first_name
                except:
                    j += 1
                    continue
                verifier, reasondb = await is_afk(user_id)
                if verifier:
                    try:
                        afktype = reasondb["type"]
                        timeafk = reasondb["time"]
                        data = reasondb["data"]
                        reasonafk = reasondb["reason"]
                        seenago = get_readable_time(
                            (int(time.time() - timeafk))
                        )
                        if afktype == "text":
                            msg += f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n"
                        if afktype == "text_reason":
                            msg += f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n"
                        if afktype == "animation":
                            if str(reasonafk) == "None":
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                                )
                            else:
                                send = await message.reply_animation(
                                    data,
                                    caption=f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                                )
                        if afktype == "photo":
                            if str(reasonafk) == "None":
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n",
                                )
                            else:
                                send = await message.reply_photo(
                                    photo=f"downloads/{user_id}.jpg",
                                    caption=f"**{first_name[:25]} Is Afk.\nLast Seen** `{seenago}`\n**Reason:** `{reasonafk}`\n",
                                )
                    except:
                        msg += f"**{first_name[:25]} Is Afk**\n"
            j += 1
    if msg != "":
        try:
            send =  await message.reply_text(
                msg, disable_web_page_preview=True
            )
        except:
            return
    
