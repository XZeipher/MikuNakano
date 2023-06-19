import os
import random 
from Miku import app,LOG
from config import OWNER_ID, DEV_USERS, SUDO_USERS 
from pyrogram import filters
from PIL import Image,ImageDraw,ImageFont
from wantedposter.wantedposter import WantedPoster

NORMAL = [10_000,5_000,2_060,1200,1500,150]

async def make_bounty(pic,first_name,last_name,bounty_amount):   
     wanted_poster = WantedPoster(pic,last_name,first_name,bounty_amount)
     path = wanted_poster.generate() 
     return path   

@app.on_message(filters.command("wanted"))
async def _ok(app, message):
    if message.sender_chat:
        return
    msg = await message.reply("**Creating poster....**")
    user = message.from_user
    user_name = user.first_name
    if user.id in DEV_USERS:
        bounty = 461_110_000
    elif user.id in SUDO_USERS:
        bounty = 340_000_000
    else:
        bounty = random.choice(NORMAL)    
    
    try:
        pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{message.from_user.id}.png")
    except AttributeError:
        pic = "./Miku/resources/profilepic.png"
    
    last_name = user.last_name if user.last_name else None
    welpic = await make_bounty(pic,user_name,last_name,bounty)
    await message.reply_photo(welpic)
    await msg.delete()
    try:
        os.remove(welpic)
        if user.photo:
            os.remove(pic)
    except Exception as er:
        LOG.print(f" {er}")
        
        
__help__ = """
**Create Wanted Poster**

**Commands**

♠ `/wanted` - create bounty with your character

"""

__mod_name__ = "Wanted"

