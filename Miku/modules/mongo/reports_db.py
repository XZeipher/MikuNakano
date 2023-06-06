from Miku import db

reportsdb = db.report

async def report_on(chat_id : int):
    return await reportsdb.insert_one({"chat_id" : chat_id})

async def isOn(chat_id : int) -> bool:
    return bool(await reportsdb.find_one({"chat_id" : chat_id}))

async def report_off(chat_id : int):
    return await reportsdb.delete_one({"chat_id" : chat_id})
