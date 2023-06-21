from Miku import app
from pyrogram import *
from pyrogram.types import *
import openai
import random
import requests
import json

key = "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"
text = ""
API_KEY = [
    "mfDX5RWRfp3drRlJrhKnUESfAEcvBsanwvyTNC4tfg0ELbXrK10OZ3YI7cPG",
    "UphNOVzEDLSZvZR9VBMGsjLfPnQ3yh2qh0dGgLq6jbKYk1EVHUp3r4aX1cIo",
    "bGp6ZyGJAkVBisvIPRMUUM5AtCLTUen0W2Br1Thp5Uzl1d38sdMsd436Ns6Z",
    "E2KcVIEb2z5OZcJzTeZLaGIAByB0V0g0asROjC681tYsHZ6LkQFU6n1j5TO6",
    "nwlu0MD33EHSxsLWZxVN8CDVZd9zOzIdj97BBRrSNgndcLyYg3nSZixiDw4t",
    "LacoWFS1YgGNdWxmZsvoko7cqXc8T8aYCk6PN6oNQVVnxkDxcUYwHTs1XBAS",
    "8gN6LPbVyPprzc6iqEm6rGscpcgkpVC2MSHP1NqW3wc7dePulBx3QhSYQ48d",
    "PpwVYZSGIPS6GSyxWpGy0UJCBsSgEIN7WHevNzEL9yK0oG4V9GqOKWe1SFqP",
    "KGSD1PEtmmlxq386JC02oi05tadZIFqioCPydI58O9Op5TMrWufSnjpYh3Sn",
    "6GemRIXq87NuC3XW8owVqkzVPn10jsJIFwpLt6UtLnaOupLNjs5tQDkP0WRA",
    "qlBt8dp7qJjo6PBZaWfkUpdolVRTSqP7hF6JF4IFN3ahopdCwTY9H7u5oXwU",
    "PEGpyq2jYDHzTztjKW6cZG9IIVCe7vroYwWepnAtWgtbPguzaMX1xXJMaUL5",
    "zgisLerC5jxfHwJIedKECUTTBXTGFY9uXTD6dagWI2jYGHopfEfvMZx0GFFx",
    "M7M5ePQKzImLRGB3KdtyOJtAknsnOCm2mFCB75WMmUr7Djwb93B0FzfGinLa",
    "1hgz5P9hcuVO9CE46vhkMjFSMkEYdFisq0JHn1of5tzjNsaY8kobM2UHSgO5"
]


@app.on_message(filters.command("gen"))
async def generate(client, message):
    global text
    text = message.text.split("/gen")[1]
    button1 = InlineKeyboardButton("DALL-E", callback_data="button1")
    button2 = InlineKeyboardButton("Dark Sushi", callback_data="button2") 
    button3 = InlineKeyboardButton("Guofeng3", callback_data="button3") 
    button4 = InlineKeyboardButton("Meina Mix", callback_data="button4") 
    keyboard = InlineKeyboardMarkup([[button1, button2]] , [[ button3 , button4]])
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
    elif callback_data == "button2":
        x = await callback_query.message.edit_text("**Creating Artificial Image...**")
        url = "https://stablediffusionapi.com/api/v4/dreambooth"
        payload = json.dumps({
            "key": random.choice(API_KEY),
            "model_id": "dark-sushi-25d",
            "prompt": text,
            "negtive-prompt": "drawing, extra legs, extra body, extra hand, cartoon, weird face"          
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload).json()
        if "output" in response and response["output"]:
            output_url = response["output"][0]
        elif "future_links" in response and response["future_links"]:
            output_url = response["future_links"][0]
        else:
            output_url = None
        await x.delete()
        await callback_query.message.reply_photo(photo=output_url, caption=f"**Prompt:-**\n{text}")
    elif callback_data == "button3":
        x = await callback_query.message.edit_text("**Creating Artificial Image...**")
        url = "https://stablediffusionapi.com/api/v4/dreambooth"
        payload = json.dumps({
            "key": random.choice(API_KEY),
            "model_id": "guofeng3",
            "prompt": text,
            "negtive-prompt": "drawing, extra legs, extra body, extra hand, cartoon, weird face"          
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload).json()
        if "output" in response and response["output"]:
            output_url = response["output"][0]
        elif "future_links" in response and response["future_links"]:
            output_url = response["future_links"][0]
        else:
            output_url = None
        await x.delete()
        await callback_query.message.reply_photo(photo=output_url, caption=f"**Prompt:-**\n{text}")
    elif callback_data == "button4":
        x = await callback_query.message.edit_text("**Creating Artificial Image...**")
        url = "https://stablediffusionapi.com/api/v4/dreambooth"
        payload = json.dumps({
            "key": random.choice(API_KEY),
            "model_id": "meinamix",
            "prompt": text,
            "negtive-prompt": "drawing, extra legs, extra body, extra hand, cartoon, weird face"          
        })
        headers = {
          'Content-Type': 'application/json'
        }
        response = requests.post(url, headers=headers, data=payload).json()
        if "output" in response and response["output"]:
            output_url = response["output"][0]
        elif "future_links" in response and response["future_links"]:
            output_url = response["future_links"][0]
        else:
            output_url = None
        await x.delete()
        await callback_query.message.reply_photo(photo=output_url, caption=f"**Prompt:-**\n{text}")


