from Miku import app,BOT_USERNAME
from pyrogram import filters , Client
from Miku.modules.mongo.notes_db import *
from Miku.modules.pyro.notes_func import GetNoteMessage, exceNoteMessageSender, privateNote_and_admin_checker
from Miku.modules.pyro.status import user_admin
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup , Message , CallbackQuery
from pyrogram.enums import ChatMemberStatus


@Client.on_message(filters.command("save") & filters.group)
@user_admin
async def _save(client, message):
    chat_id = message.chat.id
    chat_title = message.chat.title
    if message.reply_to_message and not len(message.command) >= 2:
        return await message.reply_text("**Provide Me A Note Name In Order To Save That!**")
    
    if not message.reply_to_message and not len(message.command) >= 3:
        return await message.reply_text("**Provide Me A Note Name In Order To Save That!**")
    
    NoteName = message.command[1]
    Content, Text, DataType = GetNoteMessage(message)
    await SaveNote(chat_id, NoteName, Content, Text, DataType)

    await message.reply_text(f"**Saved Note** `{NoteName}`!")
    



@Client.on_message(filters.command("get") & filters.group)
async def _getnote(client, message):
    chat_id = message.chat.id
    if not len(message.command) >= 2:
        return await message.reply_text("**Specify a note name!**")  
    note_name = message.command[1]
    if not await isNoteExist(chat_id, note_name):
         return await message.reply_text("**Note not found**")
    await send_note(message, note_name)
    

@Client.on_message(filters.regex(pattern=(r"^#[^\s]+")) & filters.group)
async def regex_get_note(client, message):
    chat_id = message.chat.id
    if message.from_user:
        note_name = message.text.split()[0].replace('#', '')
        if await isNoteExist(chat_id, note_name):
            await send_note(message, note_name)


PRIVATE_NOTES_TRUE = ['on', 'true', 'yes', 'y']
PRIVATE_NOTES_FALSE = ['off', 'false', 'no', 'n']

@Client.on_message(filters.command("privatenotes") & filters.group)
@user_admin
async def PrivateNote(client, message):
    chat_id = message.chat.id
    if len(message.command) >= 2:
        if (
            message.command[1] in PRIVATE_NOTES_TRUE
        ):
            await set_private_note(chat_id, True)
            await message.reply(
                "**Now i will send a message to your chat with a button redirecting to PM, where the user will receive the note.**",
                quote=True
            )

        elif (
            message.command[1] in PRIVATE_NOTES_FALSE
        ):
            await set_private_note(chat_id, False)
            await message.reply(
                "**I will now send notes straight to the group.**",
                quote=True
            )  
        else:
            await message.reply(
                f"**failed to get boolean value from input: expected one of y/yes/on/true or n/no/off/false; got: {message.command[1]}**",
                quote=True
            )
    else:
        if await is_pnote_on(chat_id):
            await message.reply(
                "**Your notes are currently being sent in private. Stella will send a small note with a button which redirects to a private chat.**",
                quote=True
            )
        else:
            await message.reply(
                "**Your notes are currently being sent in the group.**",
                quote=True
            )
            
@Client.on_message(filters.command("clear") & filters.group)
@user_admin
async def Clear_Note(client, message):
    chat_id = message.chat.id 
    if not (
        len(message.command) >= 2
    ):
        await message.reply(
            "**Provide a notename.**",
            quote=True
        )
        return
    
    note_name = message.command[1].lower()

    if await isNoteExist(chat_id, note_name):
        await ClearNote(chat_id, note_name)

        await message.reply(
            f"**Removed Note** `{note_name}`!",
            quote=True
        )
    else:
        await message.reply(
            "**You haven't saved a note with this name yet!**",
            quote=True
        )


@Client.on_message(filters.command("clearall") & filters.group)
async def ClearAll_Note(client, message):
    owner_id = message.from_user.id
    chat_id = message.chat.id 
    chat_title = message.chat.title
    user = await client.get_chat_member(chat_id,owner_id)
    if not user.status == ChatMemberStatus.OWNER :
        return await message.reply_text("**You Need To Be The Group Creator In Order To Use This Command.**")

    note_list = await NoteList(chat_id)
    if note_list == 0:
        await message.reply(
            f"**No notes available**",
            quote=True
        )
    keyboard = InlineKeyboardMarkup(
        [[
            InlineKeyboardButton(text='Remove', callback_data=f'clearallnotes_clear_{owner_id}_{chat_id}')
        ],
        [
            InlineKeyboardButton(text='Cancel', callback_data=f'clearallnotes_cancel_{owner_id}')
        ]]
    )
    await message.reply(
        f"**Are you sure you want to clear All notes in {chat_title}?**",
        reply_markup=keyboard,
        quote=True
    )

@Client.on_callback_query(filters.regex("^clearallnotes_"))
async def ClearAllCallback(client, callback_query: CallbackQuery):
    query_data = callback_query.data.split('_')[1]
    owner_id = int(callback_query.data.split('_')[2])
    user_id = callback_query.from_user.id 

    if owner_id == user_id:
        if query_data == 'clear':
            chat_id = int(callback_query.data.split('_')[3])
            await ClearAllNotes(chat_id)
            await callback_query.edit_message_text(
                "**Removed All Notes!**"
            ) 
            return
            
        elif query_data == 'cancel':
            await callback_query.edit_message_text(
                "**Cancelled.**"
            )
    else:
        await callback_query.answer(
            "**You Need to Be Admin First!**"
        )
                         
@Client.on_message(filters.command(['notes', 'saved']) & filters.group)
async def Notes(client, message):
    
    chat_id = message.chat.id
    chat_title = message.chat.title

    Notes_list = await NoteList(chat_id)
    
    NoteHeader = f"**♠ Notes ♠**\n"
    if (
        len(Notes_list) != 0
    ): 
        for notes in Notes_list:
            NoteName = f" • `#{notes}`\n"
            NoteHeader += NoteName
        await message.reply(
            (
                f"{NoteHeader}\n"
                "**You can retrieve these notes by using** `/get notename`, or `#notename`"
            ),
            quote=True
        )
        
    else:
        await message.reply(
            f"**No Notes Saved!**",
            quote=True
        )        
async def send_note(message: Message, note_name: str):
    chat_id = message.chat.id  
    content, text, data_type = await GetNote(chat_id, note_name)
    privateNote, allow = await privateNote_and_admin_checker(message, text)   
    if allow:
        if privateNote == None:
            if await is_pnote_on(chat_id):
                await PrivateNoteButton(message, chat_id, note_name)
            else:
                await exceNoteMessageSender(message, note_name)
            
        elif privateNote is not None:
            if await is_pnote_on(chat_id):
                if privateNote:
                    await PrivateNoteButton(message, chat_id, note_name)
                else:
                    await exceNoteMessageSender(message, note_name)
            else: 
                if privateNote:
                    await PrivateNoteButton(message, chat_id, note_name)
                else:
                    await exceNoteMessageSender(message, note_name)
                    
                    

async def note_redirect(message):
    chat_id = int(message.command[1].split('_')[1])
    note_name = message.command[1].split('_')[2]
    await exceNoteMessageSender(message, note_name, from_chat_id=chat_id)

async def PrivateNoteButton(message, chat_id, NoteName):
    PrivateNoteButton = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text='Click me!', url=f'http://t.me/{BOT_USERNAME}?start=note_{chat_id}_{NoteName}')
            ]
        ]
    )
    await message.reply(
        text=f"**Tap here to view** '{NoteName}' **in your private chat.**",
        reply_markup=PrivateNoteButton
    )
