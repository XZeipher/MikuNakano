from Miku import db
from Miku.modules.mongo.chats_db import get_served_chats

usersdb = db.users

async def get_served_users() -> list:
    chats = usersdb.find({"user_id": {"$gt": 0}})
    if not chats:
        return []
    chats_list = []
    for chat in await chats.to_list(length=10000000000):
        chats_list.append(chat["user_id"])
    return chats_list


async def is_served_user(chat_id: int) -> bool:
    chat = await usersdb.find_one({"user_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_user(chat_id: int):
    is_served = await is_served_user(chat_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": chat_id})


async def remove_served_user(chat_id: int):
    is_served = await is_served_user(chat_id)
    if not is_served:
        return
    return await usersdb.delete_one({"user_id": chat_id})
