from Miku import app
from pyrogram import *
from pyrogram.types import *
import openai
import random
import requests
import json
from Miku.modules.utils.misc import get_text, post_

key = "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"
text = ""

MODELSS = {"Dall-E":0,"Dark Sushi":"dark-sushi-25d","Guofeng3":"guofeng3","Meina Mix":"meinamix"}
MODELS_LIST = List(MODELSS)

@app.on_message(filters.command("gen") & filters.group)
async def generate(client, message):
    global text
    text = await get_text(message)
    button1 = InlineKeyboardButton("DALL-E", callback_data=f"gen.0.{message.from_user.id}")
    button2 = InlineKeyboardButton("Dark Sushi", callback_data=f"gen.1.{message.from_user.id}") 
    button3 = InlineKeyboardButton("Guofeng3", callback_data=f"gen.2.{message.from_user.id}") 
    button4 = InlineKeyboardButton("Meina Mix", callback_data=f"gen.3.{message.from_user.id}") 
    keyboard = InlineKeyboardMarkup([[button1, button2 , button3 , button4]])
    await message.reply_text("**Select a model.**", reply_markup=keyboard)


@app.on_callback_query(filters.regex(pattern=r"^gen.(.*)"))
async def generatebtns(client, query):
    global text
    data = query.data.split('.')
    auth_user = int(data[-1])
    model = int(data[1])
    if auth_user != query.from_user.id:
        await query.answer("Could you fuck off over there?")
        return
    x = await query.message.edit_text("**Creating Artificial Image...**")
    if model == 0:
        openai.api_key = key
        response = openai.Image.create(prompt=text, n=1, size="1024x1024")
        image_url = response['data'][0]['url']
        await x.delete()
        await query.message.reply_photo(photo=image_url, caption=f"**Prompt:-**\n{text}")
    elif model == 1 or model == 2 or model == 3:
        MODEL_ID = MODELSS[MODELS_LIST[model]]
        output_url = await post_(text,MODEL_ID)
        if output_url is None:
            await query.edit_message_text("Something went wrong!")
            return
        await x.delete()
        await query.message.reply_photo(photo=output_url, caption=f"**Prompt:-**\n{text}")

