# Credits :- @TheStark

import datetime,pymongo
import config,random
from Miku import app,get_readable_time,BOT_ID
from config import SUPREME_USERS
from pyrogram import filters
from Miku.modules.mongo.games_db import *
import asyncio
import json
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Miku.utils.filter_groups import game_watcher1,game_watcher2


with open('trivia.json', 'r') as file:
    data = json.load(file)


async def get_user_won(emoji,value):
    if emoji in ['🎯','🎳']:
        if value >= 4:
            u_won = True
        else:
            u_won = False
    elif emoji in ['🏀','⚽'] :
        if value >= 3:
            u_won = True
        else:
            u_won = False
    return u_won


@app.on_message(filters.command("daily"))
async def _daily(client,message):
    user_id = message.from_user.id
    if not await is_player(user_id):
        await create_account(user_id,message.from_user.username)
    coins = await user_wallet(user_id)
    x,y = await can_collect_coins(user_id)
    if x is True:
        await gamesdb.update_one({'user_id' : user_id},{'$set' : {'coins' : coins + 10000}},upsert=True)
        await write_last_collection_time_today(user_id,datetime.datetime.now().timestamp())
        return await message.reply_text("**🎁 You Have Claimed 10,000 Dalcs!\n• Current Balance »** `{0:,}` **Dalcs**".format(coins+10000))    
    await message.reply_text("**You Can Claim Your Daily Bonus Again After** `{0}`".format(get_readable_time(y)))  
    
    
    
@app.on_message(filters.command("weekly"))
async def _weekly(client,message):
    user_id = message.from_user.id
    if not await is_player(user_id):
        await create_account(user_id,message.from_user.username)
    coins = await user_wallet(user_id)
    x,y = await can_collect(user_id)
    if x is True:
        await gamesdb.update_one({'user_id' : user_id},{'$set' : {'coins' : coins + 50000}},upsert=True)
        await write_last_collection_time_weekly(user_id,datetime.datetime.now().timestamp())
        return await message.reply_text("**🎁 You Have Claimed Your Weekly Bonus Of 50,000 Dalcs!\n• Total Dalcs »** `{0:,}` **Dalcs**".format(coins+50000))    
    await message.reply_text("**You Can Claim Your Weekly Bonus Again After** `{0}`".format(get_readable_time(y)))
                         
                             
                             
async def can_play(tame,tru):
  current_time = datetime.datetime.now()
  time_since_last_collection = current_time - datetime.datetime.fromtimestamp(tame)
  x = tru - time_since_last_collection.total_seconds()
  if str(x).startswith('-'):
      return 0
  return x
  

BET_DICT = {}
DART_DICT = {}
BOWL_DICT = {}
BASKET_DICT = {}
TRIVIA_DICT = {}


@app.on_message(filters.command("trivia"))
async def _trivia(client, message):
    chat_id = message.chat.id
    user = message.from_user
    if not await is_player(user.id):
        await create_account(user.id, message.from_user.username)
    if user.id not in TRIVIA_DICT.keys():
        TRIVIA_DICT[user.id] = None
    if TRIVIA_DICT[user.id]:
        x = await can_play(TRIVIA_DICT[user.id], 10 * 60)
        if int(x) != 0:
            return await message.reply(f'**You can play trivia again in like {get_readable_time(x)}.**')

    question = random.choice(data["questions"])
    id = data["questions"].index(question)
    options = question["options"]
    answer = question["answer"]
    buttons = [[InlineKeyboardButton(option, callback_data=f"tri:{option.lower()}:{id}:{user.id}")] for option in options]
    yos = await message.reply(f"**{question['question']}**\n\n__You Have 20 Seconds to answer.__", reply_markup=InlineKeyboardMarkup(buttons))
    TRIVIA_DICT[user.id] = datetime.datetime.now().timestamp()

    await asyncio.sleep(20)
    try:
        await yos.edit("**⌛ Time Up**")
    except:
        pass


@app.on_callback_query(filters.regex("^tri:"))
async def trivia_callback(client, query):
    chosen_option, id, user_id = query.data.split(":")[1:]
    user_id = int(user_id)
    answer = data["questions"][int(id)]["answer"].lower()
    await query.message.delete()
    if query.from_user.id != user_id:
        return await query.answer("This is not for you", show_alert=True)

    if chosen_option != answer:
        return await client.send_message(query.message.chat.id,f"**🔴 Wrong answer! The correct answer was {answer.title()}**")

    coins = await user_wallet(user_id)
    new_wallet = coins + 10000
    await gamesdb.update_one({'user_id': user_id}, {'$set': {'coins': new_wallet}})

    message_text = f"**🟢 Wow! The answer {chosen_option.title()} was right. You got 10,000 dalcs.\nTotal balance:** `{new_wallet:,}` **dalcs**"
    return await client.send_message(query.message.chat.id,message_text)


    
