from Miku import app
from pyrogram import filters  , Client
from Miku.modules.pyro.status import (
    bot_admin,
    user_admin,
    bot_can_pin)

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , CallbackQuery 
from pyrogram import Client,enums
from pyrogram.handlers import CallbackQueryHandler

@Client.on_message(filters.command("pin") & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def _pin(_, message):
    replied = message.reply_to_message
    user_id = message.from_user.id
    if not replied:
        return await message.reply_text("**Reply to message to pin it!**")
    try:
        await replied.pin(disable_notification=True)
        await message.reply_text("**Pinned!**",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="Text",url=replied.link),InlineKeyboardButton(text="unpin", callback_data=f"unpin_{user_id}_{replied.id}")]]))
    except Exception as er:
        await message.reply_text(er)

@Client.on_message(filters.command("pinned") & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def _pin(_, message):
    chat = await pgram.get_chat(message.chat.id)
    if not chat.pinned_message:
        return await message.reply_text("**No Pinned Message Found!**")
    try:        
        await message.reply_text("**🖇️ Last Pinned Messages**",reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton(text="Text",url=chat.pinned_message.link)]]))  
    except Exception as er:
        await message.reply_text(er)


@Client.on_message(filters.command(["unpin","unpinall"]) & ~filters.private)
@bot_admin
@user_admin
@bot_can_pin
async def _unpinmsg(_, message):
    if message.command[0] == "unpin":
        replied = message.reply_to_message
        if not replied:
            return await message.reply_text("**Reply to message to pin it!**")
        try:
            await replied.unpin()
            await message.reply_text("**Unpinned!**",reply_markup=
            InlineKeyboardMarkup([[InlineKeyboardButton(text="Text",url=replied.link)]]))  
        except Exception as er:
            await message.reply_text(er)
    if message.command[0] == "unpinall":
        await app.unpin_all_chat_messages(message.chat.id)
        await message.reply_text("**Unpinned all messages!**", reply_markup=
        InlineKeyboardMarkup([[InlineKeyboardButton("❌ ᴄʟᴏsᴇ", callback_data="admin_close")]]))

@Client.on_callback_query(filters.regex(pattern=r"unpin_(.*)"))
async def unpin_btn(app : Client, query : CallbackQuery):
    user_id = query.from_user.id
    chat_id = query.message.chat.id
    ids = query.data.split("_")  
    if int(ids[1]) == user_id:
        await app.unpin_chat_message(chat_id,int(ids[2])) 
        await query.message.edit("**Unpinned!**")
    else:
        await app.answer_callback_query(
        query.id,
    text="**This message isn't pinned by you!**",
    show_alert=True
)
