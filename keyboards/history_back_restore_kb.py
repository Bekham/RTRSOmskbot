
from aiogram import types
from data_base import sqlite_db


def get_back_restore(st_name, user_id=0, pages='4_1'):
    back = f'st_{st_name}'
    restore = f'restore_{st_name}'
    delete_admin = f'delete_admin_{st_name}'
    back_history = f'back_history_{pages}'
    next_history = f'back_history_{pages}'
    # Генерация клавиатуры.
    list_buttons = [
        types.InlineKeyboardButton(text="Назад", callback_data=back_history),
        types.InlineKeyboardButton(text="Далее", callback_data=next_history)
    ]
    buttons = [
        types.InlineKeyboardButton(text="Назад к заданиям", callback_data=back),
        types.InlineKeyboardButton(text="Восстановить задание", callback_data=restore)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if sqlite_db.user_is_admin(user_id):

        admin_button = types.InlineKeyboardButton(text="Удалить задание", callback_data=delete_admin)
        keyboard.add(*list_buttons).add(*buttons).add(admin_button)
    else:
        keyboard.add(*buttons)

    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку


    return keyboard