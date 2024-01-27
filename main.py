from pyrogram import Client, idle, filters, enums
import time
import re
from SafoneAPI import SafoneAPI
import os
import asyncio
from html_telegraph_poster.upload_images import upload_image
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto
from jikanpy import Jikan
import signal
from io import BytesIO
import sys
import random
import base64
import aiohttp
import requests
from html_telegraph_poster import TelegraphPoster
from dotenv import load_dotenv
import google.generativeai as genai
import PIL.Image

from stickers import stickers
api_id = 3845818
api_hash = "95937bcf6bc0938f263fc7ad96959c6d"
bot_token = "5787191452:AAGPcjesbDih65vqH5rUFbrxZ96yHemISi4"
app = Client("anime_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)
GOOGLE_API_KEY = "AIzaSyA5X_AHEvif0EyIP8_Kx4jCg7lVEsArctQ"
genai.configure(api_key=GOOGLE_API_KEY)
@app.on_message(filters.chat(-1001944303479))
async def handle_message(client, message):
    user = message.from_user
    userid = user.id
    topz = message.reply_to_message_id
    KAYO_ID=-1001944303479
    if topz == 20 and message.text.startswith("/"):
        pass
    elif topz == 20 and message.text:
        topic_id=topz
        sticker_id = random.choice(stickers)
        sticker = await app.send_sticker(
                chat_id=KAYO_ID,
                sticker=sticker_id,
                reply_to_message_id=topic_id
            )
        txt = await app.send_message(
            chat_id=KAYO_ID,
            text=f"Loading gemini-pro ...",
            reply_to_message_id=topic_id
        )
        model = genai.GenerativeModel('gemini-pro')
        await txt.edit("⚡ Thinking....")
        text = message.text
        await txt.edit("Shhh! 🤫, Thinking!\nPlease Wait..\nDon't send any other query in the meantime\n\n#BETA")
        response = model.generate_content(text)
        await txt.edit('Formating the Result...')
        await sticker.delete()
        await txt.delete()
        if response.text:
            print("response: ", response.text)
            await app.send_message(
                chat_id=KAYO_ID,
                text=response.text,
                reply_to_message_id=topic_id
            )
    elif topz == 20 and message.caption:
        topic_id=topz
        model_name = "gemini-pro-vision"
        sticker_id = random.choice(stickers)
        sticker = await app.send_sticker(
                chat_id=KAYO_ID,
                sticker=sticker_id,
                reply_to_message_id=topic_id
            )
        txt = await app.send_message(
            chat_id=KAYO_ID,
            text=f"Loading {model_name} ...",
            reply_to_message_id=topic_id
        )
        model = genai.GenerativeModel(model_name)
        await txt.edit("Downloading Image....")
        file_path = await message.download()
        caption = message.caption
        img = PIL.Image.open(file_path)
        await txt.edit("Shhh! 🤫, **Gemini Pro Vision** is at Work.\nPlease Wait..\n\n#BETA")
        response = (
            model.generate_content([caption, img])
            if caption
            else model.generate_content(img)
        )
        os.remove(file_path)
        await txt.edit('Formating the Result...')
        await sticker.delete()
        await txt.delete()
        if response.text:
            print("response: ", response.text)
            await app.send_message(
                chat_id=KAYO_ID,
                text=response.text,
                reply_to_message_id=topic_id
            )
        elif response.parts: # handle multiline resps
            for part in response.parts:
             print("part: ", part)
            await app.send_message(
                chat_id=KAYO_ID,
                text=part,
                reply_to_message_id=topic_id
            )
            time.sleep(2)
        else:
            await message.reply(
                "Couldn't figure out what's in the Image. Contact @pirate_user for help."
            )
app.start()
print("Powered by @animxt")
idle()
