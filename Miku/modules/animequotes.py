import requests
import random
from Miku import app
from pyrogram import filters , Client
from pyrogram.types import InlineKeyboardButton, CallbackQuery, InlineKeyboardMarkup 
from .pyro.decorators import control_user,command

QUOTES_IMG = (
      "https://i.imgur.com/Iub4RYj.jpg", 
      "https://i.imgur.com/uvNMdIl.jpg", 
      "https://i.imgur.com/YOBOntg.jpg", 
      "https://i.imgur.com/fFpO2ZQ.jpg", 
      "https://i.imgur.com/f0xZceK.jpg", 
      "https://i.imgur.com/RlVcCip.jpg", 
      "https://i.imgur.com/CjpqLRF.jpg", 
      "https://i.imgur.com/8BHZDk6.jpg", 
      "https://i.imgur.com/8bHeMgy.jpg", 
      "https://i.imgur.com/5K3lMvr.jpg", 
      "https://i.imgur.com/NTzw4RN.jpg", 
      "https://i.imgur.com/wJxryAn.jpg", 
      "https://i.imgur.com/9L0DWzC.jpg", 
      "https://i.imgur.com/sBe8TTs.jpg", 
      "https://i.imgur.com/1Au8gdf.jpg", 
      "https://i.imgur.com/28hFQeU.jpg", 
      "https://i.imgur.com/Qvc03JY.jpg", 
      "https://i.imgur.com/gSX6Xlf.jpg", 
      "https://i.imgur.com/iP26Hwa.jpg", 
      "https://i.imgur.com/uSsJoX8.jpg", 
      "https://i.imgur.com/OvX3oHB.jpg", 
      "https://i.imgur.com/JMWuksm.jpg", 
      "https://i.imgur.com/lhM3fib.jpg", 
      "https://i.imgur.com/64IYKkw.jpg", 
      "https://i.imgur.com/nMbyA3J.jpg", 
      "https://i.imgur.com/7KFQhY3.jpg", 
      "https://i.imgur.com/mlKb7zt.jpg", 
      "https://i.imgur.com/JCQGJVw.jpg", 
      "https://i.imgur.com/hSFYDEz.jpg", 
      "https://i.imgur.com/PQRjAgl.jpg", 
      "https://i.imgur.com/ot9624U.jpg", 
      "https://i.imgur.com/iXmqN9y.jpg", 
      "https://i.imgur.com/RhNBeGr.jpg", 
      "https://i.imgur.com/tcMVNa8.jpg", 
      "https://i.imgur.com/LrVg810.jpg", 
      "https://i.imgur.com/TcWfQlz.jpg", 
      "https://i.imgur.com/muAUdvJ.jpg", 
      "https://i.imgur.com/AtC7ZRV.jpg", 
      "https://i.imgur.com/sCObQCQ.jpg", 
      "https://i.imgur.com/AJFDI1r.jpg", 
      "https://i.imgur.com/TCgmRrH.jpg", 
      "https://i.imgur.com/LMdmhJU.jpg", 
      "https://i.imgur.com/eyyax0N.jpg", 
      "https://i.imgur.com/YtYxV66.jpg", 
      "https://i.imgur.com/292w4ye.jpg", 
      "https://i.imgur.com/6Fm1vdw.jpg", 
      "https://i.imgur.com/2vnBOZd.jpg", 
      "https://i.imgur.com/j5hI9Eb.jpg", 
      "https://i.imgur.com/cAv7pJB.jpg", 
      "https://i.imgur.com/jvI7Vil.jpg", 
      "https://i.imgur.com/fANpjsg.jpg", 
      "https://i.imgur.com/5o1SJyo.jpg", 
      "https://i.imgur.com/dSVxmh8.jpg", 
      "https://i.imgur.com/02dXlAD.jpg", 
      "https://i.imgur.com/htvIoGY.jpg", 
      "https://i.imgur.com/hy6BXOj.jpg", 
      "https://i.imgur.com/OuwzNYu.jpg", 
      "https://i.imgur.com/L8vwvc2.jpg", 
      "https://i.imgur.com/3VMVF9y.jpg", 
      "https://i.imgur.com/yzjq2n2.jpg", 
      "https://i.imgur.com/0qK7TAN.jpg", 
      "https://i.imgur.com/zvcxSOX.jpg", 
      "https://i.imgur.com/FO7bApW.jpg", 
      "https://i.imgur.com/KK06gwg.jpg", 
      "https://i.imgur.com/6lG4tsO.jpg"
      
      )    

@Client.on_message(command(commands=("quote")))
@control_user()
async def quote(_, message):
    url = "https://animechan.vercel.app/api/random"
    r = requests.get(url)
    e = r.json()
    quote = e["quote"]
    character= e["character"]
    anime = e["anime"]           
    await message.reply_text(f"""
⚡ **Quote** :
❝ {quote} ❞

📌 **Character** : **{anime}** 
✨ **Anime** : **{character}**
""",
reply_markup=InlineKeyboardMarkup(
        [
        [
          InlineKeyboardButton (text="Change ⚡",callback_data="change_quote")
        ],
        ]))                                                

@Client.on_callback_query(filters.regex("change_quote"))
@control_user()
async def change_quote(_,CallbackQuery):
    query = CallbackQuery.message     
    url = "https://animechan.vercel.app/api/random"
    r = requests.get(url)
    e = r.json()
    quote = e["quote"]
    character= e["character"]
    anime = e["anime"] 
    await query.edit_text(f"""
⚡ **Quote** :
❝ {quote} ❞

📌 **Character** : **{anime}** 
✨ **Anime** : **{character}**
""",
reply_markup=InlineKeyboardMarkup(
        [
        [
          InlineKeyboardButton (text="Change ⚡",callback_data="change_quote")
        ],
        ]))    

@Client.on_message(command(commands=("animequotes")))
@control_user()
async def anime_quote(_,msg):
    await msg.reply_photo(random.choice(QUOTES_IMG),
    reply_markup=InlineKeyboardMarkup(
        [
        [
          InlineKeyboardButton (text="Change ⚡",callback_data="anime_quote")
        ],
        ]))  

@Client.on_callback_query(filters.regex("anime_quote"))
@control_user()
async def anime_quote(_,CallbackQuery):
    query = CallbackQuery.message         
    await query.reply_photo(random.choice(QUOTES_IMG),
    reply_markup=InlineKeyboardMarkup(
        [
        [
          InlineKeyboardButton (text="Change ⚡",callback_data="anime_quote")
        ],
        ]))   

__help__="""
**Get Amazing Anime Quotes**

**Commands**

♠ `/quote` : get random text quotes
♠ `/animequotes` : get random picture quotes

"""
__mod_name__ = "Quotes"
