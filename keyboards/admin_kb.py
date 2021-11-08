from aiogram import types

def get_admin_keyboard(user_id):
    users_list = f'admin_users_{user_id}'
    # Генерация клавиатуры.
    list_buttons = []

    buttons = [
        types.InlineKeyboardButton(text="Все пользователи", callback_data=users_list)
    ]
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.add(*buttons)

    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку


    return keyboard