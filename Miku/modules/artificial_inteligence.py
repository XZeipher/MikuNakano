from Miku import app
import httpx
from pyrogram import filters
from .pyro.decorators import control_user, command

@app.on_message(command(commands=("chat")))
@control_user()
async def _sax(app, message):
    txt = await message.reply("**writing....**")
    
    if len(message.command) < 2:
        return await txt.edit("**give me a message too.**")
    
    query = message.text.split(maxsplit=1)[1]
    url = "https://api.safone.me/chatgpt"
    payload = {
        "message": query,
        "chat_mode": "assistant",
        "dialog_messages": "[{\"bot\":\"\",\"user\":\"\"}]"
    }
    
    async with httpx.AsyncClient(timeout=20) as client:
        try:
            response = await client.post(url, json=payload, headers={"Content-Type": "application/json"})
            response.raise_for_status()
            results = response.json()
            await txt.edit(results["message"])
        except httpx.HTTPError as e:
            await txt.edit(f"**Api is Down try** `/ask`")
        except Exception as e:
            await txt.edit(f"**Api is Down try** `/ask`")


@app.on_message(command(commands=("sugoi")))
@control_user()
async def sugoi(app, message):
    text = await message.reply("")
    if len(message.command) < 1:
        return await text.edit("**Give me a message too.**")
    msg = message.text.split(maxsplit=1)[1]
    url = f"https://sugoi-api.vercel.app/chat?msg={msg}"
    async with httpx.AsyncClient(timeout=20) as cli:
        try:
            resp = await cli.get(url)
            js = resp.json()
            await text.edit(js['response'])
        except Exception as e:
            await text.edit(f"**Api is Down try** `/ask`")


@app.on_message(command(commands=("ask")))
@control_user()
async def openai(app, message):
    txt = await message.reply("💭")
    if len(message.command) < 1:
        return await txt.edit("**Give me a message too.**")
    msg = message.text.split(maxsplit=1)[1]
    url = "https://api.qewertyy.me/models"
    params = {"model_id": 0, "prompt": msg}
    async with httpx.AsyncClient(timeout=20) as cli:
        try:
            resp = await cli.post(url, params=params)
            await txt.edit(resp.json()['content'])
        except Exception as e:
            print(str(e))
            await txt.edit("**Api is Down contact: @MikuNakanoXSupport**")
            
@app.on_message(command(commands=("bard")))
@control_user()
async def bardapi(app, message):
    txt = await message.reply("💭")
    if len(message.command) < 1:
        return await txt.edit("**Give me a message too.**")
    msg = message.text.split(maxsplit=1)[1]
    url = f"https://api.safone.me/bard?message={msg}"
    async with httpx.AsyncClient(timeout=20) as cli:
        try:
            resp = await cli.get(url)
            data = resp.json()
            if 'images' in data['detail']:
                images = data['detail']['images']
                if 'choices' in data and data['choices']:
                    text = data['choices'][0]['content'][0]
                else:
                    text = "No Text Available!"
                await txt.delete()
                await message.reply_photo(images[0], caption=text)
            elif 'choices' in data and data['choices']:
                text = data['choices'][0]['content'][0]
                await txt.edit(text)
            else:
                await txt.edit("**Api is Down contact: @MikuNakanoXSupport**")
