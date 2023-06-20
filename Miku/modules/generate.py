import openai
from pyrogram import filters
from Miku import app

chat_id = None
key = "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"
c[chat_id] = {'time': True}

@app.on_message(filters.command("gen") & filters.group)
async def gen(client , msg):
	chat_id = msg.chat.id
	x = await msg.reply("**Creating Artificial Image....**")
	if c[chat_id]['time'] == False:
		return await x.edit("**One Process Is Running Try Later.**")        
    text = msg.text.split("/gen")[1]
    c[chat_id]['time'] = False
    openai.api_key = key    
    response = openai.Image.create(prompt=f"anime style {text}", n=1, size="1024x1024")
    image_url = response['data'][0]['url']
    await msg.edit(photo=image_url , caption=f"**Prompt:-**\n{text}")
    c.pop(chat_id)





