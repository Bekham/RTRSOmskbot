
from aiogram import types


def get_back_restore(st_name):
    back = f'st_{st_name}'
    restore = f'restore_{st_name}'
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Назад", callback_data=back),
        types.InlineKeyboardButton(text="Восстановить задание", callback_data=restore)
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)
    return keyboard