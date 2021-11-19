from aiogram import types, Dispatcher
import json

from google.cloud import dialogflow

from create_bot import language_code, session_client, session, bot
from data_base import sqlite_db
# from dialogflow import types
# from google.cloud import dialogflow
import os
# import google.cloud.dialogflow
from google.api_core.exceptions import InvalidArgument



async def echo_send(message: types.Message):
    text_input = dialogflow.TextInput(  # Текст запроса
        text=message.text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)  # Ввод запроса
    response = session_client.detect_intent(  # Ответ бота
        session=session, query_input=query_input)
    if response.query_result.fulfillment_text:  # Если ответ имеется
        await bot.send_message(message.from_user.id,
                               response.query_result.fulfillment_text)  # Отправляем его пользователю
    else:  # В обратном случае
        await bot.send_message(message.from_user.id, "Я тебя не понимаю")  # Я тебя не понимаю
    # if response:
    #     await message.answer(text=response)
    # else:
    #     await message.answer('Я Вас не совсем понял!')

    # if message.text == 'Привет' or message.text == 'привет':
    #     await message.answer('Игорь пидр!')
    # else:
    #     await message.answer(message.text)
    # await message.reply(message.text)
    #     await bot.send_message(message.from_user.id, message.text)


def register_handler_other(dp: Dispatcher):
    # dp.register_message_handler(menu_command, commands=['Станции'], state=None)
    dp.register_message_handler(echo_send)
