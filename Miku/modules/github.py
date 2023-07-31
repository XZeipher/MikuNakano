import requests 
from Miku import app
from config import SUPPORT_CHAT
from pyrogram import filters,enums,Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup 


@Client.on_message(filters.command(["git","github"]))
async def _github(_, message):
    if len(message.command) < 2:
        return await message.reply_text("**Provide Me Your Git Username.**")

    username = message.text.split(None,1)[1]
    URL = f'https://api.github.com/users/{username}'
    result = requests.get(URL).json()
    try:
        m = await message.reply_text("**Searching....**")
        url = result['html_url']
        name = result['name']
        company = result['company']        
        created_at = result['created_at']
        avatar_url = result['avatar_url']
        blog = result['blog']
        location = result['location']
        repositories = result['public_repos']
        followers = result['followers']
        following = result['following']
        caption = f"""**Info Of {name}**

**Username :** `{username}`
**Profile Link :** [{name}]({url})
**Company :** `{company}`
**Created On :** `{created_at}`
**Repos :** `{repositories}`
**Location :** `{location}`
**Followers :** `{followers}`
**Followings :** `{following}`"""
        await message.reply_photo(avatar_url, caption=caption,reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text=f"{name}",
                            url=url,
                        ),
                    ],
                ],
            ), parse_mode=enums.ParseMode.MARKDOWN)
    except Exception as e:
        print(str(e))
        await message.reply_text(f"**Something Went Wrong.**")
        pass

__help__ = """
**You Can Get Information Of Any Github Profile**

**Commands**

♠ `/github` | `/git` : Fetch Info Of Any Github User.

"""

__mod_name__ = "Github"


