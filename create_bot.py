from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
logging.basicConfig(level=logging.INFO)

with open('login.json', 'r') as f:
    login_data = json.load(f)
TOKEN = login_data['TOKEN']

storage = MemoryStorage

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

