from aiogram import types

from data_base import sqlite_db


def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Бекишево", callback_data="trip_st_bekishevo"),
        types.InlineKeyboardButton(text="Веселая Поляна", callback_data="trip_st_vp"),
        types.InlineKeyboardButton(text="Вольное", callback_data="trip_st_volnoe"),
        types.InlineKeyboardButton(text="Екатеринославка", callback_data="trip_st_ekatrinoslavka"),
        types.InlineKeyboardButton(text="Михайловка", callback_data="trip_st_mihailovka"),
        types.InlineKeyboardButton(text="Москаленский", callback_data="trip_st_moskalensky"),
        types.InlineKeyboardButton(text="Неверовка", callback_data="trip_st_neverovka"),
        types.InlineKeyboardButton(text="Новоцарицыно", callback_data="trip_st_novotsaritsino"),
        types.InlineKeyboardButton(text="Одесское", callback_data="trip_st_odesskoe"),
        types.InlineKeyboardButton(text="Павлоградка", callback_data="trip_st_pavlogradka"),
        types.InlineKeyboardButton(text="Паново", callback_data="trip_st_panovo"),
        types.InlineKeyboardButton(text="Полтавка", callback_data="trip_st_polavka"),
        types.InlineKeyboardButton(text="Русская Поляна", callback_data="trip_st_rp"),
        types.InlineKeyboardButton(text="Саргатское", callback_data="trip_st_sargatskoe"),
        types.InlineKeyboardButton(text="Цветково", callback_data="trip_st_setkovo"),
        types.InlineKeyboardButton(text="Цветнополье", callback_data="trip_st_tsvetnopole"),
        types.InlineKeyboardButton(text="Щербакуль", callback_data="trip_st_sherbakul"),
        types.InlineKeyboardButton(text="Щербаки", callback_data="trip_st_sherbaki"),
        types.InlineKeyboardButton(text="Называевск", callback_data="trip_st_nz"),
        types.InlineKeyboardButton(text="Хутора", callback_data="trip_st_khutora"),
        types.InlineKeyboardButton(text="Исилькуль", callback_data="trip_st_isilkul"),
    ]

    # mobility = types.InlineKeyboardButton(text="Мобилити (Активные задания)", callback_data="mobility_list")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=3)
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
