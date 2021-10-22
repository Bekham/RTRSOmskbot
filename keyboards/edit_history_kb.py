# from aiogram import types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

edit_history_client = ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Создать задание", "История"]
but_station = KeyboardButton('Станции')
edit_history_client.add(*buttons).add(but_station)