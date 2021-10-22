from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import stations_kb
from create_bot import bot
from keyboards import client_kb
from data_base import sqlite_db
from keyboards import edit_history_kb


async def stations(message: types.Message):
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    if message.from_user.id == user_data[1]:
        await message.answer("Станции Омского Цеха:", reply_markup=stations_kb.get_keyboard())
        await message.delete()



async def callbacks_num(call: types.CallbackQuery):
    # await call.message.delete()
    # Парсим строку и извлекаем действие, например `st_incr` -> `incr`
    action = call.data.split("_")[1]
    data_stations = sqlite_db.sql_read_all_stations()
    for item in data_stations:
        if action == item[2]:
            await call.message.answer(f"Здесь будут задания станции {item[1]}",
                                      reply_markup=edit_history_kb.edit_history_client)
    # Не забываем отчитаться о получении колбэка
    await call.answer()
    await call.message.delete_reply_markup()

def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(stations, Text(equals="Станции"), state='*')


def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num, Text(startswith="st_"))


