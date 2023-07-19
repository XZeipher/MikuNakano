from Miku import app
import httpx
from pyrogram import filters
from .pyro.decorators import control_user,command

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
            response = await client.post(url, json=payload,headers = {"Content-Type": "application/json"})
            response.raise_for_status()
            results = response.json()
            await txt.edit(results["message"])
        except httpx.HTTPError as e:
            await txt.edit(f"An error occurred: {str(e)}")
        except Exception as e:
            await txt.edit(f"An error occurred: {str(e)}")


@app.on_message(command(commands=("ask")))
async def asla(app, message):
    text = await message.reply("💭")
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
            await text.edit(f"An error occurred: {str(e)}")
