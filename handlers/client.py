from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from keyboards import stations_kb
from create_bot import bot
from keyboards import client_kb
from data_base import sqlite_db
from keyboards.edit_history_kb import edit_history_client


async def stations(message: types.Message):
    user_data = sqlite_db.sql_read_user(message.from_user.id)
    if message.from_user.id == user_data[1]:
        await message.answer("Станции Омского Цеха:", reply_markup=stations_kb.get_keyboard())



async def callbacks_num(call: types.CallbackQuery):
    print('sdff')
    # Парсим строку и извлекаем действие, например `st_incr` -> `incr`
    action = call.data.split("_")[1]
    if action == "bekishevo":
        await call.message.edit_text(f"Здесь будут задания станции {action}", reply_markup=edit_history_client)
        # await message.answer("Станции Омского Цеха:", reply_markup=stations_kb.get_keyboard())
    elif action == "vp":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "ekatrinoslavka":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "mihailovka":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "moskalensky":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "neverovka":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "novotsaritsino":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "odesskoe":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "omsk":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "pavlogradka":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "panovo":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "polavka":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "rp":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "sargatskoe":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "tsetkovo":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "tsvetnopole":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "sherbakul":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "sherbaki":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "nz":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "khutora":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    elif action == "isilkul":
        await call.message.edit_text(f"Здесь будут задания станции {action}")
    # elif action == "finish":
        # Если бы мы не меняли сообщение, то можно было бы просто удалить клавиатуру
        # вызовом await call.message.delete_reply_markup().
        # Но т.к. мы редактируем сообщение и не отправляем новую клавиатуру,
        # то она будет удалена и так.
        # await call.message.edit_text(f"Итого: {user_value}")
    # Не забываем отчитаться о получении колбэка
    await call.answer()
# def register_handler_client(dp: Dispatcher):
def register_handler_client(dp: Dispatcher):
    dp.register_message_handler(stations, commands=['Станции'], state='*')
    # dp.callback_query_handler(callbacks_num, Text(startswith="st_"))

def register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(callbacks_num, Text(startswith="st_"))


