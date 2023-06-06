import time
import re
import asyncio
import sys
import traceback,io
from pyrogram import types, filters, errors,enums
from config import SUPREME_USERS
from Miku import app, BOT_USERNAME
from typing import List, Union, Callable
from pyrogram.types import Message
from config import HANDLERS
from functools import wraps
from dotmap import DotMap
from Miku.lang import get_string
from Miku.modules.mongo.lang_db import *

DISABLE_COMMANDS = []
COMMANDS_LIST = []
ERROR_LOG = "ErrorMiku"

def language(func):
    @wraps(func)
    async def wrapper(_, update):
        if isinstance(update,types.Message):
            chat_id = update.chat.id
        if isinstance(update,types.CallbackQuery):
            chat_id= update.message.chat.id
        try:
            language = await get_lang(chat_id)
            language = get_string(language)
        except:
            language = get_string("en")
        language = DotMap(language) 
        return await func(_,update, language)
    return wrapper


def control_user(max_messages: int = 3, interval: float = 1.5):
    def decorator(func: Callable):
        last_message_times = {}
        message_counts = {}

        @wraps(func)
        async def wrapper(client, update):
            chat_id, user_id, alert = await get_user_id(update)
            current_time = time.time()

            if user_id not in last_message_times:
                last_message_times[user_id] = current_time
                message_counts[user_id] = 1
            else:
                elapsed_time = current_time - last_message_times[user_id]
                if elapsed_time < interval:
                    if not alert:
                        return await update.reply("Please refrain from spamming.")
                    else:
                        return await update.answer("Slow down...")

                last_message_times[user_id] = current_time
                message_counts[user_id] += 1

            if message_counts[user_id] > max_messages:
                # Block code
                # will do later
                pass

            try:
                await func(client, update)
                if last_message_times[user_id] + (max_messages * interval) < current_time:
                    del last_message_times[user_id]
                    del message_counts[user_id]
            except errors.FloodWait as e:
                await asyncio.sleep(e.x + 2)
            except Exception as err:
                exc_type, exc_value, exc_traceback = sys.exc_info()
                error_traceback = traceback.format_exception(exc_type, exc_value, exc_traceback)
                error_message = f"**Error** | User ID: {user_id} | Chat ID: {chat_id}\n"
                error_message += f"Message Text: {update.text or update.caption if not alert else update.message.text or update.message.caption}\n\n"
                error_message += "".join(error_traceback)
                if len(error_message) > 4096:
                   with io.BytesIO(str.encode(error_message)) as out_file:
                       out_file.name = "err.text"
                   await app.send_document(ERROR_LOG,out_file)
                else:
                    await app.send_message(ERROR_LOG,error_message)

                raise err

        return wrapper

    return decorator


def command(commands: Union[str, List[str]], prefixes: Union[str, List[str]] = HANDLERS, case_sensitive: bool = False,
            disable: bool = False):
    command_lister(commands, disable)
    commands = commandsHelper(commands)

    command_re = re.compile(r"([\"'])(.*?)(?<!\\)\1|(\S+)")
    async def func(flt, _, message: Message):
        text = message.text or message.caption
        message.command = None

        if not text:
            return False

        pattern = r"^{}(?:\s|$)" if flt.case_sensitive else r"(?i)^{}(?:\s|$)"

        for prefix in flt.prefixes:
            if not text.startswith(prefix):
                continue

            without_prefix = text[len(prefix):]

            for cmd in flt.commands:
                if not re.match(pattern.format(re.escape(cmd)), without_prefix):
                    continue

                message.command = [cmd] + [
                    re.sub(r"\\([\"'])", r"\1", m.group(2) or m.group(3) or "")
                    for m in command_re.finditer(without_prefix[len(cmd):])
                ]

                return True

        return False

    commands = commands if isinstance(commands, list) else [commands]
    commands = {c if case_sensitive else c.lower() for c in commands}

    prefixes = [] if prefixes is None else prefixes
    prefixes = prefixes if isinstance(prefixes, list) else [prefixes]
    prefixes = set(prefixes) if prefixes else {""}

    return filters.create(
        func,
        "CommandFilter",
        commands=commands,
        prefixes=prefixes,
        case_sensitive=case_sensitive
    )


async def get_user_id(update) -> tuple[int,int,bool]:
    if isinstance(update, types.Message):
        alert = False
        chat_id = update.chat.id
        if update.sender_chat:
            user_id = update.sender_chat.id
        else:
            user_id = update.from_user.id
    elif isinstance(update, types.CallbackQuery):
        alert = True
        chat_id = update.message.chat.id
        user_id = update.from_user.id
    else:
        alert = None
        user_id = None
        chat_id = None
    return chat_id,user_id, alert



def command_lister(commands: Union[str, List[str]], disable: bool = False) -> list:
    if isinstance(commands, str):
        if disable:
            DISABLE_COMMANDS.append(commands)

    if isinstance(commands, list):
        if disable:
            DISABLE_COMMANDS.extend(commands)


def commandsHelper(commands: Union[str, List[str]]) -> list:
    commands_list = []

    if isinstance(commands, str):
        username_command = f"{commands}@{BOT_USERNAME}"
        commands_list.extend([commands, username_command])

    if isinstance(commands, list):
        for command in commands:
            username_command = f"{command}@{BOT_USERNAME}"
            commands_list.extend([command, username_command])

    return commands_list
