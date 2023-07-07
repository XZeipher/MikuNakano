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

async def minimal1(pfp,chat,id):
    if len(chat) > 21:
        chat = chat[0:18] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/minimal1.jpg")
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
    nice.save(f"./Miku/resources/downloads/nice{id}.png")
    return f"./Miku/resources/downloads/nice{id}.png"


async def minimal2(pfp,chat,id):
    if len(chat) > 21:
        chat = chat[0:20] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/minimal2.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(363,363))
    min2 = temp.copy()
    min2.paste(pfp, (73, 125), pfp)
    draw = ImageDraw.Draw(min2)
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",20)  
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",35)  
    draw.text((180,525),
                text=str(id),
                font=i_font,
                fill=(275,275,275))
    draw.text((570,350),
                text=f"{chat.upper()} ~",
                font=m_font,
                fill=(275,275,275))    
    min2.save(f"./Miku/resources/downloads/min2{id}.png") 
    return f"./Miku/resources/downloads/min2{id}.png"

async def animin1(pfp,name,id,username):
    if len(name) > 18 :
        name = name[0:18] + "..."
    if len(username) > 16 :
        username = username[0:16] + "..." 
    temp = Image.open("./Miku/resources/welcome_temp/AnimeMinimal1.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(330,330))
    min3 = temp.copy()
    min3.paste(pfp, (90, 68), pfp)
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",20)    
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",25)
    draw = ImageDraw.Draw(min3)
    draw.text((190,550),
                text=str(id),
                font=i_font,
                fill=(275,275,275))
    draw.text((280,510),
                text=name.upper(),
                font=m_font,
                fill=(275,275,275))         
    draw.text((380,580),
                text=f"@{username}".upper(),
                font=i_font,
                fill=(275,275,275))
    min3.save(f"./Miku/resources/downloads/min3{id}.png")
    return f"./Miku/resources/downloads/min3{id}.png"

async def animin2(name,id,username,chat):
    if len(username) > 18:
        username = username[0:17] + ".."
    if len(name) > 20:
        name = name[0:18] + ".."
    if len(chat) > 21:
        chat = chat[0:20] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/AnimeMinimal2.jpg")
    m_font = ImageFont.truetype("./Miku/resources/FontRemix.ttf",40)
    u_font = ImageFont.truetype("./Miku/resources/FontRemix.ttf",30)
    min4 = temp.copy()
    draw = ImageDraw.Draw(min4)
    draw.text((820,190),
                text=name.upper(),
                font=m_font,
                fill=(275,275,275))     
    draw.text((750,255),
                text=str(id),
                font=m_font,
                fill=(275,275,275))    
    draw.text((920,320),
                text=f"@{username}".upper(),
                font=u_font,
                fill=(275,275,275))
    draw.text((760,390),
                text=chat.upper(),
                font=m_font,
                fill=(275,275,275))                 
    min4.save(f"./Miku/resources/downloads/min4{id}.png")
    return f"./Miku/resources/downloads/min4{id}.png"
    
async def animin3(pfp,name,id,username,chat):
    if len(chat) > 21:
        chat = chat[0:21] + ".."
    if len(username) > 18 :
        username = username[0:18] + ".."
    if len(name) > 20 :
        name = name[0:20] + ".."
        
    temp = Image.open("./Miku/resources/welcome_temp/AnimeMinimal3.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(330,330))
    min5 = temp.copy()
    min5.paste(pfp, (28, 19), pfp)
    m_font = ImageFont.truetype("./Miku/resources/FontRemix.ttf",40)
    u_font = ImageFont.truetype("./Miku/resources/FontRemix.ttf",30)
    c_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",30)
    draw = ImageDraw.Draw(min5)
    draw.text((690,280),
                text=str(id),
                font=m_font,
                fill=(275,275,275))
    draw.text((760,220),
                text=name.upper(),
                font=m_font,
                fill=(275,275,275))         
    draw.text((870,350),
                text=f"@{username}".upper(),
                font=u_font,
                fill=(275,275,275))
    draw.text((650,410),
                text=chat.upper(),
                font=c_font,
                fill=(275,275,275))
    min5.save(f"./Miku/resources/downloads/min5{id}.png")
    return f"./Miku/resources/downloads/min5{id}.png"



async def gamin(pfp,chat,name,id, username):
    if len(name) > 13:
        name = name[0:13] + ".."
    if len(username) > 13:
        username = username[0:13] + ".."
    if len(chat) > 21:
        chat = chat[0:20] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/GamingMinimal.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(290,290))
    min6 = temp.copy()
    min6.paste(pfp, (19, 410), pfp)
    draw = ImageDraw.Draw(min6)    
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",25)
    u_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",18)
    c_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",30)
    draw.text((420,560),
                text=str(id),
                font=m_font,
                fill=(275,275,275))
    draw.text((490,520),
                text=name.upper(),
                font=m_font,
                fill=(275,275,275))         
    draw.text((590,605),
                text=f"@{username}".upper(),
                font=u_font,
                fill=(275,275,275))
    draw.text((190,230),
                text=chat.upper(),
                font=c_font,
                fill=(275,275,275))                
    min6.save(f"./Miku/resources/downloads/min6{id}.png") 
    return f"./Miku/resources/downloads/min6{id}.png"


async def sun(pfp,chat,count,id):
    if len(chat) > 21:
        chat = chat[0:20] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/Sun.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(335,335))
    min7 = temp.copy()
    min7.paste(pfp, (460, 185), pfp)
    draw = ImageDraw.Draw(min7)
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",45)
    draw.text((600,590),
                text=f"{count}th member".upper(),
                font=m_font,
                fill=(275,275,275))
    draw.text((650,75),
                text=chat.upper(),
                font=m_font,
                fill=(275,275,275))                
    min7.save(f"./Miku/resources/downloads/min7{id}.png")
    return f"./Miku/resources/downloads/min7{id}.png"


