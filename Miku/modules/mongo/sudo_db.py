from Miku import db

sudodb = db.sudo

async def add_sudo(user_id : int):
    return await sudodb.insert_one({"user_id" : user_id})


async def del_sudo(user_id : int):
    return await sudodb.delete_one({"user_id" : user_id})

async def get_sudo_list() -> list:
    sudo_list = []
    for x in await sudodb.find().to_list(length=None):
        sudo_list.append(x["user_id"])
    return sudo_list
