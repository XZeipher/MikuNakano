from pytube import YouTube
from pyrogram import filters , Client
import os
from Miku import app

@Client.on_message(filters.command("ytdl"))
async def download_youtube_video(client, message):
    video_url = message.text.split("/ytdl")[1]
    x = await message.reply_text("**Processing...**")
    try:
        yt = YouTube(video_url)
        video = yt.streams.get_highest_resolution()
        start_time = 10
        end_time = start_time + 5
        await x.edit(f"**Downloading:** {yt.title}")
        video.download(filename="temp.mp4")
        original_filename = video.default_filename
        video_file = "alpha.mp4"
        temp_file = "temp.mp4"
        
        if os.path.exists(temp_file):
            os.rename(temp_file, video_file)
            await x.delete()
            await message.reply_video(video_file, caption=yt.title)
            os.remove(temp_file)
            os.remove(video_file)
        else:
            await x.edit("**Error: File not found.**")
            os.remove(temp_file)
            os.remove(video_file)
    except Exception as e:
        print("Error:", str(e))
