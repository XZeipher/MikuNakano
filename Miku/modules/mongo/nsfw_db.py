# one like for me guys for this hard work uff

from typing import Dict, List, Union
from Miku import db

nsfwdb = db.nsfw


async def is_nsfw_on(chat_id: int) -> bool:
    chat = nsfwdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True

async def nsfw_on(chat_id: int):
    is_nsfw = is_nsfw_on(chat_id)
    if is_nsfw:
        return
    return nsfwdb.delete_one({"chat_id": chat_id})


async def nsfw_off(chat_id: int):
    is_nsfw = is_nsfw_on(chat_id)
    if not is_nsfw:
        return
    return nsfwdb.insert_one({"chat_id": chat_id})
