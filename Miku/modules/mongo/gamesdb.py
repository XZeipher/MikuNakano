import datetime
from Miku import db

gamesdb = db.alpha

async def user_wallet(user_id):
    player = await gamesdb.find_one({"user_id" : user_id})
    if not player:
        return 0
    return player['coins']
