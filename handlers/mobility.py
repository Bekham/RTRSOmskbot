
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
    max_msg_length = 3000

    for item in mobility_list:
        if item[7] and item[3].startswith('Плановое'):
            # print(item)
            task_text += (f"Станция: {item[2]}. Дата: {item[5]}. \n "
                          f"Описание: {item[4]}\n"
                          f"____________________________________\n")
    print(len(task_text))
    if len(task_text) < max_msg_length:
        await call.message.answer(task_text)
    else:

        all_len = len(task_text)
        msg_count = int(all_len/max_msg_length)
        msg_count_len = int(all_len/msg_count)-2
        start = 0
        end = msg_count_len
        for i in range(1, msg_count+1):
            await call.message.answer(task_text[start : end])
            start += msg_count_len
            if (end + msg_count_len) < all_len:
                end += msg_count_len
            else:
                end = all_len
    await call.answer()

def mobility_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(mobility_alarm_list, Text(startswith="mobility_list"))
    dp.register_callback_query_handler(mobility_plan_list, Text(startswith="_plan_tasks"))