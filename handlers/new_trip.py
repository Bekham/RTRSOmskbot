import asyncio
from contextlib import suppress
from datetime import datetime

from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import ChatNotFound

from create_bot import bot, dp
from data_base import sqlite_db
from keyboards import edit_history_kb, client_kb, back_create_kb, stations_kb, stations_trip_kb


class FSMNew_trip(StatesGroup):
    station = State()
    new_trip_description = State()
    trip_date_answer = State()
    trip_date = State()
    trip_user = State()


async def trip_registration(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)

    try:
        if call.from_user.id == user_data[1]:
            await call.message.answer("Регистрация поездки.\n"
                                 "Укажите, куда направляетесь:", reply_markup=stations_trip_kb.get_keyboard())
            await FSMNew_trip.station.set()
            # await message.delete()
    except TypeError:
        await call.message.answer("Введите /start для авторизации")


async def new_trip(call: types.CallbackQuery, state: FSMContext):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    await call.answer()
    # print(call.data)
    if call.from_user.id == user_data[1]:

        station = call.data.split("_st_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                msg_id = call.inline_message_id
                await call.message.answer(f"Поездка в {item[1]}.\n"
                                          f"Введите описание работ:",
                                          reply_markup=client_kb.kb_station_cancel)
                async with state.proxy() as data:
                    data['station'] = item[2]
                await FSMNew_trip.new_trip_description.set()

                await asyncio.sleep(240)
                try:
                    async with state.proxy() as data:
                        if len(data) == 2:
                            pass
                        else:
                            raise KeyError
                except KeyError:
                    # Если пользователь не ответил или за это время state завершился, получаем KeyError
                    async with state.proxy() as data:
                        print(msg_id)
                        if len(data) == 1 and msg_id == call.inline_message_id:
                            await call.message.answer(f'Создание поездки отменено', reply_markup=client_kb.kb_client)
                            await state.finish()


async def trip_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['new_trip_description'] = message.text
    await message.answer(f"Поездка состоится сегодня?",
                         reply_markup=stations_trip_kb.get_trip_date())
    await FSMNew_trip.trip_date_answer.set()

async def trip_date_answer_await(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    date_answer = call.data.split("_data_")[1]
    async with state.proxy() as data:
        data['trip_date_answer'] = call.message.text
    if date_answer == 'yes':
        async with state.proxy() as data:
            data['trip_date'] = datetime.now().date()
        # print(data['trip_date'])
        await call.message.answer(f"Кто едет?",
                                  reply_markup=stations_trip_kb.get_trip_user())
        await FSMNew_trip.trip_user.set()
    else:
        await call.message.answer(f"Укажите дату в формате: '26 12 1988'",
                                  reply_markup=client_kb.kb_station_cancel)
        await FSMNew_trip.trip_date.set()


async def trip_data(message: types.Message, state: FSMContext):
    if message.text:
        try:
            data_read = message.text.split(' ')
            if len(data_read) == 3:
                async with state.proxy() as data:
                    data['trip_date'] = datetime.strptime(f"{data_read[2]}-{data_read[1]}-{data_read[0]}", "%Y-%m-%d")
            else:
                raise KeyError
        except (KeyError, ValueError):
            await message.answer(f"Неверный формат!"
                                 f"Укажите дату в формате: '26 12 1988'",
                                 reply_markup=client_kb.kb_station_cancel)
            await FSMNew_trip.trip_date.set()
            # await state.finish()
        else:
            # print(sqlite_db.sql_read_all_user())
            await message.answer(f"Кто едет?",
                                 reply_markup=stations_trip_kb.get_trip_user())
            await FSMNew_trip.trip_user.set()

async def trip_user_answer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_id = call.data.split("_user_")[1]
    trip_data = {}
    async with state.proxy() as data:
        data['trip_user'] = user_id
        trip_data['trip_station'] = data['station']
        trip_data['trip_creator'] = call.from_user.id
        trip_data['trip_worker'] = data['trip_user']
        trip_data['trip_date'] = data['trip_date']
        trip_data['trip_desc'] = data['new_trip_description']
    if sqlite_db.load_data_trips(trip_data):
        # print('OK')
        current_user_data = sqlite_db.sql_read_user(call.from_user.id)
        current_trip_data = sqlite_db.sql_read_user(int(trip_data['trip_worker']))
        await call.message.answer(f"Данные о поездке записаны успешно!\n"
                                  f"Создано пользователем {current_user_data[5]} {current_user_data[6]}\n"
                                  f"Поездка для {current_trip_data[5]} {current_trip_data[6]}\n"
                                  f"Станция: РТС {trip_data['trip_station']}. Дата {str(trip_data['trip_date']).split(' ')[0]}\n"
                                  f"Описание поездки: {trip_data['trip_desc']}\n"
                                  f"____________________________________\n",
                                  reply_markup=client_kb.kb_client)
        users_data = sqlite_db.sql_read_all_user()

        for user in users_data:
            if user[1] != call.from_user.id and user[8]:
                call.message.text = f"{current_user_data[5]} {current_user_data[6]} создал поездку.\n"\
                                    f"Поездка для {current_trip_data[5]} {current_trip_data[6]}\n"\
                                    f"Станция: РТС {trip_data['trip_station']}. " \
                                    f"Дата {str(trip_data['trip_date']).split(' ')[0]}\n"\
                                    f"Описание поездки: {trip_data['trip_desc']}\n"
                # await message.reply(message.text)
                call.message.chat.id = user[8]
                await bot.send_message(call.message.chat.id, call.message.text)
    else:
        await call.message.answer("Ошибка записи! Попробуйте еще раз!",
                                  reply_markup=client_kb.kb_client)
    await state.finish()




def register_handler_new_trip(dp: Dispatcher):
    dp.register_message_handler(trip_registration, Text(equals="Поездки"), state='*')
    dp.register_message_handler(trip_description, state=FSMNew_trip.new_trip_description)
    dp.register_message_handler(trip_data, state=FSMNew_trip.trip_date)


def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(trip_registration, Text(startswith="add_trip"), state='*')
    dp.register_callback_query_handler(new_trip, Text(startswith="trip_st_"), state=FSMNew_trip.station)
    dp.register_callback_query_handler(trip_date_answer_await, Text(startswith="trip_data_"),
                                       state=FSMNew_trip.trip_date_answer)
    dp.register_callback_query_handler(trip_user_answer, Text(startswith="trip_user_"),
                                       state=FSMNew_trip.trip_user)
