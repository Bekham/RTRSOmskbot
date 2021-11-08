from aiogram import types


def get_keyboard():
    # Генерация клавиатуры.
    buttons = [
        types.InlineKeyboardButton(text="Бекишево", callback_data="st_bekishevo"),
        types.InlineKeyboardButton(text="Веселая Поляна", callback_data="st_vp"),
        types.InlineKeyboardButton(text="Вольное", callback_data="st_volnoe"),
        types.InlineKeyboardButton(text="Екатеринославка", callback_data="st_ekatrinoslavka"),
        types.InlineKeyboardButton(text="Михайловка", callback_data="st_mihailovka"),
        types.InlineKeyboardButton(text="Москаленский", callback_data="st_moskalensky"),
        types.InlineKeyboardButton(text="Неверовка", callback_data="st_neverovka"),
        types.InlineKeyboardButton(text="Новоцарицыно", callback_data="st_novotsaritsino"),
        types.InlineKeyboardButton(text="Одесское", callback_data="st_odesskoe"),
        types.InlineKeyboardButton(text="Павлоградка", callback_data="st_pavlogradka"),
        types.InlineKeyboardButton(text="Паново", callback_data="st_panovo"),
        types.InlineKeyboardButton(text="Полтавка", callback_data="st_polavka"),
        types.InlineKeyboardButton(text="Русская Поляна", callback_data="st_rp"),
        types.InlineKeyboardButton(text="Саргатское", callback_data="st_sargatskoe"),
        types.InlineKeyboardButton(text="Цветково", callback_data="st_tsetkovo"),
        types.InlineKeyboardButton(text="Цветнополье", callback_data="st_tsvetnopole"),
        types.InlineKeyboardButton(text="Щербакуль", callback_data="st_sherbakul"),
        types.InlineKeyboardButton(text="Щербаки", callback_data="st_sherbaki"),
        types.InlineKeyboardButton(text="Называевск", callback_data="st_nz"),
        types.InlineKeyboardButton(text="Хутора", callback_data="st_khutora"),
        types.InlineKeyboardButton(text="Исилькуль", callback_data="st_isilkul"),
        types.InlineKeyboardButton(text="Омск", callback_data="st_omsk"),
    ]
    mobility = types.InlineKeyboardButton(text="Мобилити (Активные задания)", callback_data="mobility_list")
    # Благодаря row_width=2, в первом ряду будет две кнопки, а оставшаяся одна
    # уйдёт на следующую строку
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    keyboard.add(*buttons).add(mobility)
    return keyboard