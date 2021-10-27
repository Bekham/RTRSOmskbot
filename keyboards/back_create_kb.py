
from aiogram import types


def get_back_create(st_name):
    back = f'st_{st_name}'
    create = f'new_task_{st_name}'
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Назад к заданиям", callback_data=back),
        types.InlineKeyboardButton(text="Создать задание", callback_data=create)
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard