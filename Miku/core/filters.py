from pyrogram import filters as filters_
from pyrogram.types import Message

from Miku import SUDOERS
from Miku import USERBOT_ID as OWNER_ID
from Miku.utils.functions import get_urls_from_text


def url(_, __, message: Message) -> bool:
    text = message.text or message.caption
    if not text:
        return False
    return bool(get_urls_from_text(text))


async def admin(_, __, message: Message) -> bool:
    if message.chat.type not in ["group", "supergroup"]:
        return False
    if not message.from_user:
        return bool(message.sender_chat)
    return message.from_user.id in [
        member.user.id
        async for member in message._client.get_chat_members(
            message.chat.id, filter="administrators"
        )
    ]


def entities(_, __, message: Message) -> bool:
    return bool(message.entities)


def anonymous(_, __, message: Message) -> bool:
    return bool(message.sender_chat)


def sudoers(_, __, message: Message) -> bool:
    if not message.from_user:
        return False
    return message.from_user.id in SUDOERS


def owner(_, __, message: Message) -> bool:
    if not message.from_user:
        return False
    return message.from_user.id == OWNER_ID


class Filters:
    pass


filters = Filters
filters.url = filters_.create(url)
filters.admin = filters_.create(admin)
filters.entities = filters_.create(entities)
filters.anonymous = filters_.create(anonymous)
filters.sudoers = filters_.create(sudoers)
filters.owner = filters_.create(owner)
