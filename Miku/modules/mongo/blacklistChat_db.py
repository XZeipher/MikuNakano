from Miku import db

blchatdb = db.blacklistchat

async def add_blacklistchat(chat_id : int):
    chat = await blchatdb.find_one({"chat_id" : chat_id})
    if not chat:
        return await blchatdb.insert_one({"chat_id" : chat_id})

async def rm_blacklistchat(chat_id : int):
    chat = await blchatdb.find_one({"chat_id" : chat_id})
    if chat:
        return await blchatdb.delete_one({"chat_id" : chat_id})
    
async def is_blackilisted(chat_id):
    chat = await blchatdb.find_one({"chat_id":chat_id})
    if chat:
        return True
    return False

async def get_blacklist_chat() -> list:
    chats = [i async for i in blchatdb.find({"chat_id": {"$lt": 0}})]
    if not chats:
        return []
    chats_list = []
    for i in chats:
        chats_list.append(i["chat_id"])
    return chats_list
