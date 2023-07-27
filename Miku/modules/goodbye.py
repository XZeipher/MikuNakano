from Miku import app
from pyrogram import filters
import uuid
import math
from PIL import Image, ImageDraw, ImageFont
from unidecode import unidecode
import asyncio

@app.on_message(filters.left_chat_member)
async def _left_mem(client, message):
    first_name = unidecode(message.left_chat_member.first_name)
    user_id = message.left_chat_member.id
 
    goodbye = Image.open("./Miku/resources/sumi-sakurasawa-rent-a-girlfriend.gif")
    stark = [goodbye.copy()]

    try:
        while 1:
            goodbye.seek(goodbye.tell() + 4)
            owo = goodbye.copy()
            stark.append(owo)

    except EOFError:
        pass

    
    text = ["World opens itself"]
    s1 = stark[0].size[0] // 2
    s2 = 290
    font = ImageFont.truetype("./Miku/resources/SuisseIntl-Regular.ttf", 20)
    s3 = math.ceil(len(stark) / len(text))

    for i in range(len(stark)):
        draw = ImageDraw.Draw(stark[i])
        s4 = (s1 - len(text[i // s3]) * 5, s2)
        draw.text(s4, text[i // s3], font=font, anchor=None)

        
        if i == len(stark) // 2:
            await asyncio.sleep(2)
            
            text = [f"Goodbye {first_name}!"]
            for j in range(len(stark)):
                draw = ImageDraw.Draw(stark[j])
                s4 = (s1 - len(text[j // s3]) * 5, s2)
                draw.text(s4, text[j // s3], font=font, anchor=None)

    x =  f"goodbye_{uuid.uuid4()}.gif"
    stark[0].save(
        x,
        save_all=True,
        append_images=stark[1:],
        optimize=False,
        duration=150,
        loop=0,
    )

    
    await client.send_animation(message.chat.id, x, caption=f"**Goodbye {message.left_chat_member.mention}. Never come back again!**")
    import os
    os.remove(x)
