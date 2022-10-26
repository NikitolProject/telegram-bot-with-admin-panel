import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from pyrogram import Client

from dotenv import load_dotenv

load_dotenv(".env")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=os.environ["API_TOKEN"])

storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

app = Client(
    name="test", 
    api_id=3856575, 
    api_hash="1d6df36bd42c437da9d0ce81dc0f3057",
    bot_token=os.environ["API_TOKEN"]
)
