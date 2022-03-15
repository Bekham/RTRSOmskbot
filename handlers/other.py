from aiogram import types, Dispatcher
import json

from google.cloud import dialogflow
from aiogram.dispatcher.filters import Text
from create_bot import language_code, session_client, session, bot
from data_base import sqlite_db
# from dialogflow import types
# from google.cloud import dialogflow
import os
# import google.cloud.dialogflow
from google.api_core.exceptions import InvalidArgument


async def update_0_5(message: types.Message):
    users_data = sqlite_db.sql_read_all_user()
    print('update')
    for user in users_data:
        if user[1] != message.from_user.id and user[8]:
            message.text = f'Обновление до версии 0.5\n' \
                           f'Что нового:\n' \
                           f'1. Добавлена возможность добавления поездок в командировки как себя, так и коллег.\n' \
                           f'2. Добавлен раздел Профили (внизу клавиатуры, рядом с кнопкой Станции)\n' \
                           f'3. В профиле есть возможность просмотреть статистику создания/закрытия ' \
                           f'заданий и поездок,' \
                           f'а также просмотреть/удалить свои поездки\n' \
                           f'4. Через свой профиль можно просматривать профили и статистику коллег.' \
                           f'ВНИМАНИЕ!!! Для активации обновления необходимо ввести:\n /start \n '
            # await message.reply(message.text)
            message.chat.id = user[8]
            await bot.send_message(message.chat.id, message.text)

async def update_0_6(message: types.Message):
    users_data = sqlite_db.sql_read_all_user()
    print('update')
    for user in users_data:
        if user[1] != message.from_user.id and user[8]:
            message.text = f'Обновление до версии 0.6\n' \
                           f'Что нового:\n' \
                           f'1. Добавлена возможность добавления поездок в командировки как себя, так и коллег.\n' \
                           f'Есть возможность добавления сразу несколько станций в поездки на несколько дней.\n' \
                           f'При добавлении поездок учитывается наличие/отстутствие выходного дня в дни поездок.\n' \
                           f'2. Добавлен раздел Профили (внизу клавиатуры, рядом с кнопкой Станции)\n' \
                           f'3. В профиле есть возможность просмотреть статистику создания/закрытия ' \
                           f'заданий и поездок,' \
                           f'а также просмотреть/удалить свои поездки\n' \
                           f'4. Через свой профиль можно просматривать профили и статистику коллег.' \
                           f'ВНИМАНИЕ!!! Для активации обновления необходимо ввести:\n /start \n '
            # await message.reply(message.text)
            message.chat.id = user[8]
            await bot.send_message(message.chat.id, message.text)


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
    dp.register_message_handler(update_0_5, Text(equals="Обновление_0_5"), state='*')
    dp.register_message_handler(update_0_6, Text(equals="Обновление_0_6"), state='*')
    # dp.register_message_handler(menu_command, commands=['Станции'], state=None)
    dp.register_message_handler(echo_send)
