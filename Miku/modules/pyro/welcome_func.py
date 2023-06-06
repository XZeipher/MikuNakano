from enum import Enum, auto
import html
import pyrogram
from pyrogram.types import InlineKeyboardMarkup
from Miku import app



class WelcomeDataType(Enum):
    text = auto()
    sticker = auto()
    animation= auto()
    document = auto()
    photo = auto()
    audio = auto()
    voice = auto()
    video = auto()
    video_note = auto()


def GetWelcomeMessage(message):
    data_type = None
    content = None
    text = str()

    if not (
        message.reply_to_message
    ):
        content = None
        text = message.text.markdown[len(message.command[0]) + 2 :]
        data_type = WelcomeDataType.text.value

    elif (
        message.reply_to_message
        and message.reply_to_message.text
    ):
        content = None
        text = message.reply_to_message.text.markdown 
        data_type = WelcomeDataType.text.value

    elif (
        message.reply_to_message
        and message.reply_to_message.sticker
    ):
        content = message.reply_to_message.sticker.file_id
        data_type = WelcomeDataType.sticker.file_id
    
    elif (
        message.reply_to_message
        and message.reply_to_message.animation
    ):
        content = message.reply_to_message.animation.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown
        data_type = WelcomeDataType.animation.value

    elif (
        message.reply_to_message
        and message.reply_to_message.document
    ):
        content = message.reply_to_message.document.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type = WelcomeDataType.document.value

    elif (
        message.reply_to_message
        and message.reply_to_message.photo
    ):
        content = message.reply_to_message.photo.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown
        data_type = WelcomeDataType.photo.value

    elif (
        message.reply_to_message
        and message.reply_to_message.audio
    ):
        content = message.reply_to_message.audio.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type = WelcomeDataType.audio.value

    elif (
        message.reply_to_message
        and message.reply_to_message.voice
    ):
        content = message.reply_to_message.voice.file_id
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type = WelcomeDataType.voice.value

    elif (
        message.reply_to_message
        and message.reply_to_message.video
    ):
        content = message.reply_to_message.video.file_id 
        if message.reply_to_message.caption:
            text = message.reply_to_message.caption.markdown 
        data_type= WelcomeDataType.video.value

    elif (
        message.reply_to_message
        and message.reply_to_message.video_note
    ):
        content = message.reply_to_message.video_note.file_id
        text = None 
        data_type = WelcomeDataType.video_note.value
    
    return (
        content,
        text,
        data_type
    )





def Welcomefillings(message, message_text, NewUserJson):
  if not NewUserJson == None:
    user_id = NewUserJson.id 
    first_name = NewUserJson.first_name 
    last_name = NewUserJson.last_name
    if last_name == None:
      last_name = ''
    full_name = f'{first_name} {last_name}'
    username = NewUserJson.username
    mention = NewUserJson.mention 
    chat_title = html.escape(message.chat.title)
    
    try:
      FillingText = message_text.format(
        id=user_id,
        first=first_name,
        fullname=full_name,
        username=username,
        mention=mention,
        chatname=chat_title
        ) 
    except KeyError:
      FillingText = message_text

  else:
    FillingText = message_text
  
  return FillingText





async def SendWelcomeMessage(message, NewUserJson, content, text, data_type, reply_markup):
    message_id = message.id
    chat_id = message.chat.id
    text = Welcomefillings(message, text, NewUserJson)
    SentMessage = None
    
    if (
        data_type == 1
    ):
        SentMessage = await app.send_message(
            chat_id=chat_id,
            text=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    
    elif (
        data_type == 2
    ):
        SentMessage = await app.send_sticker(
            chat_id=chat_id,
            sticker=content,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    
    elif (
        data_type == 3
    ):
        SentMessage = await app.send_animation(
            chat_id=chat_id,
            animation=content,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )

    elif (
        data_type == 4
    ):
        
        SentMessage = await app.send_document(
            chat_id=chat_id,
            document=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )

    elif (
        data_type == 5
    ):
        SentMessage = await app.send_photo(
          chat_id=chat_id,
          photo=content,
          caption=text,
          reply_to_message_id=message_id,
          reply_markup=reply_markup
      )  
    
    elif (
        data_type == 6
    ):
        SentMessage = await app.send_audio(
            chat_id=chat_id,
            audio=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    elif (
        data_type == 7
    ):
        SentMessage = await app.send_voice(
            chat_id=chat_id,
            voice=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    
    elif (
        data_type == 8
    ):
        SentMessage = await app.send_video(
            chat_id=chat_id,
            video=content,
            caption=text,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    
    elif (
        data_type == 9
    ):
        SentMessage = await app.send_video_note(
            chat_id=chat_id,
            video_note=content,
            reply_to_message_id=message_id,
            reply_markup=reply_markup
        )
    
    return SentMessage
