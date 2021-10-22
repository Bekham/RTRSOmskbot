from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State

from first_test.create_bot import bot
from first_test.keyboards import client_kb
from first_test.data_base import sqlite_db

# USER_ID = None
# VERIFICATION = False
# LOGIN = False

class FSMStart(StatesGroup):
    verification = State()

class AddUser(StatesGroup):
    username = State()



async def command_start(message: types.Message):


    # global ID
    # global VERIFICATION
    # USER_ID = message.from_user.id
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    print(user_data)
    if user_data == None:
        await message.answer(f'Добро пожаловать в Семью!\n'
                               f'Чтобы пройти верификацию тебе нужно сообщить мне '
                               f'Имя нашего Отца (Директор):')
        await FSMStart.verification.set()
    else:
        # message.text = 'олег'
        await hello(message=message, verif = True)


async def start_verification(message: types.Message, state: FSMContext):
    await state.update_data(verification=(message.text).lower())
    if (message.text).lower() == 'олег':
        # await state.finish()
        await hello(message, verif=True)


async def hello(message: types.Message, verif):
    if verif == True:
        await message.answer('Добро пожаловать в РТРС ОМСК')
        user_data = sqlite_db.sql_read_user(message.from_user.id)
        # try:
        if user_data != None:
            await message.answer(f'Приветствую, {user_data[2]}!')#, reply_markup=client_kb.kb_client)
        else:

            if (message.from_user.first_name).lower() == 'igorio':
                await bot.message.answer(f'Приветствую тебя, Лысый Троль! Как к тебе обращаться?!')
            else:
                await message.answer(
                                       f'Приветствую, {message.from_user.first_name}! Как к тебе обращаться?!')
            await AddUser.username.set()
        # await message.delete()
        # await FSMClient.next()
        # except:
            # await message.reply('Общение с ботом через ЛС!, напишите ему\nhttps://t.me/LetMeTellAboutUBot')
            # pass


#
async def load_username(message: types.Message, state: FSMContext):
    # if LOGIN != True:
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    if user_data == None:
        async with state.proxy() as data:
            # data['username'] = message.text
            data['username'] = await state.get_data()
            await sqlite_db.sql_add_new_user(message.from_user, data['username'])
    elif message.text != user_data[2]:
        sqlite_db.sql_update_user(message.from_user.id, message.text)
    await bot.send_message(message.from_user.id,
                           f'Хорошо, {message.text}! Приступим!')#, reply_markup=client_kb.kb_client)
    # sqlite_db.sql_update_date_user(message.from_user.id)
    # LOGIN = True
    print('LOGIN')
    await state.finish()



# async def cmd_cancel(message: types.Message, state: FSMContext):
#     await state.finish()
#     await message.answer("Действие отменено", reply_markup=types.ReplyKeyboardRemove())





def register_handler_start(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start'], state='*')
    dp.register_message_handler(start_verification, state=FSMStart.verification)
    dp.register_message_handler(hello, state='*')
    dp.register_message_handler(load_username, state=AddUser.username)
    # dp.register_message_handler(cmd_cancel, commands="cancel", state="*")
    # dp.register_message_handler(cmd_cancel, Text(equals="отмена", ignore_case=True), state="*")

