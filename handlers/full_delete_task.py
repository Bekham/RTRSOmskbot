from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import history_back_restore_kb, client_kb


class FSMFullDeleteTask(StatesGroup):
    station = State()
    full_delete_task = State()

async def full_delete_task(call: types.CallbackQuery, state: FSMContext):
    user_admin = sqlite_db.user_is_admin(call.from_user.id)
    if user_admin:
        station = call.data.split("_admin_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                await call.message.answer(f"Полное удаление задания станции {item[1]}.\n"
                                          f"Введите номер задания:",
                                          reply_markup=client_kb.kb_client)

                await FSMFullDeleteTask.full_delete_task.set()
                async with state.proxy() as data:
                    data['station'] = item[2]
    await call.answer()



async def full_delete_task_num(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['full_delete_task'] = message.text
        station = data.get('station')
    tasks = data['full_delete_task'].split(' ')
    for task in tasks:
        if await sqlite_db.sql_full_delete_task(station, task):
            await message.answer(f"Задание №{task} удалено успешно!")
        else:
            await message.answer("Ошибка! Задание не удалено!",
                                 reply_markup=history_back_restore_kb.get_back_restore(station))
    await message.answer(f"Удаление завершено!",
                             reply_markup=history_back_restore_kb.get_back_restore(station))
    await state.finish()





def register_full_delete_task_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(full_delete_task, Text(startswith="delete_admin_"), state='*')


def register_handler_full_delete_task(dp: Dispatcher):
    dp.register_message_handler(full_delete_task_num, state=FSMFullDeleteTask.full_delete_task)
