from Miku import db

actiondb = db.action

async def isEnbale(chat_id : int) -> bool:
    chat = bool(await actiondb.find_one({"chat_id" : chat_id}))
    return chat

async def add_action(chat_id : int):
    chat = await isEnbale(chat_id)
    if not chat:
        await actiondb.insert_one({"chat_id" : chat_id})

async def rm_action(chat_id : int):
    chat = await isEnbale(chat_id)
    if chat:
        await actiondb.delete_one({"chat_id" : chat_id})
