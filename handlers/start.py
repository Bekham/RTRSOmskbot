from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from create_bot import bot
from keyboards import client_kb
from data_base import sqlite_db


class FSMStart(StatesGroup):
    verification = State()
    first_name = State()
    last_name = State()


async def command_start(message: types.Message):
    await message.delete()
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    print(user_data)
    if user_data == None:
        await message.answer(f'Добро пожаловать в Семью!\n'
                               f'Чтобы пройти верификацию тебе нужно сообщить мне '
                               f'фамилию нашего Начальника:')
        await FSMStart.verification.set()
    else:
        if user_data[8] == None:
            # print(message)
            # print(message.from_user.id)
            sqlite_db.sql_update_user_chat_id(message.from_user.id, message.chat.id)

        await message.answer(f'Привет, {user_data[2]}!\n'
                             f'Добро пожаловать в РТРС ОМСК',
                             reply_markup=client_kb.kb_client)


async def start_verification(message: types.Message, state: FSMContext):
    if (message.text).lower() != 'пронин':
        await message.answer("Неверно! Или ты Никита или засланый казачок!")
        return
    verification = True
    async with state.proxy() as data:
        data['verification'] = verification
    await message.answer("Добро пожаловать в РТРС ОМСК\n"
                         "Давай познакомимся!\n"
                         "Как тебя зовут?")
    await FSMStart.next()


async def start_firstname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        verification = data.get('verification')
        data['first_name'] = message.text
    if verification:
        await message.answer("Отлично! А теперь напиши свою фамилию:")
        await FSMStart.next()

async def start_lastname(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        verification = data.get('verification')
        data['last_name'] = message.text
        first_name = data.get('first_name')
    if verification:
        await sqlite_db.sql_add_new_user(state, user_id = message.from_user.id)
        if (message.from_user.first_name).lower() == 'igorio':
            await message.answer(f'Привет, Лысый Троль! \n'
                                     f'Регистрация завершена!\n'
                                     f'Приступим!', reply_markup=client_kb.kb_client)
        else:
            await message.answer(f'Привет, {first_name.title()} {data["last_name"].title()}\n'
                                     f'Регистрация завершена! \n'
                                     f'Приступим!', reply_markup=client_kb.kb_client)
        await state.finish()


async def cmd_cancel(message: types.Message, state: FSMContext):
    await state.finish()
    await message.answer("Действие отменено", reply_markup=client_kb.kb_client)


async def command_help(message: types.Message):
    await message.delete()
    await message.answer(f'Помощь начинающему АПГшнику:\n'
                         f'1. Чтобы начать процесс авторизации, необходимо ввести:\n /start \n '
                         f'2. Команда "Отмена" позволяет выйти из процесса регистрации/удаления/восстановления задания.'
                         f'3. Выход к перечню станций через кнопку Станции (внизу экрана) или команду "Станции".')





def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(command_help, commands=['help'], state='*')
    dp.register_message_handler(command_help, Text(startswith="help"), state='*')
    dp.register_message_handler(command_help, Text(startswith="Help"), state='*')
    dp.register_message_handler(command_help, Text(startswith="Помощь"), state='*')
    dp.register_message_handler(command_help, Text(startswith="помощь"), state='*')
    dp.register_message_handler(start_verification, state=FSMStart.verification)
    dp.register_message_handler(start_firstname, state=FSMStart.first_name)
    dp.register_message_handler(start_lastname, state=FSMStart.last_name)
    # dp.register_message_handler(load_username, state=AddUser.username)
    dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")
    dp.register_message_handler(cmd_cancel, Text(equals="Отмена создания задания", ignore_case=True), state="*")

