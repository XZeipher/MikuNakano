import openai
from pyrogram import filters
from Miku import app

key = "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"


@app.on_message(filters.command("gen") & filters.group)
async def gen(client, msg):
    chat_id = msg.chat.id
    x = await msg.reply_text("**Creating Artificial Image....**")
    text = msg.text.split("/gen")[1]
    openai.api_key = key
    response = openai.Image.create(prompt=text, n=1, size="720x720")
    image_url = response['data'][0]['url']
    await x.delete()
    await msg.reply_photo(photo=image_url, caption=f"**Prompt:-**\n{text}")
