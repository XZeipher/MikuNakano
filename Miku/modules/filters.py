import re
from Miku import app
from Miku.modules.mongo.filters_db import *
from Miku.modules.pyro.filters_func import GetFIlterMessage,get_text_reason,SendFilterMessage
from Miku.modules.pyro.status import user_admin
from pyrogram import filters
from Miku.utils.filter_groups import filter_watcher
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup)


@app.on_message(filters.command("filter") & filters.group)
async def _filter(client, message):
    
    chat_id = message.chat.id 
    if (
        message.reply_to_message
        and not len(message.command) == 2
    ):
        await message.reply(
            "**You need to give me a text to set in filters.**"
        )  
        return 
    
    filter_name, filter_reason = get_text_reason(message)
    if (
        message.reply_to_message
        and not len(message.command) >=2
    ):
        await message.reply(
            "**You need to give me a text to set in filters.**"
        )
        return

    content, text, data_type = await GetFIlterMessage(message)
    await add_filter_db(chat_id, filter_name=filter_name, content=content, text=text, data_type=data_type)
    await message.reply(
        f"**Saved filter :** `{filter_name}`"
    )



@app.on_message(filters.all & filters.group, group=filter_watcher)
async def FilterCheckker(client, message):
    if not message.text:
        return
    text = message.text
    chat_id = message.chat.id
    if (
        len(await get_filters_list(chat_id)) == 0
    ):
        return

    ALL_FILTERS = await get_filters_list(chat_id)
    for filter_ in ALL_FILTERS:
        
        if (
            message.command
            and message.command[0] == 'filter'
            and len(message.command) >= 2
            and message.command[1] ==  filter_
        ):
            return
            
        pattern = r"( |^|[^\w])" + re.escape(filter_) + r"( |$|[^\w])"
        if re.search(pattern, text, flags=re.IGNORECASE):
            filter_name, content, text, data_type = await get_filter(chat_id, filter_)
            await SendFilterMessage(
                message=message,
                filter_name=filter_,
                content=content,
                text=text,
                data_type=data_type
            )
@app.on_message(filters.command('filters') & filters.group)
async def _filters(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    if message.chat.type == 'private':
        chat_title = 'local'
    FILTERS = await get_filters_list(chat_id)
    
    if len(FILTERS) == 0:
        await message.reply(
            f'**There Is No Filters In {chat_title}.**'
        )
        return

    filters_list = f'**♠ Filters In {chat_title} ♠\n**'
    
    for filter_ in FILTERS:
        filters_list += f'• `{filter_}`\n'
    
    await message.reply(
        filters_list
    )


@app.on_message(filters.command('removeallfilters') & filters.group)
async def stopall(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title 
    user = await client.get_chat_member(chat_id,message.from_user.id)
    if user.status != ChatMemberStatus.OWNER :
        return await message.reply_text("**You Need To Be Group Creator To Use This Command.**") 

    KEYBOARD = InlineKeyboardMarkup(
        [[InlineKeyboardButton(text='Remove All Filters 🗑️', callback_data='custfilters_stopall')],
        [InlineKeyboardButton(text='Cancel ❌', callback_data='custfilters_cancel')]]
    )

    await message.reply(
        text=(
            f'**Are You Sure You Want To Remove All Filters.**'
        ),
        reply_markup=KEYBOARD
    )


@app.on_callback_query(filters.regex("^custfilters_"))
async def stopall_callback(client, callback_query: CallbackQuery):  
    chat_id = callback_query.message.chat.id 
    query_data = callback_query.data.split('_')[1]  
    user = await client.get_chat_member(chat_id,callback_query.from_user.id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("**You Need To Be Group Creator To Use This Command.**") 
    
    if query_data == 'stopall':
        await stop_all_db(chat_id)
        await callback_query.edit_message_text(
            text='**Removed All Filters.**'
        )
    
    elif query_data == 'cancel':
        await callback_query.edit_message_text(
            text='**Canceled.**'
        )

@app.on_message(filters.command('stop') & filters.group)
@user_admin
async def stop(client, message):
    chat_id = message.chat.id
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            '**Give Me A Filter To Stop That.**'
        )
        return
    
    filter_name = message.command[1]
    if (
        filter_name not in await get_filters_list(chat_id)
    ):
        await message.reply(
            "**This Word Isn't Available In Filters.**"
        )
        return
    
    await stop_db(chat_id, filter_name)
    await message.reply(
        f'**Stopped :** `{filter_name}`'
    )
