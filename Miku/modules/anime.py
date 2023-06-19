import bs4
import html
import jikanpy
import datetime
import textwrap
import requests
import json
from pyrogram import filters 
from Miku import app
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery , Message 
from pyrogram.enums import ParseMode 
from Miku.utils.anime_bot import rand_key, search_filler,parse_filler


url = 'https://graphql.anilist.co'
FILLERS = {}

async def shorten(description, info='anilist.co'):
    msg = ""
    if len(description) > 700:
        description = description[0:500] + '....'
        msg += f"\n**🗒 Description ›** `_{description}_`[Read More]({info})"
    else:
        msg += f"\n**🗒 Description ›**`_{description}_`"
    return msg

async def t(milliseconds: int) -> str:
    """Inputs time in milliseconds, to get beautified time,
    as string"""
    seconds, milliseconds = divmod(int(milliseconds), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = ((str(days) + " Days, ") if days else "") + \
        ((str(hours) + " Hours, ") if hours else "") + \
        ((str(minutes) + " Minutes, ") if minutes else "") + \
        ((str(seconds) + " Seconds, ") if seconds else "") + \
        ((str(milliseconds) + " ms, ") if milliseconds else "")
    return tmp[:-2]


airing_query = '''
    query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        siteUrl
        episodes
        title {
          romaji
          english
          native
        }
        nextAiringEpisode {
           airingAt
           timeUntilAiring
           episode
        }
      }
    }
    '''
manga_query = """
query ($id: Int,$search: String) {
      Media (id: $id, type: MANGA,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          type
          format
          status
          siteUrl
          averageScore
          genres
          bannerImage
      }
    }
"""

character_query = """
    query ($query: String) {
        Character (search: $query) {
               id
               name {
                     first
                     last
                     full
               }
               siteUrl
               image {
                        large
               }
               description
        }
    }
"""


anime_query = '''
   query ($id: Int,$search: String) {
      Media (id: $id, type: ANIME,search: $search) {
        id
        title {
          romaji
          english
          native
        }
        description (asHtml: false)
        startDate{
            year
          }
          episodes
          season
          type
          format
          status
          duration
          siteUrl
          studios{
              nodes{
                   name
              }
          }
          trailer{
               id
               site
               thumbnail
          }
          averageScore
          genres
          bannerImage
      }
    }
'''



@app.on_message(filters.command("anime"))
async def _anime(_, message):
    if len(message.command) < 2 :
        await message.reply_video('https://telegra.ph/file/d60afdfa00eab309abb47.mp4', '**Format : /anime < anime name >**')
        return     
    else:
        search = message.text.split(None,1)
        search = search[1]
    variables = {'search': search}
    json = requests.post(
        url, json={
            'query': anime_query,
            'variables': variables
        }).json()
    if 'errors' in json.keys():
        await message.reply_text('**Not Found.**')
        return
    
    if json:        
        json = json['data']['Media']
        msg = f"""
**📀 Title › {json['title']['romaji']}** ┌⁠(⁠・⁠。⁠・⁠)⁠┘⁠♪ **({json['title']['native']})**

**⌨️ Type ›** {json['format']}
**📊 Status ›** {json['status']}
**✨ Episodes ›** {json.get('episodes', 'N/A')}

**🕐 Duration ›** {json.get('duration', 'N/A')} ᴘᴇʀ ᴇᴘ.
**📆 Release Year ›** {json['startDate']['year']}
**🌟 Score ›**: {json['averageScore']}

**🎭 Genres ›**: `"""
        for x in json['genres']:
            msg += f"{x}, "
        msg = msg[:-2] + '`\n'
        msg += "**☯️ Studios ›**: `"
        for x in json['studios']['nodes']:
            msg += f"{x['name']}, "
        msg = msg[:-2] + '`\n'
        anime_name_w = f"{json['title']['romaji']}"
        info = json.get('siteUrl')
        trailer = json.get('trailer', None)
        anime_id = json['id']
        if trailer:
            trailer_id = trailer.get('id', None)
            site = trailer.get('site', None)
            if site == "youtube":
                trailer = 'https://youtu.be/' + trailer_id
        description = json.get('description', 'N/A').replace('<b>', '').replace(
            '</b>', '').replace('<br>', '')
        msg += await shorten(description, info)
        image = info.replace('anilist.co/anime/', 'img.anili.st/media/')

    if trailer:
        buttons = [[
                InlineKeyboardButton("♠ Trailer ♠", url=trailer),                
            ]]
        buttons += [[InlineKeyboardButton("♠ More Info ♠", url=info)]]
    else:
        buttons = [[InlineKeyboardButton("♠ More Info ♠", url=info)]]
        
         
    if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                await message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message.reply_text(
           msg,
           parse_mode=ParseMode.MARKDOWN,
           reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("manga"))
async def _manga(_, message):
    if len(message.command) < 2 :
        await message.reply_video("https://telegra.ph/file/bd2f8bb3a01bed38db873.mp4" , "**Format : /manga < manga name >**")
        return  
    search = message.text.split(None,1)
    search = search[1]
    variables = {'search': search}
    json = requests.post(
        url, json={
            'query': manga_query,
            'variables': variables
        }).json()
    msg = ''      
    if 'errors' in json.keys():
        await message.reply_text('Not Found.')
        return
    if json:
        json = json['data']['Media']
        title, title_native = json['title'].get('romaji',
                                                False), json['title'].get(
                                                    'native', False)
        start_date, status, score = json['startDate'].get(
            'year', False), json.get('status',
                                     False), json.get('averageScore', False) 
        if title:
            msg += f"**💫Title ›** {title}"
            if title_native:
                msg += f"(`{title_native}`)"
        if start_date:
            msg += f"\n\n**💤 Start Year ›** `{start_date}`"
        if status:
            msg += f"\n**📊 Status ›** `{status}`"
        if score:
            msg += f"\n**⚙️ Score ›** `{score}`"
        msg += '\n**♾️ Genres ›** '
        for x in json.get('genres', []):
            msg += f"{x}, "
        msg = msg[:-2]
        info = json['siteUrl']       
        buttons = [[InlineKeyboardButton("♠ More Info ♠", url=info)]]        
        image = json.get("bannerImage", False)
        msg += f"**\n\n• Description ›** _{json.get('description', None)}_"
        if image:
            try:
                await message.reply_photo(
                    photo=image,
                    caption=msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
            except:
                msg += f" [〽️]({image})"
                await message.reply_text(
                    msg,
                    parse_mode=ParseMode.MARKDOWN,
                    reply_markup=InlineKeyboardMarkup(buttons))
        else:
            await message.reply_text(
                msg,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=InlineKeyboardMarkup(buttons))

@app.on_message(filters.command("character"))
async def _character(_, message):
    if len(message.command) < 2 :
        await message.reply_video('https://telegra.ph/file/659343204f218f8ec2441.mp4','Format : /character < character name >')
        return   
    search = message.text.split(None,1)  
    search = search[1]
    variables = {'query': search}
    json = requests.post(
        url, json={
            'query': character_query,
            'variables': variables
        }).json()   
    if 'errors' in json.keys():
        await message.reply_text('Character not found')
        return
    if json:
        json = json['data']['Character']
        msg = f"**🪴 Character :** {json.get('name').get('full')}**(`{json.get('name').get('native')}`)** \n"
        description = f"{json['description']}"
        site_url = json.get('siteUrl')
        char_name = f"{json.get('name').get('full')}"
        msg += await shorten(description, site_url)
        image = json.get('image', None)
        if image:
            image = image.get('large')
            await message.reply_photo(
                photo=image,
                caption=msg.replace('<b>', '</b>'),               
                parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply_text(
                msg.replace('<b>', '</b>'), reply_markup=InlineKeyboardMarkup(buttons), parse_mode=ParseMode.MARKDOWN) 

@app.on_message(filters.command("airing"))
async def _airing(_, message):
    if len(message.command) < 2 :
        await message.reply_text('**Usage:** `/airing <anime name>`')
        return           
    search_str = message.text.split(None,1)
    variables = {'search': search_str[1]}
    response = requests.post(
        url, json={
            'query': airing_query,
            'variables': variables
        }).json()['data']['Media']
    info = response.get('siteUrl')
    image = info.replace('anilist.co/anime/', 'img.anili.st/media/')
    msg = f"**• Name ›** **{response['title']['romaji']}**(`{response['title']['native']}`)\n**⦾ ɪᴅ »** `{response['id']}`[⁠ ⁠]({image})"
    if response['nextAiringEpisode']:
        time = response['nextAiringEpisode']['timeUntilAiring'] * 1000
        time = await t(time)
        msg += f"\n**• Episode ›** `{response['nextAiringEpisode']['episode']}`\n**⦾ ᴀɪʀɪɴɢ ɪɴ »** `{time}`"
    else:
        msg += f"\n**• Episode ›**{response['episodes']}\n**⦾ sᴛᴀᴛᴜs »** `N/A`"
    await message.reply_text(msg, parse_mode=ParseMode.MARKDOWN)



__help__ = """
**Get Information about anime , characters, manga from Anilist.**

**Commands**

♠ `/anime <anime>`: Returns Information about the anime from Anilist.

♠ `/manga <manga>`: Returns Information about the manga from Anilist.

♠ `/character <character>`: Returns Information about the character from Anilist.

♠ `/airing <anime>`: Returns Information about airing from Anilist.

"""
__mod_name__ = "Anime"



    
