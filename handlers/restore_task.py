from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import history_back_restore_kb, client_kb, back_create_kb


class FSMRestoreTask(StatesGroup):
    station = State()
    restores_task = State()

async def restore_task(call: types.CallbackQuery, state: FSMContext):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                await call.message.answer(f"Восстановление задания станции {item[1]}."
                                          f"Введите номер задания:",
                                          reply_markup=client_kb.kb_client)

                await FSMRestoreTask.restores_task.set()
                async with state.proxy() as data:
                    data['station'] = item[2]
    await call.answer()



async def restore_task_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['restores_task'] = message.text
        station = data.get('station')
    if await sqlite_db.sql_restore_task(state, user_id=message.from_user.id):
        await message.answer("Данные восстановлены успешно!",
                             reply_markup=history_back_restore_kb.get_back_restore(station))
    else:
        await message.answer("Ошибка! Задание не восстановлено!",
                             reply_markup=history_back_restore_kb.get_back_restore(station))
    # print(data['description'], station)
    await state.finish()





def register_restore_task_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(restore_task, Text(startswith="restore_"), state='*')


def register_handler_restore_task(dp: Dispatcher):
    dp.register_message_handler(restore_task_num, state=FSMRestoreTask.restores_task)
