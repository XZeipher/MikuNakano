import time
import asyncio 
from typing import List
from Miku import app,get_readable_time,StartTime
from config import DEV_USERS
from pyrogram import filters
from httpx import AsyncClient
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@app.on_message(filters.command("ping"))
async def _ping(_, message):
    start = time.time()
    msg = await message.reply("⚡")
    end = time.time()
    telegram_ping = str(round((end - start) * 1000, 3)) + " ms"
    uptime = get_readable_time((time.time() - StartTime)) + "uptime"
    await msg.edit(f"""
**• Ping  •
» {telegram_ping}
» {uptime}**""")


sites_list = {
    "Telegram": "https://api.telegram.org",
    "Kaizoku": "https://animekaizoku.com",
    "Kayo": "https://animekayo.com",
    "Jikan": "https://api.jikan.moe/v3",
}


async def ping_func(to_ping: List[str]) -> List[str]:
    ping_result = []

    for each_ping in to_ping:

        start_time = time.time()
        site_to_ping = sites_list[each_ping]
        async with AsyncClient() as client:
            r = await client.get(site_to_ping)
        end_time = time.time()
        ping_time = str(round((end_time - start_time), 2)) + "s"

        pinged_site = f"<b>{each_ping}</b>"

        if each_ping == "Kaizoku" or each_ping == "Kayo":
            pinged_site = f'<a href="{sites_list[each_ping]}">{each_ping}</a>'
            ping_time = f"<code>{ping_time} (Status: {r.status_code})</code>"

        ping_text = f"{pinged_site}: <code>{ping_time}</code>"
        ping_result.append(ping_text)

    return ping_result


@app.on_message(filters.command("pingall") & filters.user(DEV_USERS))
async def _pingall(_, message):
    to_ping = ["Kaizoku", "Kayo", "Telegram", "Jikan"]
    pinged_list = await ping_func(to_ping)
    pinged_list.insert(2, "")
    uptime = get_readable_time((time.time() - StartTime))

    reply_msg = "**⏱ Ping**\n"
    reply_msg += "\n".join(pinged_list)
    reply_msg += f"\n**Uptime:** {uptime}"

    await message.reply_text(
        reply_msg,
        disable_web_page_preview=True,
    )
    
    
