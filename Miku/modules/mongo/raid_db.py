from Miku import db

raiddb = db.raid

async def isRaidOn(chat_id : int) -> bool:
    return bool(await raiddb.find_one({"chat_id" : chat_id}))

async def raid_on(chat_id : int):
    chat = await isRaidOn(chat_id)
    if not chat:
        return await raiddb.insert_one({"chat_id" : chat_id})

async def raid_off(chat_id : int):
    chat = await isRaidOn(chat_id)
    if chat:
        return await raiddb.insert_one({"chat_id" : chat_id})
