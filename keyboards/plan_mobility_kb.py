
from aiogram import types


def get_plan_tasks():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Активные плановые задания", callback_data='_plan_tasks')
    ]
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(*buttons)
    return keyboard