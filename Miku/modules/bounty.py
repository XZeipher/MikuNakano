import os
import random
from Miku import app, LOG
from config import OWNER_ID, DEV_USERS, SUDO_USERS
from pyrogram import filters
from Miku.modules.mongo.games_db import user_wallet
from PIL import Image, ImageDraw, ImageFont
from wantedposter.wantedposter import WantedPoster


async def make_bounty(pic, first_name, last_name, bounty_amount):
    wanted_poster = WantedPoster(pic, last_name, first_name, bounty_amount)
    path = wanted_poster.generate()
    return path


@app.on_message(filters.command("wanted"))
async def _ok(app, message):
    user_id = message.from_user.id
    if message.sender_chat:
        return
    msg = await message.reply("**Creating Poster....**")
    user = message.from_user
    user_name = user.first_name
    if user.id in DEV_USERS:
        bounty = "♾️"
    else:
        bounty = await user_wallet(user_id)
    try:
        pic = await app.download_media(user.photo.big_file_id, file_name=f"pp{message.from_user.id}.png")
    except AttributeError:
        pic = "./Miku/resources/profilepic.png"

    last_name = user.last_name if user.last_name else None
    welpic = await make_bounty(pic, user_name, last_name, bounty)
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

♠ `/wanted` - get your bounty amount in poster earn more to increase bounty.
"""

__mod_name__ = "Wanted"
