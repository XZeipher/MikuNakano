import re
import os
import glob
from Miku import app
from pyrogram import filters, enums
from unidecode import unidecode
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import BadRequest
from geniuses import GeniusClient
import aiohttp
from bs4 import BeautifulSoup
from requests import post
from bing_image_downloader import downloader
from Miku.modules.pyro.chat_actions import send_action
from Miku.modules.antinsfw import get_file_id_from_message
from config import BOT_TOKEN as bot_token

async def Sauce(bot_token, file_id):
    async with aiohttp.ClientSession() as session:
        async with session.post(f'https://api.telegram.org/bot{bot_token}/getFile?file_id={file_id}') as response:
            json_data = await response.json()
            file_path = json_data['result']['file_path']
            headers = {'User-agent': 'Mozilla/5.0 (Linux; Android 6.0.1; SM-G920V Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36'}
            to_parse = f"https://images.google.com/searchbyimage?safe=off&sbisrc=tg&image_url=https://api.telegram.org/file/bot{bot_token}/{file_path}"
            async with session.get(to_parse, headers=headers) as response:
                soup = BeautifulSoup(await response.text(), 'html.parser')
                result = {
                    "similar": '',
                    'output': ''
                }
                for similar_image in soup.find_all('input', {'class': 'gLFyf'}):
                    url = f"https://www.google.com/search?tbm=isch&q={quote_plus(similar_image.get('value'))}"
                    result['similar'] = url
                for best in soup.find_all('div', {'class': 'r5a77d'}):
                    output = best.get_text()
                    decoded_text = unidecode(output)
                    result["output"] = decoded_text

                return result

@app.on_message(filters.command(["p", "pp", "grs", "reverse"]) & filters.group)
async def _reverse(_, msg):
    text = await msg.reply("**⇢ wait a sec...**")
    file_id = await get_file_id_from_message(msg)
    if not file_id:
        return await text.edit("**reply to character!**")
    await text.edit("**⇢ Requesting to Google....**")
    result = await Sauce(bot_token, file_id)
    if not result["output"]:
        return await text.edit("Couldn't find anything")
    await text.edit(f'[{result["output"]}]({result["similar"]})', reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Site", url=result["similar"])]]
    ))

@app.on_message(filters.command("lyrics"))
@send_action(enums.ChatAction.TYPING)
async def _lyrics(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Provide Me A Text To Extract Lyrics.**")
    GENIUSES_API_KEY = (
        "gIgMyTXuwJoY9VCPNwKdb_RUOA_9mCMmRlbrrdODmNvcpslww_2RIbbWOB8YdBW9"
    )
    q = message.text.split(None, 1)[1]
    g_client = GeniusClient(GENIUSES_API_KEY)
    songs = g_client.search(q)
    if len(songs) == 0:
        return await e.reply(
            "**Lyrics Not Found.**",
        )
    song = songs[0]
    name = song.title
    song.header_image_thumbnail_url
    lyrics = song.lyrics
    for x in ["Embed", "Share URL", "Copy"]:
        if x in lyrics:
            lyrics = lyrics.replace(x, "")
    pattern = re.compile("\n+")
    lyrics = pattern.sub("\n", lyrics)
    out_str = f"**{name}**\n`{lyrics}`"
    await message.reply_text(out_str)


@app.on_message(filters.command("google") & filters.group)
async def _google(_, message):
    try:
        query = message.text.split(None, 1)[1]
    except IndexError:
        return await message.reply(
            "**Provide Me A Valid Query.**",
        )
    url = f"https://www.google.com/search?&q={query}&num=5"
    usr_agent = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/61.0.3163.100 Safari/537.36"
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=usr_agent) as response:
            soup = BeautifulSoup(await response.text(), "html.parser")
            results = soup.find_all("div", attrs={"class": "g"})
            final = f"**Results** :-\n<b>{query}</b>:"
            if not results or len(results) == 0:
                return await e.reply(
                    "**No Result Found.**",
                )
            for x in results:
                link = (x.find("a", href=True))["href"]
                name = x.find("h3")
                if link and name:
                    if not name == "Images" and not name == "Description":
                        final += f"\n- <a href='{link}'>{name}</a>"
            await message.reply_text(final, disable_web_page_preview=True)

__help__ = """
**Modules Based On Google Scraping.**

**Commands**

♠ `/google <text>`: search anything on google.

♠ `/reverse` : search images details.

♠ `/lyrics` : search song lyrics.
"""

__mod_name__ = "Google"
