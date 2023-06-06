from Miku import db

gbandb = db.gban

async def is_gbanned_user(user_id: int) -> bool:
    user = bool(await gbandb.find_one({"user_id": user_id}))
    return user

async def add_gban_user(user_id : int,reason : str):
    is_gbanned = await is_gbanned_user(user_id)
    if is_gbanned:
        return
    await gbandb.insert_one({"user_id": user_id})
    await gbandb.update_one({"user_id": user_id},{"$set" : {"reason" : reason}},upsert=True)
    
async def get_gban_reason(user_id : int):
    user = await gbandb.find_one({"user_id": user_id})
    if user:
        return user.get("reason")    

async def remove_gban_user(user_id: int):
    is_gbanned = await is_gbanned_user(user_id)
    if not is_gbanned:
        return
    return await gbandb.delete_one({"user_id": user_id})

async def get_gbans_list() -> list:
    gbanlist = [i async for i in gbandb.find({"user_id": {"$gt": 0}})]
    if not gbanlist:
        return []
    gban_list = []
    for i in gbanlist:
        gban_list.append(i["user_id"])
    return gban_list

