from functools import wraps 
from pyrogram import Client
from pyrogram.types import Message
from pyrogram.enums import ChatMemberStatus
from Miku import BOT_ID,app,BOT_NAME
from config import SUPREME_USERS
from pyrogram.enums import ChatType

COMMANDERS = [ChatMemberStatus.ADMINISTRATOR,ChatMemberStatus.OWNER]


# def user_has_permission(permission):
#     def decorator(func):
#         @wraps(func)
#         async def wrapper(client, message: Message):
#             user_id = message.reply_to_message.from_user.id
#             chat_id = message.chat.id

#             x = await client.get_chat_member(chat_id, user_id)
#             privileges = x.privileges.__dict__

#             if permission in privileges and privileges[permission]:
#                 await func(client, message)
#             else:
#                 print(f"User does not have the permission: {permission}")

#         return wrapper

#     return decorator



async def user_has_permission(chat_title : str, chat_id: int, user_id: int, permission: str,bot=True) -> tuple[bool, str]:
    try:
        if user_id in SUPREME_USERS:
            have_permission = True
        else:
            chat_member = await app.get_chat_member(chat_id, user_id)
            chat_permissions = chat_member.privileges
            if permission == "can_delete_messages":
                have_permission = chat_permissions.can_delete_messages
            elif permission == "can_manage_chat":
                have_permission = chat_permissions.can_manage_chat
            elif permission == "can_manage_video_chats":
                have_permission = chat_permissions.can_manage_video_chats
            elif permission == "can_restrict_members":
                have_permission = chat_permissions.can_restrict_members
            elif permission == "can_promote_members":
                have_permission = chat_permissions.can_promote_members
            elif permission == "can_change_info":
                have_permission = chat_permissions.can_change_info
            elif permission == "can_post_messages":
                have_permission = chat_permissions.can_post_messages
            elif permission == "can_edit_messages":
                have_permission = chat_permissions.can_edit_messages
            elif permission == "can_invite_users":
                have_permission = chat_permissions.can_invite_users
            elif permission == "can_pin_messages":
                have_permission = chat_permissions.can_pin_messages    
            else:
                have_permission = False

    except Exception as e:
        print(e)
        have_permission = False

    if not have_permission:
        if bot:
            txt = f"**{BOT_NAME} Doesn'tDoes The Permission:\n__{permission}__\nIn {chat_title}. Please Give Me The Permission To Perform This Action.**"
        else:
            txt = f"**You Don't Have The Permission:\n{permission}\nɪɴ {chat_title}.So I Won't Be Able To Perform This Action.**"
        return have_permission, txt
    else:
        return have_permission, None


def bot_admin(func):
    @wraps(func)
    async def is_bot_admin(app : Client, message : Message,*args,**kwargs):
        chat_type = message.chat.type
        if chat_type == ChatType.PRIVATE:
            return await message.reply("**This Command Was Made For Groups Not Private**")
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)                 
        if BOT.status != ChatMemberStatus.ADMINISTRATOR:                                       
            await message.reply_text(f"**{BOT_NAME} Isn't Admin In {message.chat.title}**")
            return 
        return await func(app,message,*args,**kwargs)
    return is_bot_admin

def bot_can_ban(func):
    @wraps(func)
    async def can_restrict(app : Client, message : Message,*args,**kwargs):
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)
                 
        if not BOT.privileges.can_restrict_members:                        
            await message.reply_text(f"**{BOT_NAME} Has No Permission To Restrict In {message.chat.title}. Check And Give Me Rights💕**")
            return 
        return await func(app,message,*args,**kwargs)
    return can_restrict

def bot_can_change_info(func):
    @wraps(func)
    async def can_change_info(app : Client, message : Message,*args,**kwargs):
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)

        if not BOT.privileges.can_change_info:                         
            await message.reply_text(f"**{BOT_NAME} Has Permission To Change Info In {message.chat.title}. Check And Give Me Rights💕**")
            return 
        return await func(app,message,*args,**kwargs)
    return can_change_info


