from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import start, client, admin, other


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()



start.register_handler_start(dp)
client.register_handler_client(dp)
client.register_callback_query_handler(dp)
admin.register_handler_admin(dp)
other.register_handler_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
