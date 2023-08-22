from pyrogram import Client, filters
from Miku import ubot
import httpx
import asyncio

ub_text = """
/eval 
import requests
b = requests.post("http://api.qewertyy.me/models/inference/task", data={}).json()
await message.reply_photo(b['img_urls'][0])
"""

async def send_task(text):
    async with httpx.AsyncClient() as cli:
        ids = cli.post("http://api.qewertyy.me/models/inference", data={"model_id": 2, "prompt": text})
        await asyncio.sleep(20)
        data = {"task_id": a['task_id'], "request_id": a['request_id']}
        await ubot.send_message("lslkzmdncbcb", ub_text.format(data))

@Client.on_message(filters.command("draw"))
async def draw(_, message):
    text = message.text.split(maxsplit=1)[1]
    await send_task(text)
