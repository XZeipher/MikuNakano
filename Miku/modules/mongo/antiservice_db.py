from Miku import db

antiservicedb = db.antiservice

async def antiservice_on(chat_id : int):
    return await antiservicedb.insert_one({"chat_id" : chat_id})

async def antiservice_off(chat_id : int):
    return await antiservicedb.delete_one({"chat_id" : chat_id})

async def isEnbale(chat_id : int) -> bool:
    chat = bool(await antiservicedb.find_one({"chat_id" : chat_id}))
    return chat
