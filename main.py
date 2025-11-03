# Don't Remove Credit Tg - @VJ_Botz
# Subscribe YouTube Channel: https://youtube.com/@Tech_VJ

import os
import re
import sys
import json
import time
import asyncio
import requests
from aiohttp import ClientSession
from subprocess import getstatusoutput

import core as helper
from utils import progress_bar
from vars import API_ID, API_HASH, BOT_TOKEN

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.errors import FloodWait


# ✅ Bot Client (NO phone login, NO input)
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)


# ✅ START
@bot.on_message(filters.command(["start"]))
async def start(bot: Client, m: Message):
    await m.reply_text(
        f"<b>Hello {m.from_user.mention} 👋\n\n"
        "I download video links from your TXT file and upload them here.\n\n"
        "Use /upload to begin.\n"
        "Use /stop to cancel tasks.</b>"
    )


# ✅ STOP
@bot.on_message(filters.command("stop"))
async def restart_handler(_, m):
    await m.reply_text("**Stopped ✅**", True)
    os.execl(sys.executable, sys.executable, *sys.argv)



# ✅ UPLOAD FUNCTION (All inputs taken INSIDE Telegram, NOT CONSOLE)
@bot.on_message(filters.command(["upload"]))
async def upload(bot: Client, m: Message):

    # STEP 1 – TXT FILE
    editable = await m.reply("📄 **Send TXT file**")
    txt_msg = await bot.listen(m.chat.id)

    if not txt_msg.document:
        return await m.reply("❌ Please send a valid .txt file!")

    file_path = await txt_msg.download()
    await txt_msg.delete()

    try:
        with open(file_path, "r") as f:
            lines = f.read().splitlines()
        os.remove(file_path)
    except:
        return await m.reply("❌ Invalid TXT File!")

    await editable.edit(f"✅ **Total Links:** {len(lines)}\n\nSend starting number:")
    msg1 = await bot.listen(m.chat.id)
    start_from = int(msg1.text)
    await msg1.delete()

    # STEP 2 – Batch Name
    await editable.edit("✅ Send **Batch Name**")
    msg2 = await bot.listen(m.chat.id)
    batch_name = msg2.text
    await msg2.delete()

    # STEP 3 – Resolution
    await editable.edit("✅ Send **Resolution** (144/240/360/480/720/1080)")
    msg3 = await bot.listen(m.chat.id)
    quality = msg3.text
    await msg3.delete()

    # STEP 4 – Caption
    await editable.edit("✅ Send **Caption**")
    msg4 = await bot.listen(m.chat.id)
    caption = msg4.text
    await msg4.delete()

    # STEP 5 – Thumbnail
    await editable.edit("✅ Send thumbnail URL or 'no'")
    msg5 = await bot.listen(m.chat.id)
    thumb = msg5.text
    await msg5.delete()

    if thumb.startswith("http"):
        getstatusoutput(f"wget '{thumb}' -O thumb.jpg")
        thumb = "thumb.jpg"
    else:
        thumb = None

    await editable.edit("⏳ **Processing... Please wait**")

    # ✅ START DOWNLOADING LOOP
    count = start_from

    for index in range(start_from - 1, len(lines)):

        try:
            url = lines[index]

            # ✅ Clean filename
            video_name = f"{str(count).zfill(3)} {batch_name}".strip()

            # ✅ YT-DLP command
            if "youtu" in url:
                cmd = f'yt-dlp -f "bestvideo[height<={quality}]+bestaudio/best" "{url}" -o "{video_name}.mp4"'
            else:
                cmd = f'yt-dlp -f "best" "{url}" -o "{video_name}.mp4"'

            # ✅ Run download
            os.system(cmd)

            # ✅ Send to Telegram
            await bot.send_video(
                chat_id=m.chat.id,
                video=f"{video_name}.mp4",
                caption=caption,
                thumb=thumb
            )

            os.remove(f"{video_name}.mp4")
            count += 1
            time.sleep(1)

        except FloodWait as e:
            await asyncio.sleep(e.x)
            continue

        except Exception as e:
            await m.reply(f"❌ Error: {str(e)}\nURL: `{url}`")
            continue

    await bot.send_message(m.chat.id, "**✅ DONE BOSS 😎**")



# ✅ BOT START
bot.run()