@app.on_message(filters.command("bet"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)
  if user.id not in BET_DICT.keys():
      BET_DICT[user.id] = None     
  if BET_DICT[user.id]:
      x= await can_play(BET_DICT[user.id],12)
      print(x)
      if int(x) != 0:
        return await message.reply(f'**You Can Bet Again After** `{get_readable_time(x)}`.')     
  possible = ['h','heads','tails','t','head','tail']
  if len(message.command) < 3:
      return await message.reply_text("**• Usage :** `/bet [amount] [heads/tails]`")
  to_bet = message.command[1]
  cmd = message.command[2].lower()
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_text("**Provide Valid Amount.**")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_text("**You Can't Bet 0 Dalcs**") 
  elif to_bet > coins:
      return await message.reply_text("**You Don't have that Much Dalcs Here Is your Balance »** `{0:,}` **Dalcs**".format(coins)) 
  rnd = random.choice(['heads','tails'])
  if cmd not in possible:
      return await message.reply_text("**You Should Try Heads Or Tails Either.**")
  if cmd in ['h','head','heads']:
      if rnd == 'heads':
          user_won = True         
      else:
          user_won = False
  if cmd in ['t','tail','tails']:
      if rnd == 'tails':
          user_won = True
      else:
          user_won = False
  BET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not user_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply_text("**🛑 The Coin Landed On** `{0}`!\n**• You Lost** `{1:,}` **Dalcs\n• Total Balance :** `{2:,}` **Dalcs**".format(rnd,to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      return await message.reply_text("**✅ The Coin Landed On** `{0}`!\n**You Won** `{1:,}` **Dalcs\nTotal Balance** : `{2:,}` **Dalcs**".format(rnd,to_bet,new_wallet)) 
     

@app.on_message(filters.command("dart"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)
  if user.id not in DART_DICT.keys():
      DART_DICT[user.id] = None     
  if DART_DICT[user.id]:
      x= await can_play(DART_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'**You Can Play Dart Again After** `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_text("**Give Amount For Playing Dart.**")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_text("**Provide A Valid Amount.**")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_text("**You Can't Bet 0 Amount.**") 
  elif to_bet > coins:
      return await message.reply_text("**You Don't Have That Much Dalcs Here Is Your Balance »** `{0:,}` **Dalcs**".format(coins))
  m = await client.send_dice(chat_id,'🎯')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  DART_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**🛑 Sad But You Lost** `{0:,}` **Dalcs\n• Current Balance »** `{1:,}` **Dalcs**".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**✅ Wow You Won** `{0:,}` **Dalcs\n• Current Balance »** `{1:,}`**Dalcs**".format(to_bet,new_wallet))
     
      
@app.on_message(filters.command("bowl"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username) 
  if user.id not in BOWL_DICT.keys():
      BOWL_DICT[user.id] = None     
  if BOWL_DICT[user.id]:
      x= await can_play(BOWL_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'**You Can Play Bowl Again After** `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_text("**Give A Amount To Play Bowl.**")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_text("**Provide A Valid Amount.**")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_text("**You Can't Bet 0 Amount.**") 
  elif to_bet > coins:
      return await message.reply_text("**You Don't Have That Much Dalcs Here Is Your Balance »** `{0:,}` **Dalcs**".format(coins))
  m = await client.send_dice(chat_id,'🎳')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BOWL_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**🛑 Sad But You Lost** `{0:,}` **Dalcs\n• Current Balance »** `{1:,}` **Dalcs**".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**✅ Wow You Won** `{0:,}` **Dalcs\n• Current Balance** `{1:,}` **Dalcs**".format(to_bet,new_wallet))
  

@app.on_message(filters.command("basket"))
async def _bet(client,message):
  chat_id = message.chat.id
  user = message.from_user
  if not await is_player(user.id):
     await create_account(user.id,message.from_user.username)  
  if user.id not in BASKET_DICT.keys():
      BASKET_DICT[user.id] = None     
  if BASKET_DICT[user.id]:
      x= await can_play(BASKET_DICT[user.id],20)
      if int(x) != 0:
        return await message.reply(f'**You Can Play Basket Again After** `{get_readable_time(x)}`.')
  if len(message.command) < 2:
      return await message.reply_text("**Give Me A Amount To Play Basket.**")
  to_bet = message.command[1]
  coins = await user_wallet(user.id)
  if to_bet == '*':
      to_bet = coins
  elif not to_bet.isdigit():
       return await message.reply_text("**Provide A Valid Amount.**")
  to_bet = int(to_bet)
  if to_bet == 0:
      return await message.reply_text("**You Can't Bet 0 Amount.**") 
  elif to_bet > coins:
      return await message.reply_text(_["minigames4"].format(coins))
  m = await client.send_dice(chat_id,'🏀')
  msg = await message.reply('....')
  u_won = await get_user_won(m.dice.emoji,m.dice.value)
  BASKET_DICT[user.id] = datetime.datetime.now().timestamp()
  if not u_won:
      new_wallet = coins - to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**You Don't Have That Much Dalcs** `{0:,}` **Dalcs**".format(to_bet,new_wallet))
  else:
      new_wallet = coins + to_bet
      await gamesdb.update_one({'user_id' : user.id}, {'$set' : {'coins' : new_wallet}})
      await asyncio.sleep(5)
      return await msg.edit("**✅ Wow You Won** `{0:,}` **Dalcs\n• Current Balance »** `{1:,}` **Dalcs**".format(to_bet,new_wallet))

                                                                                             

@app.on_message(filters.command("pay") & filters.group)
async def _pay(client,message):
    if not message.reply_to_message:
        return await message.reply_text("**Reply To An User.**")
    to_user =  message.reply_to_message.from_user
    from_user = message.from_user
    if to_user.id == from_user.id:
        if message.from_user.id not in SUPREME_USERS:
            return
    if not await is_player(to_user.id):
        await create_account(to_user.id,to_user.username)
    if not await is_player(from_user.id):
        await create_account(from_user.id,from_user.username)
    if len(message.command) < 2:
        return await message.reply_text("**• Usage:** `/pay 100`")
    amount = message.command[1]
    to_pay =  message.command[1].lower()
    tcoins = await user_wallet(to_user.id)
    fcoins = await user_wallet(from_user.id)
    if amount == '*':
        if message.from_user.id not in SUPREME_USERS:
            amount = fcoins
    elif not amount.isdigit():
       return await message.reply_text("**Give Me A Valid Amount.**")
    amount = int(amount)
    if amount == 0:
        return await message.reply_text("**You Can't Bet 0 Amount.**") 
    elif amount > fcoins:
        if message.from_user.id not in SUPREME_USERS:
            return await message.reply_text("**You Don't Have That Much Dalcs Here Is Your Balance »** `{0:,}` **Dalcs**".format(fcoins))
    if message.from_user.id not in SUPREME_USERS:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
        await gamesdb.update_one({'user_id' : from_user.id},{'$set' : {'coins' : fcoins - amount }})
    else:
        await gamesdb.update_one({'user_id' : to_user.id},{'$set' : {'coins' : tcoins + amount }})
    await message.reply_text("**Success {0} PAID {1:,} Dalcs To {2}.**".format(from_user.mention,amount,to_user.mention))


@app.on_message(filters.command(["top","leaderboard"]))
async def _top(client,message): 
    x = gamesdb.find().sort("coins", pymongo.DESCENDING)
    msg = "**📈 GLOBAL LEADERBOARD | 🌍**\n\n"
    counter = 1
    for i in await x.to_list(length=None):
        if counter == 11:
            break
        if i["coins"] == 0:
            pass
        else:
            user_name = i["username"]
            link = f"[{user_name}](https://t.me/{user_name})"
            if not user_name:
                user_name = i["user_id"]
                try:
                    link = (await app.get_users(user_name)).mention
                except Exception as e:
                    print(e)
                    link = user_name
            
            coins = i["coins"]
            if counter == 1:
               msg += f"{counter:02d}.**👑 {link}** ⪧ `{coins:,}`\n"
                
            else:
                msg += f"{counter:02d}.**👤 {link}** ⪧ `{coins:,}`\n"
            counter += 1
    await message.reply(msg,disable_web_page_preview=True)
    
@app.on_message(filters.command(["bal","balance","dalcs","bounty"]))
async def _bal(client,message):
    user = message.from_user
    if not await is_player(user.id):
        await create_account(user.id,message.from_user.username)
    coins = await user_wallet(user.id)
    await message.reply("**♠ {0}'s Bounty ♠**\n≪━─━─━─━─◈─━─━─━─━≫\n**Đ »** `{1:,}` \n**≪━─━─━─━─◈─━─━─━─━≫".format(user.mention,coins))

    
    
@app.on_message(filters.command("setdalcs"))
async def _bal(client,message):
    user = message.from_user
    if user.id not in SUPREME_USERS:
        return 
    if not message.reply_to_message:
        return await message.reply_text("**Reply To An User.**")
    if not message.reply_to_message.from_user:
        return await message.reply_text("**Reply To An User.**")
    from_user = message.reply_to_message.from_user
    if not await is_player(from_user.id):
        await create_account(from_user.id,from_user.username) 
    if len(message.command) < 2:
        return await message.reply("**Give Me Value To Set Dalcs.**")
    dalcs = message.command[1]
    if not dalcs.isdigit():
        return await message.reply("**The Provided Value is not a Integer.**")
    dalcs = abs(int(dalcs))
    await gamesdb.update_one({'user_id' : from_user.id},{'$set' : {'coins' : dalcs }})
    return await message.reply_text(f"**Success!\nSet the Dalcs of user {from_user.mention} to {dalcs}**")
    