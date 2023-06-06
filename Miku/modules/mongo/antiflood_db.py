from Miku import db
from typing import Union


antifloodb = db.antiflood

async def set_flood(chat_id : int, flood_val : Union[int,bool]):
    chat = await antifloodb.find_one({"chat_id" : chat_id})
    if chat is None:        
        if type(flood_val) == int:
            flood_limit = flood_val
            flood = True
        elif type(flood_val) == bool:
            flood_limit = 4
            flood = flood_val
        mm = {"chat_id": chat_id, "flood_limit": flood_limit, "flood_mode": {"flood_mode": 1,"until_time": None},'flood' : flood}
        return await antifloodb.insert_one(mm)
    else:
        if type(flood_val) == int:
            set_key = {
                'flood_limit': flood_val,
                'flood': True
            }
        elif type(flood_val) == bool:
            set_key = {
                'flood': flood_val
            }
        return await antifloodb.update_one({"chat_id" : chat_id}, {"$set" : set_key}, upsert=True)

async def set_antiflood_mode(chat_id : int, flood_mode,until_time=None):
    chat = await antifloodb.find_one({"chat_id" : chat_id})
    if chat is not None:
        return await antifloodb.update_one({'chat_id': chat_id},{
                '$set': {
                    'flood_mode': {
                        'flood_mode': flood_mode,
                        'until_time': until_time}}},upsert=True)
                    
    else:
        mm = {'chat_id': chat_id, 'flood_limit': 4, 'flood': False, 'flood_mode': flood_mode, 'until_time': until_time}                                                                       
        return await antifloodb.insert_one(mm)
                    
async def get_flood(chat_id: int) -> bool :
    chat = await antifloodb.find_one({"chat_id" : chat_id})
    if chat:
        return chat["flood"]
    else:
        return False                    
                
async def get_antiflood_settings(chat_id : int):
    chat = await antifloodb.find_one({"chat_id" : chat_id})
    if chat:
        flood_mode = chat["flood_mode"]["flood_mode"]
        until_date = chat["flood_mode"]["until_time"]
    else:
        flood_mode = 1
        until_date = None
    return (flood_mode,until_date)
               
async def get_flood_limit(chat_id : int) -> int:
    chat = await antifloodb.find_one({"chat_id" : chat_id})
    if chat:
        return chat["flood_limit"]
