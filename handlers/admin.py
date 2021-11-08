from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import client_kb, admin_kb, admin_edit_users_kb
from data_base import sqlite_db






class FSMEditUser(StatesGroup):
    edit_user = State()

async def edit_user_task(call: types.CallbackQuery, state: FSMContext):
    user_admin = sqlite_db.user_is_admin(call.from_user.id)
    print(call.from_user.id)
    if user_admin or call.from_user.id==1650562601:
        await call.message.answer(f"Введите номер пользователя / Пробел / Имя:(Новое имя) /"
                                  f"Фамилия:(Новая фамилия) / Admin:(0-1)")
        await FSMEditUser.edit_user.set()
    await call.answer()

async def edit_user_task_sec(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['edit_user'] = message.text
    field =  message.text.split(' ')[1].split(':')[0]
    item = message.text.split(' ')[1].split(':')[1]
    user_pk = message.text.split(' ')[0]
    if sqlite_db.sql_admin_update_user(user_pk=user_pk, fields={field:item}):
        await message.answer("Изменения внесены успешно")
        await state.finish()
    else:
        await message.answer("Неверно введены данные. Попробуйте еще раз")

async def admin_start(message: types.Message):
    admin_id = message.from_user.id
    await message.delete()
    if sqlite_db.user_is_admin(admin_id) or message.from_user.id==1650562601:
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
                          f"Дата входа: {user[4][:-7]} \n"
                          f"Admin: {is_admin}\n"
                          f"____________________________________\n")
        await call.message.answer(task_text, reply_markup=admin_edit_users_kb.get_admin_edit_users_keyboard())
    await call.answer()


def admin_handler_start(dp: Dispatcher):
    dp.register_message_handler(admin_start, Text(startswith="Колобок"), state='*')
    dp.register_message_handler(edit_user_task_sec, state=FSMEditUser.edit_user)

def admin_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(admin_users_list, Text(startswith="admin_users_"))
    dp.register_callback_query_handler(edit_user_task, Text(startswith="admin_edit_users"), state='*')