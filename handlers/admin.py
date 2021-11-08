from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import client_kb, admin_kb
from data_base import sqlite_db


async def admin_start(message: types.Message):
    admin_id = message.from_user.id
    await message.delete()
    if sqlite_db.user_is_admin(admin_id):
        await message.answer(f'Раздел Админка.', reply_markup=admin_kb.get_admin_keyboard(admin_id))


async def admin_users_list(call: types.CallbackQuery):
    admin_id = call.data.split("_")[-1]
    if sqlite_db.user_is_admin(admin_id):
        users = sqlite_db.sql_read_all_user()
        task_text = ''
        for user in users:
            if user[7]:
                is_admin = True
            else:
                is_admin = False
            task_text += (f"{user[0]}: {user[5]} {user[6]} \n "
                          f"Дата входа: {user[4]} \n"
                          f"Admin: {is_admin}\n"
                          f"____________________________________\n")

        await call.message.answer(task_text)
    await call.answer()

def admin_handler_start(dp: Dispatcher):
    dp.register_message_handler(admin_start, Text(startswith="Колобок"), state='*')

def admin_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(admin_users_list, Text(startswith="admin_users_"))