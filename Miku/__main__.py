# Respect @ImmortalsXKing
# Don't Fking Remove Credits Else Gay

import asyncio
import importlib
import random
import re
import platform
import sys
import time
from contextlib import closing, suppress
from pyrogram import enums, filters, idle , __version__
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from uvloop import install
from Miku import BOT_NAME, BOT_USERNAME, LOG_GROUP_ID, aiohttpsession, app
from Miku.modules import ALL_MODULES
from Miku.modules.sudoers import bot_sys_stats
from Miku.utils import paginate_modules
from Miku.utils.constants import MARKDOWN
from Miku.utils.dbfunctions import clean_restart_stage
from Miku.utils import formatter

StartTime = time.time()
loop = asyncio.get_event_loop()

HELPABLE = {}
bot_start_time = time.time()
bot_uptime = int(time.time() - bot_start_time)

async def start_bot():
    global HELPABLE
    global BOT_ID
    global BOT_NAME
    global BOT_USERNAME
    global BOT_MENTION
    global BOT_DC_ID
    
    for module in ALL_MODULES:
        imported_module = importlib.import_module(f"Miku.modules.{module}")
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[imported_module.__MODULE__.lower()] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print("+===============================================================+")
    print("|                              Miku Nakano                           |")
    print("+===============+===============+===============+===============+")
    print(bot_modules)
    print("+===============+===============+===============+===============+")
    print(f"[INFO]: {BOT_NAME} Has Been Started!")

    restart_data = await clean_restart_stage()
    await app.start()
    x = app.get_me()
    BOT_ID = x.id
    BOT_NAME = x.first_name + (x.last_name or "")
    BOT_USERNAME = x.username
    BOT_MENTION = x.mention
    BOT_DC_ID = x.dc_id


    try:
        print("[INFO]: Sending Connection To Telegram!")
        await app.send_photo(LOG_GROUP_ID,photo="https://telegra.ph/file/378037bc2d59f232c6e8c.jpg", caption=f"**Miku Nakano !\nPython Version:** `v{platform.python_version()}`\n**Pyrogram Version:** `{__version__}`\n**UpTime:** `{formatter.get_readable_time((bot_uptime))}`",parse_mode=MARKDOWN)
    except Exception as e:
    	print(f"[ERROR]: {e}")

    await idle()

    await aiohttpsession.close()
    print("[INFO]: CLOSING AIOHTTP SESSION AND STOPPING BOT")
    await app.stop()
    for task in asyncio.all_tasks():
        task.cancel()
    print("[INFO]: Turned off tasks!")


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Commands", callback_data="bot_commands"
            ),
            InlineKeyboardButton(
                text="Support ",
                url="t.me/x",
            ),
        ],
        [
            InlineKeyboardButton(
                text="System Stats ðŸ–¥",
                callback_data="stats_callback",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Add Me To Your Groupâš¡",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
)

home_text_pm = """**
 {} 
Hola! {} ,
I am an Anime themed advance group management bot with a lot of Sexy Features 

 Uptime: {}
 Python: {}
 Pyrogram: {}

 Keep Your Group Secure From Spammers by Adding me **"""
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

keyboard = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="Support ",
                url=f"t.me/x",
            ),
            InlineKeyboardButton(
                text="Updates ",
                url="t.me/x",
            ),
        ],
        [
            InlineKeyboardButton(
                text="System Stats ðŸ’»",
                callback_data="stats_callback",
            ),
        ],
    ]
)


@app.on_message(filters.command("start"))
async def start(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        return await message.reply_photo(
            photo=random.choice(MIKU_IMG),
            caption=f"Hii {message.from_user.mention}, I'm here to help since: {formatter.get_readable_time((bot_uptime))} ",
            reply_markup=keyboard,
        )
    if len(message.text.split()) > 1:
        name = (message.text.split(None, 1)[1]).lower()
        if name == "mkdwn_help":
            await message.reply(
                MARKDOWN, parse_mode="html", disable_web_page_preview=True
            )
        elif "_" in name:
            module = name.split("_", 1)[1]
            text = (
                f"Here is the help for **{HELPABLE[module].__MODULE__}**:\n"
                + HELPABLE[module].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        elif name == "help":
            text, keyb = await help_parser(message.from_user.first_name)
            await message.reply(
                text,
                reply_markup=keyb,
            )
    else:
        await message.reply_photo(
            photo=random.choice(PM_PHOTO),
            caption=home_text_pm.format(BOT_NAME,message.from_user.mention,sys.version,__version__,formatter.get_readable_time((bot_uptime))),
            reply_markup=home_keyboard_pm,
        )
    return


@app.on_message(filters.command("help"))
async def help_command(_, message):
    if message.chat.type != enums.ChatType.PRIVATE:
        if len(message.command) >= 2:
            name = (message.text.split(None, 1)[1]).lower()
            if str(name) in HELPABLE:
                key = InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Click here",
                                url=f"t.me/{BOT_USERNAME}?start=help_{name}",
                            )
                        ],
                    ]
                )
                await message.reply(
                    f"Click on the below button to get help about {name}",
                    reply_markup=key,
                )
            else:
                await message.reply(
                    "PM Me For More Details.", reply_markup=keyboard
                )
        else:
            await message.reply(
                "Pm Me For More Details.", reply_markup=keyboard
            )
    elif len(message.command) >= 2:
        name = (message.text.split(None, 1)[1]).lower()
        if str(name) in HELPABLE:
            text = (
                f"Here is the help for **{HELPABLE[name].__MODULE__}**:\n"
                + HELPABLE[name].__HELP__
            )
            await message.reply(text, disable_web_page_preview=True)
        else:
            text, help_keyboard = await help_parser(
                message.from_user.first_name
            )
            await message.reply(
                text,
                reply_markup=help_keyboard,
                disable_web_page_preview=True,
            )
    else:
        text, help_keyboard = await help_parser(message.from_user.first_name)
        await message.reply(
            text, reply_markup=help_keyboard, disable_web_page_preview=True
        )
    return


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))
    return (
        home_text_pm,
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(CallbackQuery.from_user.mention)
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(CallbackQuery.id, text, show_alert=True)


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Hey {query.from_user.first_name} your **Miku** is here! 
I Help Admins To Manage Their Groups! 
Main commands available :
  /help: PM's you this message.
  /privacy: to view the privacy policy, and interact with your data.
  /help <module name>: PM's you info about that module.
  /settings:
    in PM: will send you your settings for all supported modules.
    in a group: will redirect you to pm, with all that chat's settings.
For all command use / or !"""
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "Here is the help for", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("back", callback_data="help_back")]]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    install()
    with closing(loop):
        with suppress(asyncio.exceptions.CancelledError):
            loop.run_until_complete(start_bot())
        loop.run_until_complete(asyncio.sleep(3.0))  
