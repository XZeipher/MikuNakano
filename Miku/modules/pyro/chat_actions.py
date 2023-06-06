from functools import wraps
from Miku import app

def send_action(action):   
    def decorator(func):
        @wraps(func)
        async def command_func(_,msg, *args, **kwargs):
            await app.send_chat_action(
                chat_id=msg.chat.id, action=action
            )
            return await func(_,msg, *args, **kwargs)

        return command_func

    return decorator
