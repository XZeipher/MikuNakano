from Miku import db

nsfwdb = db.nsfw

async def add_nsfw(chat_id : int):
    return await nsfwdb.insert_one({"chat_id":chat_id})

async def rm_nsfw(chat_id : int):
    return await nsfwdb.delete_one({"chat_id":chat_id})
