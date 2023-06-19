from os import remove
from pyrogram import filters, enums 
from Miku import arq, app
from config import SUPREME_USERS as CHAD
from Miku.modules.mongo.antinsfw_db import is_nsfw_on, nsfw_off, nsfw_on
from Miku.modules.pyro.status import user_admin,user_can_change_info
from Miku.modules.mongo.approve_db import isApproved
from .pyro.decorators import control_user,command

async def get_file_id_from_message(message):
    file_id = None
    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
async def detect_nsfw(_, message):
    chat_id = message.chat.id
    if not await is_nsfw_on(message.chat.id):
        return
    if not message.from_user:
        return
    user = message.from_user
    xx = await _.get_chat_member(chat_id, user.id)
    if xx.privileges or user.id in SUPREME_USERS or await isApproved(chat_id, user.id):
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await app.download_media(file_id)    
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    print(results)
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw    
    if not nsfw:
        return
    try:
        await message.delete()
    except Exception:
        return
    await message.reply_text(
        f"""
**⚡ NSFW SECURITY SYSTEM ⚡**

**User:** {message.from_user.mention} [`{message.from_user.id}`]
**Safe:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Adult:** `{results.sexy} %`
**Hentai:** `{results.hentai} %`
**Drawings:** `{results.drawings} %`

"""
    )


@app.on_message(command(commands=("scan")))
@control_user()
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "**Reply To Scan.**"
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "**Reply To Scan.**"
        )
        return
    m = await message.reply_text("**Scanning...")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("**Media Invalid.**")
    file = await app.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        pass
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**Neutral:** `{results.neutral} %`
**Porn:** `{results.porn} %`
**Hentai:** `{results.hentai} %`
**Sexy:** `{results.sexy} %`
**Drawings:** `{results.drawings} %`
**NSFW:** `{results.is_nsfw}`
"""
    )


@app.on_message(command(commands=("antinsfw")))
@control_user()
@user_admin
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("**Usage:** `/antinsfw [on/off]`")
        return
    status = message.text.split(None, 1)[1].strip()
    status = status.lower()
    chat_id = message.chat.id
    if status in ("on", "yes"):
        await nsfw_on(chat_id)
        await message.reply_text(
            "**Enabled Anti NSFW Security.**"
        )
    elif status in ("off", "no"):
        await nsfw_off(chat_id)
        await message.reply_text("**Disabled Anti NSFW Security.**")
    else:
        await message.reply_text("**Use** `/antinsfw [on/off]`")


__help__ = """
**NSFW Security System Protects Your Group.**

**Commands**

♠ `/antinsfw [on/off]` - Detects NSFW Media's In Group.
"""
__mod_name__ = "NSFW-System"

