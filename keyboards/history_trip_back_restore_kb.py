
from aiogram import types
from data_base import sqlite_db


def get_back_restore(user_id_trips=0, user_id_request=0, pages='5_0_5_0'):
    back = f'profile_back_{user_id_trips}'
    back_history = f'trips_history_back_{pages}_{user_id_trips}_{user_id_request}'
    next_history = f'trips_history_next_{pages}_{user_id_trips}_{user_id_request}'
    # Генерация клавиатуры.
    delete_task = f'trips_delete_{user_id_trips}'
    list_buttons = []

    buttons = [
        types.InlineKeyboardButton(text="Назад к профилю", callback_data=back),
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    if pages.split('_')[1] != '0':
        list_buttons.append(types.InlineKeyboardButton(text="Назад", callback_data=back_history))
        # print(pages.split('_')[1])
    if pages.split('_')[3] != '0':
        list_buttons.append(types.InlineKeyboardButton(text="Вперед", callback_data=next_history))
        # print(pages.split('_')[3])
    if len(list_buttons) != 0:
        keyboard.add(*list_buttons)

    if user_id_trips == user_id_request or sqlite_db.user_is_admin(user_id_request):
        delete_button = types.InlineKeyboardButton(text="Удалить запись", callback_data=delete_task)
        keyboard.add(*buttons).add(delete_button)
    else:
        keyboard.add(*buttons)

    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку


    return keyboard

def get_trips_history_back(user_id):
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="История поездок", callback_data=f"trip_history_curr_{user_id}"),
    ]
    # mobility = types.InlineKeyboardButton(text="Мобилити (Активные задания)", callback_data="mobility_list")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    # keyboard.add(*buttons).add(mobility)
    keyboard.add(*buttons)
    return keyboard