async def gamin1(pfp,name,username,id):
    if len(name) > 15:
        name = name[0:14] + ".."
    if len(username) > 13:
        username = username[0:13] + ".."
    temp = Image.open("./Miku/resources/welcome_temp/Gaming.jpg") 
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(360,360))
    min8 = temp.copy()
    min8.paste(pfp, (105, 174), pfp)
    draw = ImageDraw.Draw(min8)
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",30)    
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",25)
    id_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",15) 
    draw.text((780,270),
                text=name.upper(),
                font=i_font,
                fill=(275,275,275))
    draw.text((900,330),
                text=f"@{username}",
                font=m_font,
                fill=(275,275,275))
    draw.text((230,570),
                text=str(id),
                font=id_font,
                fill=(275,275,275))                                    
    min8.save(f"./Miku/resources/downloads/min8{id}.png")
    return f"./Miku/resources/downloads/min8{id}.png"

      
async def wholesome(pfp,chat,id):
    temp = Image.open("./Miku/resources/welcome_temp/WS.jpg")  
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(290,290))   
    min9 = temp.copy()
    min9.paste(pfp, (965, 403), pfp)
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",20)
    m_font = ImageFont.truetype("./Miku/resources/FontRemix.ttf",65)
    draw = ImageDraw.Draw(min9)
    draw.text((730,120),
                text=chat.upper(),
                font=m_font,
                fill=(275,275,275))
    draw.text((1080,367),
                text=str(id),
                font=i_font,
                fill=(275,275,275))               
    min9.save(f"./Miku/resources/downloads/min9{id}.png")
    return f"./Miku/resources/downloads/min9{id}.png"

async def meriloli(pfp,chat,id):
    temp = Image.open("./Miku/resources/welcome_temp/Nezuko.jpg")   
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(280,280))   
    min10 = temp.copy()
    min10.paste(pfp, (37, 18), pfp)
    draw = ImageDraw.Draw(min10)
    i_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",20)
    m_font = ImageFont.truetype("./Miku/resources/monumentextended-regular.otf",50)
    draw.text((680,605),
                text=chat.upper(),
                font=m_font,
                fill=(275,275,275))
    draw.text((170,345),
                text=str(id),
                font=i_font,
                fill=(275,275,275))               
    min10.save(f"./Miku/resources/downloads/min10{id}.png")
    return f"./Miku/resources/downloads/min10{id}.png"

async def animegirl1(pfp,id) :
    temp = Image.open("./Miku/resources/welcome_temp/AnimeGirl1.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(535,535))
    min11 = temp.copy()
    min11.paste(pfp, (63, 130), pfp)
    min11.save(f"./Miku/resources/downloads/min11{id}.png")
    return f"./Miku/resources/downloads/min11{id}.png"

async def animegirl2(pfp,id):
    temp = Image.open("./Miku/resources/welcome_temp/AnimeGirl2.jpg")
    pfp = Image.open(pfp).convert("RGBA")
    pfp = await circle(pfp,(230,230))
    min12 = temp.copy()
    min12.paste(pfp, (250, 433), pfp)
    min12.save(f"./Miku/resources/downloads/min12{id}.png")
    return f"./Miku/resources/downloads/min12{id}.png"
    






