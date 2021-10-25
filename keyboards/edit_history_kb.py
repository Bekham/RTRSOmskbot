# from aiogram import types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
#
# edit_history_client = ReplyKeyboardMarkup(resize_keyboard=True)
# buttons = ["Создать задание", "История"]
# but_station = KeyboardButton('Станции')
# edit_history_client.add(*buttons).add(but_station)
from aiogram import types


def get_keyboard_station(st_name):
    new_task = f'new_task_{st_name}'
    history = f'history_{st_name}'
    delete_task = f'del_task_{st_name}'
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Создать задание", callback_data=new_task),
        types.InlineKeyboardButton(text="Удалить задание", callback_data=delete_task),
        types.InlineKeyboardButton(text="История", callback_data=history)
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard