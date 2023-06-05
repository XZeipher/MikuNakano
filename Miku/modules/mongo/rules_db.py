from Miku import db

rulesdb = db.rules

async def is_rules(chat_id : int) -> bool:
    chat = bool(await rulesdb.find_one({"chat_id": chat_id}))
    return chat

async def set_rules(chat_id : int, rules : str):
    set_rules = {
        "chat_id" : chat_id,
        "rules" : rules 
    } 
    return await rulesdb.insert_one(set_rules) 

async def clear_rules(chat_id : int): 
    chat = await  is_rules(chat_id)
    if chat:
        return await rulesdb.delete_one({"chat_id" : chat_id})

async def get_rules(chat_id : int):
    chat = await rulesdb.find_one({"chat_id": chat_id})
    if chat:
        return chat.get("rules")
