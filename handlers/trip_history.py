from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import edit_history_kb, history_back_restore_kb, history_trip_back_restore_kb


async def trip_history(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)  # Поиск пользователя в базе
    if call.from_user.id == user_data[1]:  # Если юзер в базе, то ищем историю поездок
        kb_data = call.data.split("_")
        if kb_data[2] == 'curr':
            user_id_trips = int(kb_data[-1])
        else:
            user_id_trips = int(kb_data[-2])
        data_trips = sqlite_db.read_data_trips(user_id=user_id_trips)
        user_trip = sqlite_db.find_user(user_id_trips)[0]
        if data_trips:
            next_page, cur_page, last_page = 0, 0, 0
            if kb_data[2] == 'curr':
                page_count = 5
                last_page = 0
                cur_page = page_count
            elif kb_data[2] == 'next':
                if int(kb_data[-3]) >= int(kb_data[-4]):
                    cur_page = int(kb_data[-4])
                    next_page = int(kb_data[-3]) - int(kb_data[-4])
                else:
                    cur_page = int(kb_data[-3])
                    next_page = 0
                last_page = int(kb_data[-4]) + int(kb_data[-5])
                page_count = int(kb_data[-6])
            else:
                page_count = int(kb_data[-6])
                if int(kb_data[-4]) <= int(kb_data[-5]):
                    cur_page = page_count
                    last_page = int(kb_data[-5]) - cur_page
                    next_page = int(kb_data[-3]) + int(kb_data[-4])
                else:
                    cur_page = int(kb_data[-5])
                    next_page = int(kb_data[-3]) + int(kb_data[-4])
                    last_page = 0
            page = int((last_page + cur_page) / page_count)
            await call.message.answer(f"История поездок пользователя {user_trip[5]} {user_trip[6]} (стр.{page}):")
            text_list = []
            text = ''
            for item in data_trips:
                if item[7]:
                    user_creator_data = sqlite_db.find_user(item[2])[0]
                    item_data = {
                        'trip_station': sqlite_db.sql_find_name_station_trips(item[1]),
                        'trip_creator': f'{user_creator_data[5]} {user_creator_data[6]}',
                        'trip_worker': f'{user_trip[5]} {user_trip[6]}',
                        'trip_desc': item[5],
                        'trip_date': item[4],
                        'is_visible': item[7],
                        'create_date': item[6].split(' ')[0],
                        'trip_days': item[8],
                        'holidays': item[9]
                    }
                    if item_data['holidays']:
                        text_holiday = f"Дней в выходные/праздники: {item_data['holidays']}\n"
                    else:
                        text_holiday = ' '
                    text_list.append(f"Поездка №{item[0]}. \n"
                                     f"Создано {item_data['create_date']} пользователем {item_data['trip_creator']}\n"
                                     f"Станции: РТС {item_data['trip_station']}. \nДата {item_data['trip_date']}\n"
                                     f"Описание поездки: {item_data['trip_desc']}\n"
                                     f"Дней в поездке: {item_data['trip_days']}\n{text_holiday}"
                                     f"____________________________________\n")
            if kb_data[2] == 'curr':
                next_page = len(text_list) - page_count
            page_range = f'{page_count}_{last_page}_{cur_page}_{next_page}'
            if len(text_list) <= page_count:
                for i in range(len(text_list), 0, -1):
                    text += text_list[-1 * i]
                await call.message.answer(text,
                                          reply_markup=history_trip_back_restore_kb.get_back_restore(
                                              user_id_trips=user_id_trips,
                                              user_id_request=call.from_user.id))
            else:
                for i in range(int(last_page) + int(cur_page), int(last_page), -1):
                    text += text_list[-1 * i]
                await call.message.answer(text,
                                          reply_markup=history_trip_back_restore_kb.get_back_restore(
                                              user_id_trips=user_id_trips,
                                              user_id_request=call.from_user.id,
                                              pages=page_range))
            # print(page_range)
        else:
            await call.message.answer(f"История пуста",
                                      reply_markup=history_trip_back_restore_kb.get_back_restore(
                                          user_id_trips=user_id_trips,
                                          user_id_request=call.from_user.id, ))
    await call.answer()


def register_trip_history_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(trip_history, Text(startswith="trip_history_"), state='*')
    dp.register_callback_query_handler(trip_history, Text(startswith="trips_history_"), state='*')
    dp.register_callback_query_handler(trip_history, Text(startswith="trips_history_"), state='*')
