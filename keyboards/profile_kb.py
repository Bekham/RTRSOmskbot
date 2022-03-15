from aiogram import types

from data_base import sqlite_db


def get_trips_history(user_id):
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Добавить поездку", callback_data=f"add_trip"),
        types.InlineKeyboardButton(text="История поездок", callback_data=f"trip_history_curr_{user_id}"),
        types.InlineKeyboardButton(text="Профили пользователей", callback_data=f"users_profile"),
    ]
    # mobility = types.InlineKeyboardButton(text="Мобилити (Активные задания)", callback_data="mobility_list")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    # keyboard.add(*buttons).add(mobility)
    keyboard.add(*buttons)
    return keyboard

def get_trip_date():
    trip_date = [
        types.InlineKeyboardButton(text="Да", callback_data="trip_data_yes"),
        types.InlineKeyboardButton(text="Нет", callback_data="trip_data_no"),
    ]
    date = types.InlineKeyboardMarkup(row_width=2)
    date.add(*trip_date)
    return date

def get_trip_user():
    all_users = sqlite_db.sql_read_all_user()
    buttons_users = []
    for user in all_users:
        buttons_users.append(types.InlineKeyboardButton(text=f"{user[5]} {user[6]}", callback_data=f"trip_user_{user[1]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons_users)
    return keyboard

def get_user_profiles():
    all_users = sqlite_db.sql_read_all_user()
    buttons_users = []
    for user in all_users:
        buttons_users.append(types.InlineKeyboardButton(
            text=f"{user[5]} {user[6]}",
            callback_data=f"profile_back_{user[1]}"))
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons_users)
    return keyboard

# def any_msg(answer=None):
#     keyboard = types.InlineKeyboardMarkup()
#     if answer:
#         callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data=answer)
#     else:
#         callback_button = types.InlineKeyboardButton(text="Нажми меня", callback_data="test")
#     keyboard.add(callback_button)
#     return keyboard