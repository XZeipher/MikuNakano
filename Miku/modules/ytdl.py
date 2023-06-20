from pytube import YouTube
from pyrogram import filters
import os
from Miku import app

@app.on_message(filters.command("ytdl") & filters.private)
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
        new_filename = original_filename.replace("temp.mp4", "")
        video_file = "alpha.mp4"
        temp_file = f"{original_filename}"
        os.rename(temp_file, video_file)
        await x.delete()
        await message.reply_video(video_file, caption=yt.title)
    except Exception as e:
        print("Error:", str(e))
