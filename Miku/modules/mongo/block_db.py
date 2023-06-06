from Miku import db

blockdb = db.block

async def block_user(user_id : int):
  user =  await blockdb.find_one({"user_id" : user_id})
  if not user:
     return await blockdb.insert_one({"user_id" : user_id})
    

async def unblock_user(user_id : int):
  user =  await blockdb.find_one({"user_id" : user_id})
  if user:
     return await blockdb.delete_one({"user_id" : user_id}) 
    
async def is_blocked(user_id : int):
  user =  await blockdb.find_one({"user_id" : user_id})
  return bool(user)
