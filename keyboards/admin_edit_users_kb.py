from aiogram import types

def get_admin_edit_users_keyboard():
    edit_users = f'admin_edit_users'
    # Генерация клавиатуры.


    # button = types.InlineKeyboardButton(text="Редактировать пользователя", callback_data=edit_users)
    buttons = [
        types.InlineKeyboardButton(text="Редактировать", callback_data=edit_users)
    ]
    keyboard_edit_user = types.InlineKeyboardMarkup(row_width=2)
    keyboard_edit_user.add(*buttons)
    return keyboard_edit_user
