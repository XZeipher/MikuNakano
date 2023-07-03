from pyrogram import filters
from pyrogram.types import *
from pyrogram.enums import ChatType
from Miku import app

LOG_ID = int("-1001813613591")

@app.on_message(filters.command(["report", "bug" , "feedback"]))
async def requests(client: app, message: Message):
	if message.chat.type == ChatType.PRIVATE:
		return await message.reply_text("**Report Can Be Done In Groups Only.**")
    text_link = message.link
    text = message.text.split(None)[1]
    EVENT = InlineKeyboardMarkup(
  [
    [
      InlineKeyboardButton(
        text="Event", url=text_link
      )
    ]
  ]
    )

    USER_TEXT = f'''**<a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a> your report has been successfully sent to our developers
ThankYou :)**'''
    DEV_TEXT = f'''**#Report

User :- <a href="tg://user?id={message.from_user.id}">{message.from_user.first_name}</a>
Text :- {text}**
'''
    await client.send_message(LOG_ID, DEV_TEXT,reply_markup=EVENT)
    await message.reply_text(USER_TEXT)
