import psycopg2
from pyrogram import *
from Miku import app, BOT_ID
from Miku.modules.pyro.status import user_admin, bot_admin, bot_can_ban
from pyrogram.enums import ChatMemberStatus
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, ChatPermissions
from pyrogram.errors import BadRequest

DB_URL = "postgres://qfpqlxhq:FVU_uUXjM5ESmdny5Of2KmS_PS_v9L9J@arjuna.db.elephantsql.com/qfpqlxhq"

HOST = DB_URL.split("@")[1].split("/")[0]
USER = DB_URL.split("postgres://")[1].split(":")[0]
PASS = DB_URL.split(":")[2].split("@")[0]

DB = psycopg2.connect(
    host=HOST,
    port='5432',
    user=USER,
    password=PASS,
    database=USER
)
cusr = DB.cursor()
DB.rollback()
DB.autocommit = True

cusr.execute("""
    CREATE TABLE IF NOT EXISTS fsub (
        id SERIAL PRIMARY KEY,
        fsub_on VARCHAR(255) NOT NULL,
        channel VARCHAR(255) NOT NULL
    )
""")
DB.commit()


async def fsub_off(chat_id):
    cusr.execute("SELECT * FROM fsub WHERE fsub_on = %s", (chat_id,))
    chat = cusr.fetchone()
    if chat:
        cusr.execute("DELETE FROM fsub WHERE fsub_on = %s", (chat_id,))
        DB.commit()
        return True
    return False


async def fsub_on(chat_id, channel):
    cusr.execute("INSERT INTO fsub (fsub_on, channel) VALUES (%s, %s)", (chat_id, channel))
    DB.commit()


async def alpha(chat_id):
    cusr.execute("SELECT channel FROM fsub WHERE fsub_on = %s", (chat_id,))
    chat = cusr.fetchone()
    if chat:
        return chat[0]
    return False


@app.on_message(filters.command("fsub") & filters.group)
@user_admin
@bot_admin
@bot_can_ban
async def force_sub(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    args = message.text.split()
    user = await _.get_chat_member(chat_id, user_id)
    if not user.status == ChatMemberStatus.OWNER:
        return await message.reply_text("**You Need To Be Group Creator To Use This Command.**")
    if "OFF".lower() in args:
        await fsub_off(str(chat_id))
        return await message.reply_text("**Force Sub Disabled.**")
    elif len(args) < 2:
        return await message.reply_text("**Provide Me A Channel ID or Username To Activate Force Sub.**")
    ch = args[1]
    try:
        channel = await _.get_chat(ch)
    except:
        return await message.reply_text("**Invalid Channel.**")
    try:
        await _.get_chat_member(channel.id, BOT_ID)
    except BadRequest:
        return await message.reply_text("**Make Me Admin On That Channel.**")
    member = await _.get_chat_member(channel.id, BOT_ID)
    if member.status != ChatMemberStatus.ADMINISTRATOR:
        return await message.reply_text("**Make Me Admin On That Channel.**")

    await fsub_on(str(chat_id), str(channel.id))
    await message.reply_text(f"**Force Sub Enabled In @{channel.username}.**")


@app.on_message(group=69)
async def executor(_, message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    users = []
    ahem = _.get_chat_members(chat_id)
    async for mem in ahem:
        users.append(mem.user.id)
    if not message.from_user:
        return
    ADMINS = []
    async for m in _.get_chat_members(chat_id, filter=ChatMembersFilter.ADMINISTRATORS):
        ADMINS.append(m.user.id)
    if message.from_user.id in ADMINS:
        return
    if message.from_user.id in users:
        return
    ch = await alpha(str(chat_id))
    if not ch:
        return
    channel = await _.get_chat(int(ch))
    buttons = InlineKeyboardMarkup([[InlineKeyboardButton("Join", url=f"t.me/{channel.username}"),
                                     InlineKeyboardButton("Unmute", callback_data=f"fsubuser_{message.from_user.id}")]])
    msg = f"**Hey {message.from_user.mention}\nSubscribe To This Channel {channel.username} In Order To Unmute Yourself.**"
    await message.reply_text(msg, reply_markup=buttons)
    try:
        await _.restrict_chat_member(chat_id, message.from_user.id, ChatPermissions(can_send_messages=False))
    except Exception as e:
        await message.reply_text(e)


@app.on_callback_query(filters.regex(pattern=r"fsubuser_(.*)"))
async def ok(_, query: CallbackQuery):
    muted_user = int(query.data.split("_")[1])
    chat_id = query.message.chat.id
    ch = await alpha(str(chat_id))
    members = []
    async for member in _.get_chat_members(ch):
        members.append(member.user.id)
    user_id = query.from_user.id
    if user_id != muted_user:
        await _.answer_callback_query(query.id, text="It's Not For You.", show_alert=True)
        return

    if not muted_user in members:
        return await _.answer_callback_query(query.id, text="You Have To Join The Channel To Get Unmuted.", show_alert=True)

    try:
        await _.unban_chat_member(chat_id, muted_user)
    except Exception as er:
        print(er)
    await query.message.delete()
