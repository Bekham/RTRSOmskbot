from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import edit_history_kb



async def station_history(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("istory_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                data_station = sqlite_db.sql_read_station(station)
                if data_station:
                    await call.message.answer(f"История заданий станции {item[1]}:")
                    for task in data_station:
                        user_create = sqlite_db.find_user(task[2])
                        user_update = sqlite_db.find_user(task[3])
                        if task[6]:
                            status = 'Активно'
                        else:
                            status = 'Завршено'
                        await call.message.answer(f"Задание №{task[0]}. \n"
                                                  f"Создано {(task[4]).split(' ')[0]} пользователем {user_create[0][5]} {user_create[0][6]}\n"
                                                  f"Обновлено {(task[5]).split(' ')[0]} пользователем {user_update[0][5]} {user_update[0][6]}\n"
                                                  f"Статус: {status}\n"
                                                  f"{task[1]}\n"
                                                  f"____________________________________")
                else:
                    await call.message.answer(f"История пуста")

    await call.answer()






def register_history_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(station_history, Text(startswith="history_"), state='*')


