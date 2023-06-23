import binascii
import random
import string
import psycopg2
from Miku import app
from pyrogram import filters

DB = psycopg2.connect(
    host='rosie.db.elephantsql.com',
    port='5432',
    user='ucnbgdmc',
    password='CoCBP3Z3Ka_vg1KCEax66ea5Tbfaunac',
    database='ucnbgdmc'
)
cusr = DB.cursor()
cusr.execute("""
    CREATE TABLE IF NOT EXISTS tokens (
        id SERIAL PRIMARY KEY,
        user_id VARCHAR(255) NOT NULL,
        key TEXT NOT NULL
    )
""")
DB.commit()

@app.on_message(filters.command("token") & filters.private)
async def privates(client , message):
	await message.reply_text("**You Can't Use This Command At Private\n Use This Command In @MikuNakanoXSupport**")

@app.on_message(filters.command("token") & filters.group)
def generate_token(client , message):
	user_id = str(message.from_user.id)
    cusr.execute("SELECT key FROM tokens WHERE user_id = %s", (user_id,))
    existing_token = cusr.fetchone()
    if existing_token:
        token = existing_token[0]
        await message.reply_text(f"**You have already generated a token. Here is your token:** `{token}`")
    token_bytes = random.randbytes(5)
    token_hex = binascii.hexlify(token_bytes).decode()
    token = f"Miku-Alpha_{token_hex}"
    cusr.execute("INSERT INTO tokens (user_id, key) VALUES (%s, %s)", (user_id, token))
    DB.commit()
    await message.reply_text(f"**Here is your token :-**\n`{token}`")
