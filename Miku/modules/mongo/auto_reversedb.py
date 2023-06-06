from Miku import db


reversedb = db.reverse


async def add_reverse(chat_id : int):
    return await reversedb.insert_one({"chat_id" : chat_id})
    
async def rm_reverse(chat_id : int):   
    chat = await reversedb.find_one({"chat_id" : chat_id})
    if chat: 
        return await reversedb.delete_one({"chat_id" : chat_id})
