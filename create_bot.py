from aiogram import Bot
from aiogram.dispatcher import Dispatcher
import json
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import logging
import os

from google.cloud import dialogflow

logging.basicConfig(level=logging.INFO)

with open('login.json', 'r') as f:
    login_data = json.load(f)
TOKEN = login_data['TOKEN']

storage = MemoryStorage
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="service-account-file.json"

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

session_client = dialogflow.SessionsClient() #Сессия клиента
project_id = 'small-talk-lmsc' #Айди проекта берём с json файла
session_id = 'sessions' #Указываем любое значение, в моём случае "sessions"
language_code = 'ru' #Язык русский
session = session_client.session_path(project_id, session_id) #Объявляем сессию по айди проекта и айди сессии