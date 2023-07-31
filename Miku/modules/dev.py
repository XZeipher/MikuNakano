import os
import asyncio 
import subprocess
from os import remove
from os import system as execute
from Miku import app,BOT_NAME
from config import *
from pyrogram import filters,enums,Client
from contextlib import suppress
from pyrogram.errors import BadRequest ,Unauthorized
from Miku.utils.pastebin import paste
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


@Client.on_message(filters.command(["leave","dleave"]) & filters.user(DEV_USERS))
async def _leave(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Provide ID To Leave.**")
    user_id = message.from_user.id
    chat_id = message.text.split(None,1)[1].strip()
    if chat_id.startswith("-100"):       
        chat_id = int(chat_id)        
    else:
        return await message.reply_text("**Provide Valid ID.**")
    if message.command[0] == "leave":
        try:    
            await app.leave_chat(chat_id)
        except Exception as ilo:
            return await message.reply_text(f"**Error:** {ilo}")
        with suppress(Unauthorized):
            return await app.send_message(user_id,"ʙᴇᴇᴘ ʙᴏᴏᴘ, I ʟᴇғᴛ ᴛʜᴀᴛ sᴏᴜᴘ!.")
    if message.command[0] == "dleave":
        try:    
            await app.leave_chat(chat_id,delete=True)
        except Exception as ex:
            return await message.reply_text(f"**Error:** {ex}")
        with suppress(Unauthorized):
            return await app.send_message(user_id,"ʙᴇᴇᴘ ʙᴏᴏᴘ, I ʟᴇғᴛ ᴛʜᴀᴛ sᴏᴜᴘ!. ᴀʟsᴏ ᴅᴇʟᴇᴛᴇᴅ ᴛʜᴇ ᴅɪᴀʟᴏɢs.")


@Client.on_message(filters.command("restart") & filters.user(DEV_USERS))
async def _restart(_, message):
    text = await message.reply("**Restarting....**")
    await text.delete()
    try:
        os.system(f"kill -9 {os.getpid()} && tmux && python3 -m Miku")
    except Exception as er:
        print(er)


def update_repo(path : str, git_token : str, git_username : str, repo_name : str):
    try : 
        subprocess.check_output(f'cd {path}', shell=True)
        k = subprocess.check_output(f'git pull https://{git_token}@github.com/{git_username}/{repo_name}.git', shell=True)
        print(k.decode("utf-8"))
        return "Sucess! Updated the Repo"
    except Exception as e:
        return e
        
@Client.on_message(filters.command(["gitpull", "update"]) & filters.user(DEV_USERS))
async def _gitpull(_, message):
   # m = subprocess.check_output(["git", "pull"]).decode("UTF-8")
   # if str(m[0]) != "A":
        y = update_repo("MikuNakano","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","PrincesssGirlXD","MikuNakano")
        x = await message.reply_text("**Updating....**")
        os.system(f"kill -9 {os.getpid()} && python3 -m Miku")
        await message.reply_text(y)
  #  else:
  #      await message.reply_text(f"**» {BOT_NAME} ɪs ᴀʟʀᴇᴀᴅʏ ᴜᴩ-ᴛᴏ-ᴅᴀᴛᴇ !**")

@Client.on_message(filters.command("logs") & filters.user(DEV_USERS))
async def _logs(_, message):
    x = subprocess.getoutput("tail log.txt")
    link = await paste(x)
    await message.reply_text("**Here Is Your Logs.**",
                       reply_markup=InlineKeyboardMarkup([[
                           InlineKeyboardButton("Logs", url=link),
                           InlineKeyboardButton("Send", callback_data="send_logs")
                       ]]))        

@Client.on_callback_query(filters.regex("send_logs"))
async def semdd(_, query):
    await query.message.edit("**Sent Logs as file**")
    await _.send_document(query.message.chat.id, "log.txt")

@Client.on_message(filters.command("backup") & filters.user(DEV_USERS))
async def backup(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply("**This Command Can Only Be Used In PM.**")

    m = await message.reply("**Importing...**")

    code = execute(f'mongodump --uri "{MONGO_DB_URL}"')
    if int(code) != 0:
        return await m.edit(
            "**Looks like you don't have mongo-database-tools installed **"
            + "**grab it from mongodb.com/try/download/database-tools**"
        )

    code = execute("zip backup.zip -r9 dump/*")
    if int(code) != 0:
        return await m.edit(
            "**Looks like you don't have `zip` package installed, BACKUP FAILED!**"
        )

    await message.reply_document("backup.zip")
    await m.delete()
    remove("backup.zip")



__mod_name__ = "Development"

__help__ = """
**These Are Developer Commands None Of Your Business.**

**Commands**

 `/leave` : leave any chat through id.
 `/restart` : restart bot's instance.
 `/gitpull` : upgrade source code.
 `/backup` : get backup repository of this bot.

"""
