from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text, state
from aiogram.dispatcher.filters.state import StatesGroup, State

from data_base import sqlite_db
from keyboards import edit_history_kb, client_kb, back_delete_kb


class FSMDel_task(StatesGroup):
    station = State()
    num_del = State()

async def delete_task(call: types.CallbackQuery, state: FSMContext):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        station = call.data.split("_task_")[1]
        data_stations = sqlite_db.sql_read_all_stations()
        for item in data_stations:
            if station == item[2]:
                await call.message.answer(f"Выполнение задания станции {item[1]}.\n"
                                          f"Введите номер задания для выполнения:",
                                          reply_markup=client_kb.kb_client)
                # await call.message.answer("Введите номер задания для удаления:")
                await FSMDel_task.num_del.set()
                async with state.proxy() as data:
                    data['station'] = item[2]
    await call.answer()



async def task_num_delete(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['num_del'] = message.text
        station = data.get('station')
    if await sqlite_db.sql_delete_task(state, user_id=message.from_user.id,  is_active=0):
        await message.answer("Данные успешно сохранены!",
                             reply_markup=back_delete_kb.get_back_delete(station))
    else:
        await message.answer("Ошибка! Задание не сохранено!",
                             reply_markup=back_delete_kb.get_back_delete(station))
    # print(data['description'], station)
    await state.finish()





def register_delete_task_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(delete_task, Text(startswith="del_task_"), state='*')


def register_handler_delete_task(dp: Dispatcher):
    dp.register_message_handler(task_num_delete, state=FSMDel_task.num_del)
