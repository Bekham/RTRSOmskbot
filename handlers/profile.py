from datetime import datetime

from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import stations_kb, profile_kb
from data_base import sqlite_db
from keyboards import edit_history_kb


async def profile_main(message: types.Message):
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    sqlite_db.sql_update_user_visit(message.from_user.id)
    try:
        if message.from_user.id == user_data[1]:
            profit_tasks = sqlite_db.sql_find_all_task_by_user_id(message.from_user.id)
            profit_trips = sqlite_db.sql_find_all_trips_count_by_user_id(message.from_user.id)
            profit_trips_days = sqlite_db.read_data_trips(int(message.from_user.id))
            trip_days = 0
            holidays = 0
            for trip in profit_trips_days:
                if trip[7]:
                    trip_days += int(trip[8])
                    if trip[9]:
                        holidays += int(trip[9])
            profile_data = {
                'first_name': user_data[5],
                'last_name': user_data[6],
                'create_date': f"{str(user_data[3]).split(' ')[0]}"
            }
            if profit_tasks:
                profile_data['create_tasks'] = profit_tasks[0]
                profile_data['close_tasks'] = profit_tasks[1]
            else:
                profile_data['create_tasks'] = 0
                profile_data['close_tasks'] = 0
            # await message.answer(f"Профиль пользователя:\n", reply_markup=profile_kb.any_msg())
            await message.answer(f"Профиль пользователя:\n"
                                 f"Имя: {profile_data['first_name']}\n"
                                 f"Фамилия: {profile_data['last_name']}\n"
                                 f"Дата регистрации: {profile_data['create_date']}\n\n"
                                 f"Заданий создано: {profile_data['create_tasks']}\n"
                                 f"Заданий выполнено: {profile_data['close_tasks']}\n"
                                 f"Поездок выполнено: {profit_trips}\n"
                                 f"Всего дней в командировках: {trip_days} дней\n"
                                 f"В выходные дни: {holidays} дней\n",
                                 reply_markup=profile_kb.get_trips_history(user_id=user_data[1]))
            # await message.delete()

    except TypeError:
        await message.answer("Введите /start для авторизации")


async def profile_main_back(call: types.CallbackQuery):
    profile_user_id = call.data.split("_back_")[1]
    user_data = sqlite_db.sql_read_user(int(profile_user_id))
    try:
        if user_data:
            profit_tasks = sqlite_db.sql_find_all_task_by_user_id(int(profile_user_id))
            profit_trips = sqlite_db.sql_find_all_trips_count_by_user_id(int(profile_user_id))
            profit_trips_days = sqlite_db.read_data_trips(int(profile_user_id))
            trip_days = 0
            for trip in profit_trips_days:
                if trip[7]:
                    trip_days += int(trip[8])
            profile_data = {
                'first_name': user_data[5],
                'last_name': user_data[6],
                'create_date': f"{str(user_data[3]).split(' ')[0]}"
            }
            if profit_tasks:
                profile_data['create_tasks'] = profit_tasks[0]
                profile_data['close_tasks'] = profit_tasks[1]
            else:
                profile_data['create_tasks'] = 0
                profile_data['close_tasks'] = 0
            await call.message.answer(f"Профиль пользователя:\n"
                                 f"Имя: {profile_data['first_name']}\n"
                                 f"Фамилия: {profile_data['last_name']}\n"
                                 f"Дата регистрации: {profile_data['create_date']}\n\n"
                                 f"Заданий создано: {profile_data['create_tasks']}\n"
                                 f"Заданий выполнено: {profile_data['close_tasks']}\n"
                                 f"Поездок выполнено: {profit_trips}\n"
                                 f"Всего дней в командировках: {trip_days}\n",
                                 reply_markup=profile_kb.get_trips_history(user_id=user_data[1]))
            # await message.delete()
    except TypeError:
        await call.message.answer("Введите /start для авторизации")
    await call.answer()




async def users_profile_list(call: types.CallbackQuery):
    user_data = sqlite_db.sql_read_user(call.from_user.id)
    if call.from_user.id == user_data[1]:
        try:
            await call.message.answer(f"Выберите пользователя для просмотра его профиля",
                             reply_markup=profile_kb.get_user_profiles())
        except TypeError:
            await call.message.answer("Введите /start для авторизации")
    await call.answer()


def register_handler_profile(dp: Dispatcher):
    dp.register_message_handler(profile_main, Text(equals="Профиль"), state='*')


def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(profile_main_back, Text(startswith="profile_back_"), state='*')
    dp.register_callback_query_handler(users_profile_list, Text(startswith="users_profile"), state='*')
