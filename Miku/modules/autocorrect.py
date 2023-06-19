from Miku import app,arq
from pyrogram import filters 

@app.on_message(filters.command("autocorrect"))
async def _autocorrect(_, message):
    replied = message.reply_to_message
    if not replied:
        return await message.reply_text("**Reply To Text.**")
    text = replied.text or replied.caption
    if not text:
        return await message.reply_text("**Reply To Text.**")
    data = await arq.spellcheck(text)
    if not data.ok:
        return await message.reply_text("**Something Went Wrong.**")
    result = data.result
    await message.reply_text(result.corrected or "Empty")     
