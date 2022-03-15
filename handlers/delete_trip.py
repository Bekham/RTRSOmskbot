import asyncio

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import edit_history_kb, client_kb, back_delete_kb, history_trip_back_restore_kb


class FSMDel_trip(StatesGroup):
    user_trip = State()
    num_del = State()

async def delete_trip(call: types.CallbackQuery, state: FSMContext):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    kb_data = call.data.split("_")
    user_id_trip = int(kb_data[-1])
    user_trip = sqlite_db.find_user(user_id_trip)[0]
    if call.from_user.id == user_data[1] and user_id_trip == call.from_user.id:

        await call.answer()
        data_trips = sqlite_db.read_data_trips(user_id=user_id_trip)
        # data_stations = sqlite_db.sql_read_all_stations()
        # for item in data_trips:
        msg_id = call.inline_message_id
        await call.message.answer(f"Удаление поездки пользователя {user_trip[5]} {user_trip[6]}.\n"
                                        f"Введите номер поездки для удаления:",
                                        reply_markup=client_kb.kb_station_cancel)
        # await call.message.answer("Введите номер задания для удаления:")

        async with state.proxy() as data:
            data['user_trip'] = user_id_trip
        await FSMDel_trip.num_del.set()
        await asyncio.sleep(30)
        try:
            async with state.proxy() as data:
                if len(data) == 2:
                    pass
                else:
                    raise KeyError
        except KeyError:
            # Если пользователь не ответил или за это время state завершился, получаем KeyError
            async with state.proxy() as data:
                # print(msg_id)
                if len(data) == 1 and msg_id == call.inline_message_id:
                    await call.message.answer(f'Выполнение задания отменено', reply_markup=client_kb.kb_client)
                    await state.finish()
    # await call.answer()

async def task_num_delete_trip(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['num_del'] = message.text
        trip_id = data.get('user_trip')

    if await sqlite_db.sql_delete_trip(state, is_active=0):
        await message.answer("Данные удалены успешно!", reply_markup=client_kb.kb_client)
        await message.answer("Запись о поездке удалена!",
                             reply_markup=history_trip_back_restore_kb.get_trips_history_back(trip_id))
    else:
        await message.answer("Ошибка удаления!", reply_markup=client_kb.kb_client)
        await message.answer("Запись о поездке не удалена!",
                             reply_markup=history_trip_back_restore_kb.get_trips_history_back(trip_id))
    # print(data['description'], station)
    await state.finish()





def register_delete_trip_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(delete_trip, Text(startswith="trips_delete_"), state='*')


def register_handler_delete_trip(dp: Dispatcher):
    dp.register_message_handler(task_num_delete_trip, state=FSMDel_trip.num_del)
