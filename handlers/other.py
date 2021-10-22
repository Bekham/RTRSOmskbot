from aiogram import types, Dispatcher

from data_base import sqlite_db


# async def menu_command(message: types.Message):
#     await sqlite_db.sql_read(message)

async def echo_send(message: types.Message):
    if message.text == 'Привет' or message.text == 'привет':
        await message.answer('Игорь пидр!')
    else:
        await message.answer(message.text)
    # await message.reply(message.text)
    #     await bot.send_message(message.from_user.id, message.text)


def register_handler_other(dp: Dispatcher):
    # dp.register_message_handler(menu_command, commands=['Станции'], state=None)
    dp.register_message_handler(echo_send)
