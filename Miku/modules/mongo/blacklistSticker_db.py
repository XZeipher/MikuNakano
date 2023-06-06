from Miku import db

blsticerkdb = db.blsticker

async def addBlSticker(chat_id : int,set_name : str):
    chat = await blsticerkdb.find_one({"chat_id" : chat_id}) 
    if chat:
        list = chat.get("pack_names")
        list.append(set_name)
        return await blsticerkdb.update_one({"chat_id" : chat_id},{"$set" : {"pack_names" : list}},upsert=True)  
    list = [set_name]
    return await blsticerkdb.update_one({"chat_id" : chat_id},{"$set" : {"pack_names" : list}}, upsert=True)   
 
async def blacklisted_stickers(chat_id : int) -> list:
    chat = await blsticerkdb.find_one({"chat_id" : chat_id})
    if chat :
        return chat.get("pack_names")
    
async def isBlSticker(chat_id : int,set_name : str) -> bool:
    chat = await blsticerkdb.find_one({"chat_id" : chat_id})
    if chat:
        check = chat.get("pack_names")
        if set_name in check:
            return True
        return False
    return False

async def unBlSticker(chat_id : int,set_name : str):
    chat = await blsticerkdb.find_one({"chat_id" : chat_id}) 
    if chat:
        list = chat.get("pack_names")
        list.remove(set_name)
        return await blsticerkdb.update_one({"chat_id": chat_id}, {"$set": {"pack_names": list}}, upsert=True)
