from aiogram import types
import emoji
from data_base import sqlite_db


def get_keyboard(add_st=None):
    # Генерация клавиатуры.
    all_stations = sqlite_db.sql_read_all_stations()
    buttons = []
    if add_st:
        select_stations = add_st.split('_')
    else:
        select_stations = []
    for station in all_stations:
        if station[1] != 'Омск':
            if station[2] not in select_stations:
                buttons.append(types.InlineKeyboardButton(text=station[1], callback_data=f"trip_st_{station[2]}"))
            else:
                buttons.append(types.InlineKeyboardButton(
                    text=f'{emoji.emojize(":check_mark_button:")}{station[1]}',
                    callback_data=f"trip_st_{station[2]}"))

    # mobility = types.InlineKeyboardButton(text="Мобилити (Активные задания)", callback_data="mobility_list")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    # keyboard.add(*buttons).add(mobility)
    keyboard.add(*buttons).add(types.InlineKeyboardButton(
        text=f'{emoji.emojize(":fast-forward_button:")}  Далее  {emoji.emojize(":fast-forward_button:")}',
        callback_data=f'trip_st_next'))
    return keyboard


def get_trip_date():
    trip_date = [
        types.InlineKeyboardButton(text="Да", callback_data="trip_data_yes"),
        types.InlineKeyboardButton(text="Нет", callback_data="trip_data_no"),
    ]
    date = types.InlineKeyboardMarkup(row_width=2)
    date.add(*trip_date)
    return date


def get_trip_days(days_len=1):
    trip_days = []
    for day in range(1, days_len+1):
        trip_days.append(types.InlineKeyboardButton(text=f'{day}', callback_data=f"trip_days_{day}"))
    days = types.InlineKeyboardMarkup(row_width=days_len)
    days.add(*trip_days)
    return days


def get_trip_user():
    all_users = sqlite_db.sql_read_all_user()
    buttons_users = []
    for user in all_users:
        buttons_users.append(
            types.InlineKeyboardButton(text=f"{user[5]} {user[6]}", callback_data=f"trip_user_{user[1]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons_users)
    return keyboard
