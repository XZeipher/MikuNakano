from Miku import db

twelcomedb = db.twelcome

async def is_welcome_on(chat_id : int) -> bool:
    chat = bool(await twelcomedb.find_one({"chat_id" : chat_id}))
    return chat

async def del_welcome(chat_id : int):
    await twelcomedb.delete_one({"chat_id" : chat_id})

async def set_custom_welcome(chat_id : int, location : str):   
    return await twelcomedb.update_one({"chat_id": chat_id}, {"$set": {"location": location}}, upsert=True)

async def get_custom_welcome(chat_id : int):   
    chat = await twelcomedb.find_one({"chat_id" : chat_id})
    if not chat:
        return None
    return chat.get("location")
