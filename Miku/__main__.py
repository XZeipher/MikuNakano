import os
import asyncio
import re
import time
import uvloop
import platform
import random 
import config
import strings
import importlib
from pyrogram.types import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    CallbackQuery)

from pyrogram.errors import BadRequest,Unauthorized 
from pyrogram import filters,idle , Client
from Miku.utils.misc import paginate_modules
from Miku import *
from Miku.modules.mongo.users_db import add_served_user
from fuzzywuzzy import process
from rich.table import Table
from pyrogram.enums import ParseMode,ChatType
from pyrogram import __version__ as pyrover
from Miku.modules import ALL_MODULES
from Miku.modules.rules import send_rules
from unidecode import unidecode
from Miku import StartTime , get_readable_time
MIKU_IMG = (
      "https://telegra.ph/file/624831b44a6e36370ec70.jpg",
      "https://telegra.ph/file/b9c7fb4d2dc481104fe49.jpg",
      "https://telegra.ph/file/02fd7a43fbce78c21c3dd.jpg",
      "https://telegra.ph/file/2c662cf6276379eaf10db.jpg",
      "https://telegra.ph/file/7bce7f2e2aedc3f048737.jpg",
)

MIKU_N_IMG = (
      "https://telegra.ph/file/837c61d9c51236fea4100.jpg",
      "https://telegra.ph/file/ee34cf0d7e4782424b777.jpg",
      "https://telegra.ph/file/5410b02359a2cabc2776b.jpg",
      "https://telegra.ph/file/b1fc3b2af759999bf3b35.jpg",
      "https://telegra.ph/file/305b5b3c4527cd439b926.jpg"

)

PM_PHOTO = (
      "https://telegra.ph/file/3f06de01df5bc3c3cf343.jpg",
      "https://telegra.ph//file/88976abda0d0af9d4a517.jpg",
      "https://telegra.ph//file/b388f473ddfb9cc727bb1.jpg",
)

loop = asyncio.get_event_loop() 
uptime = get_readable_time((time.time() - StartTime))
IMPORTED = {}
HELPABLE = {}
MODULES = {}
async def main():
    global IMPORTED, HELPABLE, MODULES
    for module_name in ALL_MODULES:
        imported_module = importlib.import_module("Miku.modules." + module_name)
        try:
            MODULES[unidecode(imported_module.__mod_name__).lower()] = imported_module.__help__
        except Exception as e:
            print(e)
        if hasattr(imported_module, "__help__") and imported_module.__help__:
            HELPABLE[imported_module.__mod_name__.lower()] = imported_module
        if hasattr(imported_module, "get_help") and imported_module.get_help:
            HELPABLE[imported_module.__mod_name__.lower()] = imported_module
    header = Table(show_header=True, header_style="bold yellow")
    header.add_column(strings.LOG_MSG)
    LOG.print(header)
    await asyncio.sleep(2)
    LOG.print("Access Modules:- ".format(len(ALL_MODULES)) + "\n")
    for all_module in ALL_MODULES:
        LOG.print(f"Successfully Imported {all_module}.py")

    print()
    LOG.print(f"{BOT_NAME} Started. ")
    try:
        await app.send_photo(f"@{config.SUPPORT_CHAT}",
                             photo=random.choice(MIKU_N_IMG),
                             caption=strings.SUPPORT_SEND_MSG.format(platform.python_version(), pyrover, uptime)
                             )
    except Exception as e:
        LOG.print(f"{e}")
        LOG.print(f"Bot isn't able to send message to @{config.SUPPORT_CHAT} !")
    try:
        await ubot.send_message(f"@{config.SUPPORT_CHAT}", "**Userbot Started.**")
    except Exception as u:
        LOG.print(f"{u}")
        LOG.print(f"Userbot isn't able to send message to @{config.SUPPORT_CHAT} !")
    await idle()

      
    
           
         
if __name__ == "__main__" :
    uvloop.install()
    loop.run_until_complete(main())
    LOG.print("Stopped Client.") 
