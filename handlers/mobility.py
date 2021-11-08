
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from keyboards import stations_kb, plan_mobility_kb
from data_base import sqlite_db

async def mobility_alarm_list(call: types.CallbackQuery):
    mobility_list = sqlite_db.sql_read_all_mobility()
    task_text = f'Активные аварийные задания: \n'
    for item in mobility_list:
        if item[7] and not item[3].startswith('Плановое'):
            # print(item)
            task_text += (f"Станция: {item[2]}. Дата: {item[5]}. \n "
                          f"Описание: {item[4]}\n"
                          f"____________________________________\n")
    await call.message.answer(task_text,
                              reply_markup=plan_mobility_kb.get_plan_tasks())
    await call.answer()


async def mobility_plan_list(call: types.CallbackQuery):
    mobility_list = sqlite_db.sql_read_all_mobility()
    task_text = f'Активные плановые задания: \n'
    for item in mobility_list:
        if item[7] and item[3].startswith('Плановое'):
            # print(item)
            task_text += (f"Станция: {item[2]}. Дата: {item[5]}. \n "
                          f"Описание: {item[4]}\n"
                          f"____________________________________\n")
    await call.message.answer(task_text)
    await call.answer()

def mobility_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(mobility_alarm_list, Text(startswith="mobility_list"))
    dp.register_callback_query_handler(mobility_plan_list, Text(startswith="_plan_tasks"))