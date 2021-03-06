
from aiogram import types


def get_back_delete(st_name):
    back = f'st_{st_name}'
    delete_task = f'del_task_{st_name}'
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Назад к заданиям", callback_data=back),
        types.InlineKeyboardButton(text="Выполнить задание", callback_data=delete_task)
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard