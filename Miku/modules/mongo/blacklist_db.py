from Miku import db

blacklistdb = db.blacklist

async def add_blacklist(chat_id : int,word : str):
    chat = await blacklistdb.find_one({"chat_id" : chat_id})
    if chat:
        list = chat["words"]
        list.append(word)
        return await blacklistdb.update_one({"chat_id" : chat_id},{"$set" : {"words" : list}},upsert=True)
    list = [word]
    return await blacklistdb.update_one({"chat_id" : chat_id},{"$set" : {"words" : list}},upsert=True)

async def rm_blacklist(chat_id : int,word : str):
    chat = await blacklistdb.find_one({"chat_id" : chat_id})
    if chat:
        list = chat["words"]
        list.remove(word)
        return await blacklistdb.update_one({"chat_id" : chat_id},{"$set" : {"words" : list}})
    
async def is_blacklisted(chat_id : int,word : str) -> bool:
    chat = await blacklistdb.find_one({"chat_id" : chat_id})
    if chat:
        list = chat["words"]
        if word in list:
            return True
        return False
    return False

async def get_blacklist(chat_id: int) -> list:
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if chat:
        return chat["words"]
    return []        
    
async def un_blacklistall(chat_id : int):
    chat = await blacklistdb.find_one({"chat_id": chat_id})
    if chat:
        return await blacklistdb.delete_one({"chat_id" : chat_id})
     
