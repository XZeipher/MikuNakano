import requests
import json
import openai
from pyrogram import filters
from Miku import app

key = "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"
c = {}

@app.on_message(filters.command("gen") & filters.group)
async def gen(client, msg):
    chat_id = msg.chat.id
    text = msg.text.split("/gen")[1]
    openai.api_key = key

    # Send inline buttons to the user
    buttons = [
        [dict(text='Dall-E', callback_data='dall_e')],
        [dict(text='Dark Sushi', callback_data='dark_sushi')]
    ]
    await msg.reply_text("Please select an option:", reply_markup=dict(inline_keyboard=buttons))

@app.on_callback_query()
async def handle_callback(client, callback_query):
    if callback_query.data == 'dall_e':
        await run_dall_e(client, callback_query)
    elif callback_query.data == 'dark_sushi':
        await run_dark_sushi(client, callback_query)

async def run_dall_e(client, callback_query):
    query = callback_query.message.text.split("/gen")[1]
    response = await execute_dall_e(query)
    await handle_image_response(client, callback_query.message, query, response)

async def run_dark_sushi(client, callback_query):
    query = callback_query.message.text.split("/gen")[1]
    response = await execute_dark_sushi(query)
    await handle_image_response(client, callback_query.message, query, response)

async def execute_dall_e(query):
    url = "https://stablediffusionapi.com/api/v4/dreambooth"
    payload = {
        "key": "zgisLerC5jxfHwJIedKECUTTBXTGFY9uXTD6dagWI2jYGHopfEfvMZx0GFFx",
        "model_id": "dall-e",
        "prompt": query,
        # Add other parameters as needed
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

async def execute_dark_sushi(query):
    url = "https://stablediffusionapi.com/api/v4/dreambooth"
    payload = {
        "key": "zgisLerC5jxfHwJIedKECUTTBXTGFY9uXTD6dagWI2jYGHopfEfvMZx0GFFx",
        "model_id": "dark-sushi-25d",
        "prompt": query,
        # Add other parameters as needed
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post(url, headers=headers, data=json.dumps(payload))
    return response.json()

async def handle_image_response(client, message, query, response):
    image_url = response['data'][0]['url']
    await client.delete_messages(message.chat.id, message.message_id)
    await client.send_photo(message.chat.id, photo=image_url, caption=f"**Prompt:-**\n{query}")

