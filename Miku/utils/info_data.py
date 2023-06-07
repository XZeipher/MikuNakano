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

async def miku(pfp,chat,id):
    if len(chat) > 21:
        chat = chat[0:18] + ".."
    temp = Image.open("./Miku/resources/IMG_20230607_122544_067.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(363,363))
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",35)    
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",20)    
    nice = temp.copy()
    nice.paste(pfp, (58, 131), pfp)
    draw = ImageDraw.Draw(nice)
    draw.text((565,350),
                text=f"{chat.upper()} ~",
                font=m_font,
                fill=(275,275,275))
    
    draw.text((180,525),
                text=str(id),
                font=i_font,
                fill=(275,275,275))
    nice.save(f"./Miku/resources/nice{id}.png")
    return f"./Miku/resources/nice{id}.png"
