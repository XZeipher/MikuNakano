from pyrogram import *
from Miku import app
from PIL import Image , ImageDraw , ImageFont

async def template(name , username , ids):
    temp = Image.open("./Miku/resources/IMG_20230723_121050_314.png")
    name_font = ImageFont.truetype("./Miku/resources/FrescitoRegularPersonalUseRegular-lgmj5.otf",53)
    username_font = ImageFont.truetype("./Tanji/resources/FrescitoRegularPersonalUseRegular-lgmj5.otf",49)
    id_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",40)
    draw = ImageDraw.Draw(temp)
    draw.text((318 , 407),name,"white",font=name_font)    
    draw.text((448 , 517),username,"white",font=username_font)
    draw.text((218 , 620),str(ids),"white",font=id_font)
    temp.save(f"./Miku/resources/temp{ids}.png")
    return f"./Miku/resources/temp{ids}.png"
    
    
@app.on_message(filters.new_chat_members & filters.group,group=11)
async def _weem(_, message):    
    chat_id = message.chat.id   
    count = await _.get_chat_members_count(chat_id) 
    for m in message.new_chat_members:
        name = m.first_name 
        username = m.username
        mention = m.mention 
        user_id = m.id
        welpic = await template(name , username , user_id)
        await _.send_photo(chat_id,welpic,caption=f"**{mention} Welcome Kid!**")
        os.remove(welpic)
        