def bot_can_promote(func):
    @wraps(func)
    async def can_promote(app : Client, message : Message,*args,**kwargs):
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)

        if not BOT.privileges.can_promote_members:                         
            await message.reply_text(f"**{BOT_NAME} Has No Permission To Promote Users In {message.chat.title}. Check And Give Me Rights💕**")
            return 
        return await func(app,message,*args,**kwargs)
    return can_promote


def bot_can_pin(func):
    @wraps(func)
    async def can_pin(app : Client, message : Message,*args,**kwargs):
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)

        if not BOT.privileges.can_pin_messages:                         
            await message.reply_text(f"**{BOT_NAME} Has No Permission To Pin Messages In {message.chat.title}. Check And Give Me Rights💕**")
            return 
        return await func(app,message,*args,**kwargs)
    return can_pin

def bot_can_del(func):
    @wraps(func)
    async def can_delete(app : Client, message : Message,*args,**kwargs):
        BOT = await app.get_chat_member(message.chat.id,BOT_ID)

        if not BOT.privileges.can_delete_messages:                         
            await message.reply_text(f"**{BOT_NAME} Has No Permission To Delete Messages In {message.chat.title}. Check And Give Me Rights💕**")
            return 
        return await func(app,message,*args,**kwargs)
    return can_delete

def user_admin(mystic):
    @wraps(mystic)
    async def wrapper(app : Client, message : Message,*args,**kwargs):
        chat_type = message.chat.type
        if chat_type == ChatType.PRIVATE:
            return await message.reply("**This Command Was Made For Group Not Private.**")
        if message.sender_chat:
            if message.sender_chat.id == message.chat.id:
                return await message.reply("**You Are An Anonymous Admin I Can't Perform This Action. Please Use Real ID.**")
            else:
                return await message.reply_text("**You Aren't An Admin.**")
                
        else:
            user_id = message.from_user.id    
            chat_id = message.chat.id
            user = await app.get_chat_member(chat_id,user_id) 
        
            if (user.status not in COMMANDERS) and user_id not in SUPREME_USERS:
                return await message.reply_text("**You Aren't An Admin.**")
                                                                            
        return await mystic(app,message,*args,**kwargs)

    return wrapper

def user_can_ban(mystic):
    @wraps(mystic)
    async def wrapper(app : Client, message : Message,*args,**kwargs):
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = await app.get_chat_member(chat_id,user_id)
        
        if (user.privileges and not user.privileges.can_restrict_members) and user_id not in SUPREME_USERS: 

            return await message.reply_text("**You Don't Have Rights To Restrict Users. Sorry Can't Perform This Action.**") 
                                                    
        return await mystic(app,message,*args,**kwargs)
    return wrapper

def user_can_del(mystic):
    @wraps(mystic)
    async def wrapper(app : Client, message : Message,*args,**kwargs):
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = await app.get_chat_member(chat_id,user_id)
        
        if (user.status in COMMANDERS and not user.privileges.can_delete_messages) and user_id not in SUPREME_USERS:                     
            return await message.reply_text("**You Don't Have Rights To Delete Messages. Sorry Can't Perform This Action.**") 
                                                    
        return await mystic(app,message,*args,**kwargs)
    return wrapper
            

def user_can_change_info(mystic):
    @wraps(mystic)
    async def wrapper(app : Client, message : Message,*args,**kwargs):
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = await app.get_chat_member(chat_id,user_id)
        
        if (user.status in COMMANDERS and not user.privileges.can_change_info) and user_id not in SUPREME_USERS:                     
            return await message.reply_text("**You Don't Have Rights To Change Info. Sorry Can't Perform This Action.**") 
                                                    
        return await mystic(app,message,*args,**kwargs)
    return wrapper
            
def user_can_promote(mystic):
    @wraps(mystic)
    async def wrapper(app : Client, message : Message,*args,**kwargs):
        user_id = message.from_user.id
        chat_id = message.chat.id
        user = await app.get_chat_member(chat_id,user_id)
        
        if (user.status in COMMANDERS and not user.privileges.can_promote_members) and user_id not in SUPREME_USERS:                     
            return await message.reply_text("**You Don't Have Rights To Promote Users. Sorry Can't Perform This Action.**") 
                                                    
        return await mystic(app,message,*args,**kwargs)
    return wrapper
            
