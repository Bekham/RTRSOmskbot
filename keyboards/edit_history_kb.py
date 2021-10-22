from aiogram import types
# from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

edit_history_client = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = ["Создать задание", "История"]
edit_history_client.add(*buttons)