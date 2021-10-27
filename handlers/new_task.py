from aiogram import types, Dispatcher

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State
from create_bot import bot
from data_base import sqlite_db
from keyboards import edit_history_kb, client_kb, back_create_kb


class FSMNew_task(StatesGroup):
    station = State()
    new_task_description = State()

async def new_task(call: types.CallbackQuery, state: FSMContext):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("_task_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                await call.message.answer(f"Создание нового задания станции {item[1]}."
                                          f"Введите описание неисправности:",
                                          reply_markup=client_kb.kb_station_cancel)
                # await call.message.answer("Введите описание неисправности:",
                #                           reply_markup=client_kb.kb_client)
                await FSMNew_task.new_task_description.set()
                async with state.proxy() as data:
                    data['station'] = item[2]
    await call.answer()



async def task_description(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['description'] = message.text
        station = data.get('station')
    task =  message.text
    if await sqlite_db.sql_add_new_task(state, user_id=message.from_user.id):
        await message.answer("Данные записаны успешно!", reply_markup=client_kb.kb_client)
        await message.answer("Задание добавлено в список активных задач!", reply_markup=back_create_kb.get_back_create(station))
        users_data = sqlite_db.sql_read_all_user()
        current_user_data = sqlite_db.sql_read_user(message.from_user.id)
        for user in users_data:
            if user[1] != message.from_user.id and user[8]:
                message.text = f'{current_user_data[5]} {current_user_data[6]} создал задание.\n' \
                               f'Станция: {sqlite_db.sql_find_name_station(station)[0][0]}.\n' \
                               f'Описание: {task}.'
        # await message.reply(message.text)
                message.chat.id = user[8]
                await bot.send_message(message.chat.id, message.text)
    else:
        await message.answer("Ошибка! Задание не записано!", reply_markup=back_create_kb.get_back_create(station))
    # print(data['description'], station)
    await state.finish()





def register_new_task_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(new_task, Text(startswith="new_task_"), state='*')


def register_handler_new_task(dp: Dispatcher):
    dp.register_message_handler(task_description, state=FSMNew_task.new_task_description)
