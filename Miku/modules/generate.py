from Miku import app
from pyrogram import *
from pyrogram.types import *
import openai

key = "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"
text = ""

@app.on_message(filters.command("gen"))
async def generate(client, message):
    global text
    text = message.text.split("/gen")[1]
    button1 = InlineKeyboardButton("DALL-E", callback_data="button1")
    button2 = InlineKeyboardButton("Dark Sushi", callback_data="button2")
    keyboard = InlineKeyboardMarkup([[button1, button2]])
    await message.reply_text("**Select a model.**", reply_markup=keyboard)


@app.on_callback_query()
async def handle_callback(client, callback_query):
    callback_data = callback_query.data
    if callback_data == "button1":
        x = await callback_query.message.edit_text("**Creating Artificial Image...**")
        openai.api_key = key
        response = openai.Image.create(prompt=text, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        await x.delete()
        await callback_query.message.reply_photo(photo=image_url, caption=f"**Prompt:-**\n{text}")
