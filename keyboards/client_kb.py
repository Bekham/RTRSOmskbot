from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
b1 = KeyboardButton('Станции')
b2 = KeyboardButton('Отмена создания задания')
kb_client = ReplyKeyboardMarkup(resize_keyboard=True)
kb_station_cancel = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client.add(b1)
kb_station_cancel.add(b1).add(b2)