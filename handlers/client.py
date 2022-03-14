from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import stations_kb
from data_base import sqlite_db
from keyboards import edit_history_kb


async def stations(message: types.Message):
    sqlite_db.sql_update_user_visit(message.from_user.id)
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    try:
        if message.from_user.id == user_data[1]:
            await message.answer("Станции Омского Цеха:", reply_markup=stations_kb.get_keyboard())
            # await message.delete()
    except TypeError:
        await message.answer("Введите /start для авторизации")


async def callbacks_num(call: types.CallbackQuery):
    # await call.message.delete()
    # Парсим строку и извлекаем действие, например `st_incr` -> `incr`
    action = call.data.split("_")[1]
    data_stations = sqlite_db.sql_read_all_stations()
    for item in data_stations:
        if action == item[2]:
            data_station = sqlite_db.sql_read_station(item[2])
            await call.message.answer(f"Задания по станции {item[1]}:")
            if data_station:
                active_count = 0
                for task in data_station:
                    if task[6]:
                        active_count += 1
                # num_list = 0
                if active_count != 0:
                    task_list = []
                    task_text = ''
                    for task in data_station:
                        if task[6]:
                            # num_list += 1
                            user_update = sqlite_db.find_user(task[3])
                            if user_update:
                                task_user = f'{user_update[0][5]} {user_update[0][6]}'
                            else:
                                task_user = ''
                            task_list.append(f"{task[0]}. Дата: {(task[5]).split(' ')[0]}. \n "
                                             f"Создал:  {task_user}\n "
                                             f"Описание: {task[1]}\n"
                                             f"____________________________________\n")
                            # if num_list != active_count:
                            #     await call.message.answer(f"{task[0]}. Дата: {(task[5]).split(' ')[0]}. \n "
                            #                               f"Создал:  {task_user}\n "
                            #                               f"{task[1]}")
                            # else:
                            #     await call.message.answer(f"{task[0]}. Дата: {(task[5]).split(' ')[0]}. \n "
                            #                               f"Создал:  {task_user}\n "
                            #                               f"{task[1]}",
                            #                               reply_markup=edit_history_kb.get_keyboard_station(item[2]))
                    for i in task_list:
                        # print(i)
                        task_text += i
                    await call.message.answer(task_text,
                                              reply_markup=edit_history_kb.get_keyboard_station(item[2]))
                else:
                    await call.message.answer(f"Задания по станции {item[1]} отсутствуют.",
                                              reply_markup=edit_history_kb.get_keyboard_station(item[2]))
            else:
                # await call.message.answer(f"Задания по станции {item[1]}:")
                await call.message.answer(f"Задания по станции {item[1]} отсутствуют.",
                                          reply_markup=edit_history_kb.get_keyboard_station(item[2]))
    # Не забываем отчитаться о получении колбэка
    await call.answer()
    # await call.message.delete_reply_markup()


def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(stations, Text(equals="Станции"), state='*')


def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num, Text(startswith="st_"))
