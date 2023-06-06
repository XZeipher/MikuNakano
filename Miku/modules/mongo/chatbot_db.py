from Miku import db


chatbotdb = db.chatbot


async def addchat_bot(chat_id : int):
    return await chatbotdb.insert_one({"chat_id" : chat_id})
    
async def rmchat_bot(chat_id : int):   
    chat = await chatbotdb.find_one({"chat_id" : chat_id})
    if chat: 
        return await chatbotdb.delete_one({"chat_id" : chat_id})  
