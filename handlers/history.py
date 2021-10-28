from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import edit_history_kb, history_back_restore_kb


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
                    # total_count = len(data_station)
                    # num_list = 0
                    page_item_count = 3
                    text_list = []
                    text = ''
                    for task in data_station:
                        # num_list += 1
                        user_create = sqlite_db.find_user(task[2])
                        user_update = sqlite_db.find_user(task[3])
                        if task[6]:
                            status = 'Активно'
                        else:
                            status = 'Завершено'
                        text_list.append(f"Задание №{task[0]}. \n"
                                f"Создано {(task[4]).split(' ')[0]} пользователем {user_create[0][5]} {user_create[0][6]}\n"
                                f"Обновлено {(task[5]).split(' ')[0]} пользователем {user_update[0][5]} {user_update[0][6]}\n"
                                f"Статус: {status}\n"
                                f"{task[1]}\n"
                                f"____________________________________\n")
                        # text += f"Задание №{task[0]}. \n" \
                        #         f"Создано {(task[4]).split(' ')[0]} пользователем {user_create[0][5]} {user_create[0][6]}\n"\
                        #         f"Обновлено {(task[5]).split(' ')[0]} пользователем {user_update[0][5]} {user_update[0][6]}\n"\
                        #         f"Статус: {status}\n"\
                        #         f"{task[1]}\n"\
                        #         f"____________________________________\n"
                    page_range = f'{page_item_count}_0_{page_item_count}_{len(text_list)-page_item_count}'
                    for i in range(page_item_count, 0, -1):
                        text += text_list[-1*i]
                    await call.message.answer(text,
                        reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id, pages = page_range))
                    print(page_range)

                else:
                    await call.message.answer(f"История пуста",
                                          reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id))

    await call.answer()


async def station_history_next(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("_")[-1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                data_station = sqlite_db.sql_read_station(station)
                if data_station:
                    data_pages = call.data.split("_")
                    if int(data_pages[-2]) >= int(data_pages[-3]):
                        cur_page =  int(data_pages[-3])
                        next_page =  int(data_pages[-2]) - int(data_pages[-3])
                    else:
                        cur_page = int(data_pages[-2])
                        next_page = 0
                    last_page = int(data_pages[-3]) + int(data_pages[-4])
                    page_count = int(data_pages[-5])
                    page = int((last_page + cur_page) / page_count)
                    await call.message.answer(f"История заданий станции {item[1]} (стр.{page}):")
                    text_list = []
                    text = ''
                    for task in data_station:
                        # num_list += 1
                        user_create = sqlite_db.find_user(task[2])
                        user_update = sqlite_db.find_user(task[3])
                        if task[6]:
                            status = 'Активно'
                        else:
                            status = 'Завершено'
                        text_list.append(f"Задание №{task[0]}. \n"
                                f"Создано {(task[4]).split(' ')[0]} пользователем {user_create[0][5]} {user_create[0][6]}\n"
                                f"Обновлено {(task[5]).split(' ')[0]} пользователем {user_update[0][5]} {user_update[0][6]}\n"
                                f"Статус: {status}\n"
                                f"{task[1]}\n"
                                f"____________________________________\n")
                    page_range = f'{page_count}_{last_page}_{cur_page}_{next_page}'
                    for i in range(int(last_page)+int(cur_page), int(last_page), -1):
                        text += text_list[-1*i]
                    await call.message.answer(text,
                        reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id, pages = page_range))
                    print(page_range)

                else:
                    await call.message.answer(f"История пуста",
                                          reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id))

    await call.answer()

async def station_history_back(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("_")[-1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                data_station = sqlite_db.sql_read_station(station)
                if data_station:
                    data_pages = call.data.split("_")
                    page_count = int(data_pages[-5])
                    if int(data_pages[-3]) <= int(data_pages[-4]):
                        cur_page =  page_count
                        last_page = int(data_pages[-4]) - cur_page
                        next_page = int(data_pages[-2]) + int(data_pages[-3])
                    else:
                        cur_page = int(data_pages[-4])
                        next_page = int(data_pages[-2]) + int(data_pages[-3])
                        last_page = 0

                    page = int((last_page + cur_page) / page_count)
                    await call.message.answer(f"История заданий станции {item[1]} (стр.{page}):")
                    text_list = []
                    text = ''
                    for task in data_station:
                        # num_list += 1
                        user_create = sqlite_db.find_user(task[2])
                        user_update = sqlite_db.find_user(task[3])
                        if task[6]:
                            status = 'Активно'
                        else:
                            status = 'Завершено'
                        text_list.append(f"Задание №{task[0]}. \n"
                                f"Создано {(task[4]).split(' ')[0]} пользователем {user_create[0][5]} {user_create[0][6]}\n"
                                f"Обновлено {(task[5]).split(' ')[0]} пользователем {user_update[0][5]} {user_update[0][6]}\n"
                                f"Статус: {status}\n"
                                f"{task[1]}\n"
                                f"____________________________________\n")
                    page_range = f'{page_count}_{last_page}_{cur_page}_{next_page}'
                    for i in range(int(last_page)+int(cur_page), int(last_page), -1):
                        text += text_list[-1*i]
                    await call.message.answer(text,
                        reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id, pages = page_range))
                    print(page_range)

                else:
                    await call.message.answer(f"История пуста",
                                          reply_markup=history_back_restore_kb.get_back_restore(item[2], call.from_user.id))

    await call.answer()




def register_history_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(station_history, Text(startswith="history_"), state='*')
    dp.register_callback_query_handler(station_history_next, Text(startswith="next_history_"), state='*')
    dp.register_callback_query_handler(station_history_back, Text(startswith="back_history_"), state='*')

