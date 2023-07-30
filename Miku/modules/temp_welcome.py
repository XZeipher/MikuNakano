from pyrogram import *
import os
from Miku import app
from config import DEV_USERS
from PIL import Image,ImageOps,ImageDraw,ImageChops, ImageFont 


async def circle(pfp, size=(215, 215)):
    pfp = pfp.resize(size, Image.Resampling.LANCZOS).convert("RGBA")
    bigsize = (pfp.size[0] * 3, pfp.size[1] * 3)
    mask = Image.new("L", bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(pfp.size, Image.Resampling.LANCZOS)
    mask = ImageChops.darker(mask, pfp.split()[-1])
    pfp.putalpha(mask)
    return pfp

async def template(pic , name , ids , stats):
    temp = Image.open("./Miku/resources/20230730_081017_0000.png")
    fonts = ImageFont.truetype("./Miku/resources/NotoSans-ExtraBold.ttf",30)
    pfp = Image.open(pic).convert("RGBA")
    pfp = await circle(pfp,(139,139))
    temp.paste(pfp, (592, 117, 592 + pfp.width, 117 + pfp.height), pfp)
    draw = ImageDraw.Draw(temp)
    draw.text((186 , 337),name,"white",font=NAME)   
    draw.text((127 , 394),str(ids),"white",font=NAME)
    draw.text((208 , 448),stats,"white",font=NAME)   
    temp.save(f"./Miku/resources/temp{ids}.png")
    return f"./Miku/resources/temp{ids}.png"
    
    
@app.on_message(filters.new_chat_members & filters.group,group=11)
async def _weem(_, message):    
    chat_id = message.chat.id   
    count = await _.get_chat_members_count(chat_id) 
    for m in message.new_chat_members:
        name = m.first_name 
        mention = m.mention 
        user_id = m.id       
        try:
            user_photo = m.photo.big_file_id
            pic = await _.download_media(m.photo.big_file_id,file_name =f"pp{user_id}.png")
        except AttributeError:
            pic = "./Miku/resources/profilepic.png"
        if user_id in DEV_USERS:
        	stats = "Developer"
        else:
        	stats = "User"
        welpic = await template(pic , name , user_id , stats)
        await _.send_photo(chat_id,welpic,caption=f"**{mention} Welcome Kid!**")
        os.remove(welpic)