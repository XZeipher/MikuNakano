import requests 
import os
import asyncio
from uuid import uuid4
from bs4 import BeautifulSoup
from pyrogram.types import Message , CallbackQuery 
from pyrogram import Client
from Miku import app
from config import SUDO_USERS as DRAGONS,DEV_USERS
from typing import Tuple,Optional

DOWN_PATH = "./Miku/resources/"
LOG_CHANNEL = -1001813613591


def rand_key():
    return str(uuid4())[:8]

def search_filler(query):
    html = requests.get("https://www.animefillerlist.com/shows").text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.findAll("div", attrs={"class": "Group"})
    index = {}
    for i in div:
        li = i.findAll("li")
        for jk in li:
            yum = jk.a["href"].split("/")[-1]
            cum = jk.text
            index[cum] = yum
    ret = {}
    keys = list(index.keys())
    for i in range(len(keys)):
        if query.lower() in keys[i].lower():
            ret[keys[i]] = index[keys[i]]
    return ret


def parse_filler(filler_id):
    url = "https://www.animefillerlist.com/shows/" + filler_id
    html = requests.get(url).text
    soup = BeautifulSoup(html, "html.parser")
    div = soup.find("div", attrs={"id": "Condensed"})
    all_ep = div.find_all("span", attrs={"class": "Episodes"})
    if len(all_ep) == 1:
        ttl_ep = all_ep[0].findAll("a")
        total_ep = []
        mix_ep = None
        filler_ep = None
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": filler_ep,
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 2:
        ttl_ep = all_ep[0].findAll("a")
        fl_ep = all_ep[1].findAll("a")
        total_ep = []
        mix_ep = None
        ac_ep = None
        filler_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": mix_ep,
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 3:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = None
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ac_ep
        }
        return dict_
    if len(all_ep) == 4:
        ttl_ep = all_ep[0].findAll("a")
        mxl_ep = all_ep[1].findAll("a")
        fl_ep = all_ep[2].findAll("a")
        al_ep = all_ep[3].findAll("a")
        total_ep = []
        mix_ep = []
        filler_ep = []
        ac_ep = []
        for tol in ttl_ep:
            total_ep.append(tol.text)
        for fol in fl_ep:
            filler_ep.append(fol.text)
        for mol in mxl_ep:
            mix_ep.append(mol.text)
        for aol in al_ep:
            ac_ep.append(aol.text)
        dict_ = {
            "filler_id": filler_id,
            "total_ep": ", ".join(total_ep),
            "mixed_ep": ", ".join(mix_ep),
            "filler_ep": ", ".join(filler_ep),
            "ac_ep": ", ".join(ac_ep),
        }
        return dict_

async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )

async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """ take a screenshot """
    print(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    thumb_image_path = path or os.path.join(
        DOWN_PATH, f"{basename(video_file)}.jpg"
    )
    command = (
        f"ffmpeg -ss {duration} "
        +f'-i "{video_file}" -vframes 1 "{thumb_image_path}"'
    )
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None

async def media_to_image(
    client: Client, message: Message, msg: Message, replied: Message
):
    if not (
        replied.photo
        or replied.sticker
        or replied.animation
        or replied.video
    ):
        await msg.edit("media type Is Invalid !")
        
    media = (
        replied.photo 
        or replied.sticker 
        or replied.animation 
        or replied.video
    )
    if not os.path.isdir(DOWN_PATH):
        os.makedirs(DOWN_PATH)
    dls = await client.download_media(
        media,
        file_name=DOWN_PATH + rand_key(),
    )
    dls_loc = os.path.join(DOWN_PATH, os.path.basename(dls))
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        png_file = os.path.join(DOWN_PATH, f"{rand_key()}.png")
        cmd = (
            f"lottie_convert.py --frame 0 -if lottie "
            +f"-of png {dls_loc} {png_file}"
        )
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await msg.edit_text(
                "This sticker is Gey, Task Failed Successfully ≧ω≦"
            )
            await asyncio.sleep(5)
            await msg.delete()
            raise Exception(stdout + stderr)
        dls_loc = png_file
    elif replied.sticker and replied.sticker.file_name.endswith(".webp"):
        stkr_file = os.path.join(DOWN_PATH, f"{rand_key()}.png")
        os.rename(dls_loc, stkr_file)
        if not os.path.lexists(stkr_file):
            await msg.edit_text("```Sticker not found...```")
            await asyncio.sleep(5)
            await msg.delete()
            return
        dls_loc = stkr_file
    elif replied.animation or replied.video:
        await msg.edit_text("`Converting Media To Image ...`")
        jpg_file = os.path.join(DOWN_PATH, f"{rand_key()}.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await msg.edit_text(
                "This Gif is Gey (｡ì _ í｡), Task Failed Successfully !"
            )
            await asyncio.sleep(5)
            await msg.delete()
            return
        dls_loc = jpg_file
    return dls_loc


async def clog(
    name: str,
    text: str,
    tag: str,
    msg: Message = None,
    cq: CallbackQuery = None,
    replied: Message = None,
    file: str = None,
    send_as_file: str = None
):
    log = f"#{name.upper()}  #{tag.upper()}\n\n{text}"
    data = ""
    if msg:
        data += str(msg)
        data += "\n\n\n\n"
    if cq:
        data += str(cq)
        data += "\n\n\n\n"
    await app.send_message(chat_id=LOG_CHANNEL, text=log)
    if msg or cq:
        with open("query_data.txt", "x") as output:
            output.write(data)
        await app.send_document(LOG_CHANNEL, "query_data.txt")
        os.remove("query_data.txt")
    if replied:
        media = (
            replied.photo 
            or replied.sticker 
            or replied.animation 
            or replied.video
        )
        media_path = await app.download_media(media)
        await app.send_document(LOG_CHANNEL, media_path)
    if file:
        await app.send_document(LOG_CHANNEL, file)
    if send_as_file:
        with open("dataInQuestion.txt", "x") as text_file:
            text_file.write()
        await app.send_document(LOG_CHANNEL, "dataInQuestion.txt")
        os.remove("dataInQuestion.txt")


