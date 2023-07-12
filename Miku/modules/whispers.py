from pyrogram import filters
from Miku import app
from Miku.modules.mongo.whisper_db import Whispers
from pyrogram.types import *
import shortuuid


@app.on_inline_query()
async def mainwhisper(_, query):
    if not query.query:
        return await query.answer([], switch_pm_text='Give me a username or ID!', switch_pm_parameter='ghelp_whisper')

    text = query.query.split(' ')
    user = text[0]
    first = True
    if not user.startswith('@') and not user.isdigit():
        user = text[-1]
        first = False
    if first:
        message = ' '.join(text[1:])
    else:
        text.pop()
        message = ' '.join(text)
    if len(message) > 200:
        return
    usertype = 'username'
    whisperType = 'inline'
    if user.startswith('@'):
        usertype = 'username'
    elif user.isdigit():
        usertype = 'id'
    if user.isdigit():
        try:
            chat = await app.get_chat(int(user))
            user = f"@{chat.username}" if chat.username else chat.first_name
        except:
            user = user

    message = ' '.join(text[1:]) if first else ' '.join(text[:1])

    if len(message) > 200:
        await query.answer([], switch_pm_text='Only text up to 200 characters is allowed!', switch_pm_parameter='ghelp_whisper') 
        return

    whisperData = {'user': query.from_user.id, 'withuser': user, 'usertype': usertype, 'type': 'inline', 'message': message}
    whisperId = shortuuid.uuid()

    # Add the whisper to the database
    await Whispers.add_whisper(whisperId, whisperData)

    answers = [
        InlineQueryResultArticle(
            title=f' Send a whisper message to {user}!',
            description='Only they can see it!',
            input_message_content=InputTextMessageContent(f' A Whisper Message For {user}\nOnly they can see it!'),
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton(' Show Whisper', callback_data=f'whisper_{whisperId}')]])
        )
    ]

    await query.answer(answers)


@app.on_callback_query(filters.regex('^whisper_'))
async def showWhisper(_, callback_query):
    whisperId = callback_query.data.split('_')[-1]
    whisper = await Whispers.get_whisper(whisperId)

    if not whisper:
        await callback_query.answer("This whisper is not valid anymore!")
        return

    userType = whisper['usertype']

    if callback_query.from_user.id == whisper['user']:
        await callback_query.answer(whisper['message'], show_alert=True)
    elif userType == 'username' and callback_query.from_user.username and callback_query.from_user.username.lower() == whisper['withuser'].replace('@', '').lower():
        await callback_query.answer(whisper['message'], show_alert=True)
        await Whispers.del_whisper(whisperId)
        await callback_query.edit_message_text(f"{whisper['withuser']} read the Whisper.")
    elif userType == 'id' and callback_query.from_user.id == int(whisper['withuser']):
        user = await app.get_users(int(whisper['withuser']))
        username = user.username or user.first_name
        await callback_query.answer(whisper['message'], show_alert=True)
        await Whispers.del_whisper(whisperId)
        await callback_query.edit_message_text(f"{username} read the whisper.")
    else:
        await callback_query.answer("Not your Whisper!", show_alert=True)


__help__ = """
**Whisper Inline Function For Secret Chats.**

**Commands**
 `@MikuNakanoXSupport your message @username OR UserID`
 `@MikuNakanoXSupport @username OR UserID your message`
"""
__mod_name__ = "Whispers"
