import httpx
from pyrogram import filters , Client
import random
from Miku import app

url_sfw_1 = "https://api.waifu.pics/sfw/"
url_sfw_2 = "https://nekos.best/"

async def get_json(url):
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        return response.json()

@Client.on_message(filters.command("waifu"))
async def swaifu(client, msg):
    url = f"{url_sfw_1}waifu"
    result = await get_json(url)
    img = result['url']
    await msg.reply_photo(photo=img)

@Client.on_message(filters.command("pout"))
async def pout(client, msg):
    resp = await get_json("https://nekos.best/api/v2/pout")
    img = resp["results"][0]["url"]
    await msg.reply_animation(img)

@Client.on_message(filters.command("bored"))
async def bored(client, msg):
    resp = await get_json("https://nekos.best/api/v2/bored")
    img = resp["results"][0]["url"]
    await msg.reply_animation(img)

@Client.on_message(filters.command("nekos"))
async def nekos2(client, msg):
    resp = await get_json("https://nekos.best/api/v2/neko")
    img = resp["results"][0]["url"]
    await msg.reply_photo(photo=img)

@Client.on_message(filters.command("stare"))
async def stare(client, msg):
    resp = await get_json("https://nekos.best/api/v2/stare")
    img = resp["results"][0]["url"]
    await msg.reply_animation(img)

@Client.on_message(filters.command("think"))
async def think(client, msg):
    resp = await get_json("https://nekos.best/api/v2/think")
    img = resp["results"][0]["url"]
    await msg.reply_animation(img)

@Client.on_message(filters.command("thumbsup"))
async def thumbsup(client, msg):
    resp = await get_json("https://nekos.best/api/v2/thumbsup")
    img = resp["results"][0]["url"]
    await msg.reply_animation(img)

@Client.on_message(filters.command("neko"))
async def neko(client, msg):
    url = f"{url_sfw_1}neko"
    result = await get_json(url)
    img = result['url']
    await msg.reply_photo(photo=img)

@Client.on_message(filters.command("bully"))
async def bully(client, msg):
    url = f"{url_sfw_1}bully"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("cuddle"))
async def cuddle(client, msg):
    url = f"{url_sfw_1}cuddle"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("cry"))
async def cry(client, msg):
    url = f"{url_sfw_1}cry"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("hug"))
async def hug(client, msg):
    url = f"{url_sfw_1}hug"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("awoo"))
async def awoo(client, msg):
    url = f"{url_sfw_1}awoo"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("kiss"))
async def kiss(client, msg):
    url = f"{url_sfw_1}kiss"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("lick"))
async def lick(client, msg):
    url = f"{url_sfw_1}lick"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("pat"))
async def pat(client, msg):
    url = f"{url_sfw_1}pat"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("smug"))
async def smug(client, msg):
    url = f"{url_sfw_1}smug"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("bonk"))
async def bonk(client, msg):
    url = f"{url_sfw_1}bonk"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("yeet"))
async def yeet(client, msg):
    url = f"{url_sfw_1}yeet"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("blush"))
async def blush(client, msg):
    url = f"{url_sfw_1}blush"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("smile"))
async def smile(client, msg):
    url = f"{url_sfw_1}smile"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("highfive"))
async def highfive(client, msg):
    url = f"{url_sfw_1}highfive"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("handhold"))
async def handhold(client, msg):
    url = f"{url_sfw_1}handhold"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("bite"))
async def bite(client, msg):
    url = f"{url_sfw_1}bite"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("slap"))
async def slap(client, msg):
    url = f"{url_sfw_1}slap"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("kill"))
async def killgif(client, msg):
    url = f"{url_sfw_1}kill"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("dance"))
async def dance(client, msg):
    url = f"{url_sfw_1}dance"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)

@Client.on_message(filters.command("cringe"))
async def cringe(client, msg):
    url = f"{url_sfw_1}cringe"
    result = await get_json(url)
    img = result['url']
    await msg.reply_animation(img)
