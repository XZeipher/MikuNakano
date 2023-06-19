import httpx
from Miku import app, BOT_USERNAME
from pyrogram import filters, enums
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from app.modules.pyro.chat_actions import send_action

BUTTONS = [
    [
        InlineKeyboardButton(
            text="Contact Me In Private",
            url=f"https://t.me/{BOT_USERNAME}?start=true",
        ),
    ],
]


@app.on_message(filters.command("cosplay"))
@send_action(enums.ChatAction.UPLOAD_PHOTO)
async def _cosplay(_, message):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://waifu-api.vercel.app")
        pic = response.json()
        await message.reply_photo(pic)


@app.on_message(filters.command("ncosplay"))
@send_action(enums.ChatAction.UPLOAD_PHOTO)
async def _lewd(_, message):
    if message.chat.type != ChatType.PRIVATE:
        await message.reply_text(
            "**This Command Can Be Used In PM.**",
            reply_markup=InlineKeyboardMarkup(BUTTONS),
        )
        return
    async with httpx.AsyncClient() as client:
        response = await client.get("https://waifu-api.vercel.app/items/1")
        pic = response.json()
        await message.reply_photo(pic)


__help__ = """
**Random Anime Cosplay**

**Commands**

♠ `/cosplay` : random sfw anime cosplay.
♠ `/ncosplay` : random nsfw anime cosplay.

"""

__mod_name__ = "Cosplay"
