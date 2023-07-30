from Miku import *
from Miku.__main__ import *
from pyrogram import *
import strings
import config



MIKU_IMG = (
      "https://telegra.ph/file/624831b44a6e36370ec70.jpg",
      "https://telegra.ph/file/b9c7fb4d2dc481104fe49.jpg",
      "https://telegra.ph/file/02fd7a43fbce78c21c3dd.jpg",
      "https://telegra.ph/file/2c662cf6276379eaf10db.jpg",
      "https://telegra.ph/file/7bce7f2e2aedc3f048737.jpg",
)

MIKU_N_IMG = (
      "https://telegra.ph/file/837c61d9c51236fea4100.jpg",
      "https://telegra.ph/file/ee34cf0d7e4782424b777.jpg",
      "https://telegra.ph/file/5410b02359a2cabc2776b.jpg",
      "https://telegra.ph/file/b1fc3b2af759999bf3b35.jpg",
      "https://telegra.ph/file/305b5b3c4527cd439b926.jpg"

)

PM_PHOTO = (
      "https://telegra.ph/file/3f06de01df5bc3c3cf343.jpg",
      "https://telegra.ph//file/88976abda0d0af9d4a517.jpg",
      "https://telegra.ph//file/b388f473ddfb9cc727bb1.jpg",
)

async def send_help(app,chat, text, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(paginate_modules(0, HELPABLE, "help"))    
    await app.send_photo(
        chat_id=chat,
        photo=random.choice(MIKU_IMG),
        caption=text,
        parse_mode=ParseMode.MARKDOWN,      
        reply_markup=keyboard,
    )
    return (text, keyboard)

@Client.on_message(filters.command("start"))
async def group_start(_, message):    
    chat_id = message.chat.id 
    args = message.text.split()
    if message.chat.type == ChatType.PRIVATE :
        await add_served_user(message.from_user.id)
        if len(args) >= 2:
            if args[1].lower() == "help":
                await send_help(_,chat_id,strings.HELP_STRINGS) 
            elif args[1].lower().startswith("ghelp_"):
                mod = args[1].lower().split("_", 1)[1]
#                 try:
                mod = mod.replace("_", " ")
#                 excpet :
#                     mod = mod
                await _.send_photo(
                    chat_id,
                    photo = random.choice(MIKU_IMG),
                    caption = f"{strings.HELP_STRINGS}\n{MODULES[mod]}",
                    reply_markup = InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="«", callback_data="help_back")]]
                    ),
                )
            elif args[1][1:].isdigit():
                await send_rules(message,int(args[1]), from_pm=True)

                
        else:
            mention = message.from_user.mention                       
            await app.send_photo(
           chat_id,    
           photo=random.choice(PM_PHOTO),
           caption=strings.PM_START_TEXT.format(BOT_NAME,mention,uptime,platform.python_version(),pyrover),
           reply_markup=InlineKeyboardMarkup(strings.START_BUTTONS)
           )
                        
            
    else:
        await message.reply_photo(
                random.choice(MIKU_IMG),
                caption="**Hii {}, I'm here to help since:** `{}`".format(message.from_user.mention,uptime),
                reply_markup=InlineKeyboardMarkup(strings.GRP_START)
            )
                   
             
@Client.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(_,query):    
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data) 
               
    try:
        if mod_match:
            module = mod_match.group(1)
            text = (
                "» **Available Commands For** **{}** :\n".format(
                    HELPABLE[module].__mod_name__
                )
                + HELPABLE[module].__help__
            )
            await query.message.edit_caption(
                text,
                parse_mode=ParseMode.MARKDOWN,                
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton(text="Back 🔙", callback_data="help_back")]]
                ),
            )

        elif prev_match:
            curr_page = int(prev_match.group(1))
            await query.message.edit_caption(
                strings.HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(paginate_modules(curr_page - 1, HELPABLE, "help")
             ),
          )
                                   
        elif next_match:
            next_page = int(next_match.group(1))
            await query.message.edit_caption(
                strings.HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(next_page + 1, HELPABLE, "help")
                ),
            )                   

        elif back_match:
           await query.message.edit_caption(
                strings.HELP_STRINGS,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(
                    paginate_modules(0, HELPABLE, "help")
                ),
            )            

        return await _.answer_callback_query(query.id)

    except BadRequest:
        pass

@Client.on_message(filters.command("help"))
async def get_help(_, message):
    chat_id = message.chat.id
    args = message.text.split(None,1)
    chat_type = message.chat.type
    if chat_type != ChatType.PRIVATE:
        if len(args) >= 2 and process.extractOne(args[1].lower(),MODULES.keys())[0] in MODULES.keys():
            module = process.extractOne(args[1].lower(),MODULES.keys())[0].replace(" ","_")
            await message.reply_photo(
                photo = random.choice(MIKU_IMG),
                caption= f"**Contact me in PM to get help of {module.capitalize().replace('_',' ')}**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton(
                                text="Help 🆘",
                                url=f"https://t.me/{BOT_USERNAME}?start=ghelp_{module}"
                            )
                        ]
                    ]
                ),
            )
            return
        await message.reply_photo(
            photo = random.choice(PM_PHOTO),
            caption="**Choose An Option For Help**",
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="Private 💻",
                            url="https://t.me/{}?start=help".format(
                                BOT_USERNAME
                            ),
                        )
                    ],
                    
                ],
            ),
        )
        return

    elif len(args) >= 2 and any(args[1].lower() == x for x in HELPABLE):
        module = args[1].lower()
        text = (
            "**Here is the available help for the *{}* module:\n**".format(
                HELPABLE[module].__mod_name__
            )
            + HELPABLE[module].__help__
        )
        await send_help(
            _,
            chat_id,
            HELP_STRINGS,
            InlineKeyboardMarkup(
                [[InlineKeyboardButton(text="«", callback_data="help_back")]]
            ),
        )

    else:
        await send_help(_,chat_id,strings.HELP_STRINGS)

                              
                     
@Client.on_message(filters.command("donate"))  
async def donate(_, message):
    if message.chat.type == ChatType.PRIVATE:
        if message.from_user.id == config.OWNER_ID:
            await message.reply_text("⊙﹏⊙") 
        else:
            await message.reply_text(f"**You Can Donate Me [Here]({config.DONATION_LINK})**")                                                
    else:
        if message.from_user.id == config.OWNER_ID:
            await message.reply_text("⊙﹏⊙") 
        else:
            await message.reply_text("**I've PMed You About Donating My Creator.**")
            try:
                await app.send_message(message.from_user.id,text=f"[Here Is The Donation Link]({config.DONATION_LINK})")
            except Unauthorized:                
                await message.reply_text("**Contact Me In PM To Get Donation Information First!**")                                                                                               


__help__ = """
**Helpable Mod**

**Commands**

♠ `/help`: get help of commands.

♠ `/donate` : donate money to my master.

"""

__mod_name__ = "Help"          
