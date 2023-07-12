from pyrogram import filters
from Miku import app
from Miku.modules.mongo.whisper_db import Whispers
from pyrogram.types import *
import shortuuid


@app.on_inline_query()
async def mainwhisper(_, query):
    if not query.query:
        await query.answer([], switch_pm_text="Give me a username or ID!", switch_pm_parameter="ghelp_whisper")
        return

    user = query.query.split(' ')[0]
    first = True

    if not user.startswith('@') and not user.isdigit():
        user = query.query.split(' ')[-1]
        first = False

    if not user.startswith('@') and not user.isdigit():
        await query.answer([], switch_pm_text="Give me a username or ID!", switch_pm_parameter="ghelp_whisper")
        return

    if user.isdigit():
        try:
            chat = await app.get_chat(int(user))
            user = f"@{chat.username}" if chat.username else chat.first_name
        except:
            user = user

    message = ' '.join(query.query.split(' ')[1:]) if first else ' '.join(query.query.split(' ')[:1])

    if len(message) > 200:
        await query.answer([], switch_pm_text="Only text up to 200 characters is allowed!", switch_pm_parameter="ghelp_whisper")
        return

    answers = [
        InlineQueryResultArticle(
            title=f' Send a whisper message to {user}!',
            description='Only they can see it!',
            input_message_content=InputTextMessageContent('Generating Whisper message...'),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(' Show Whisper', callback_data=f'whisper_{shortuuid.uuid()}')]])
        )
    ]
    await query.answer(answers)

@app.on_callback_query()
async def showwhisper(_, callback_query):
    whisper_id = callback_query.data.split('_')[-1]
    whisper_data = await Whispers.get_whisper(whisper_id)  # Await the call to get_whisper
    if not whisper_data:
        await callback_query.answer("This whisper is not valid anymore!")
        return

    user_type = whisper_data['usertype']

    if callback_query.from_user.id == whisper_data['user']:
        await callback_query.answer(whisper_data['message'], show_alert=True)
    elif user_type == 'username' and callback_query.from_user.username and callback_query.from_user.username.lower() == whisper_data['withuser'].replace('@', '').lower():
        await callback_query.answer(whisper_data['message'], show_alert=True)
        await Whispers.del_whisper(whisper_id)  # Await the call to del_whisper
        await callback_query.edit_message_text(f"**{whisper_data['withuser']} read the Whisper.**")
    elif user_type == 'id' and callback_query.from_user.id == int(whisper_data['withuser']):
        user = await app.get_users(int(whisper_data['withuser']))
        username = user.username or user.first_name
        await callback_query.answer(whisper_data['message'], show_alert=True)
        await Whispers.del_whisper(whisper_id)  # Await the call to del_whisper
        await callback_query.edit_message_text(f"**{username} read the whisper.**")
    else:
        await callback_query.answer("No one sent you a whisper.", show_alert=True)


__help__ = """
**Whisper Inline Function For Secret Chats.**

**Commands**
 `@MikuNakanoXSupport your message @username OR UserID`
 `@MikuNakanoXSupport @username OR UserID your message`
"""
__mod_name__ = "Whispers"
