from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import start, client, admin, other, new_task, history, delete_task


async def on_startup(_):
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()



start.register_handler_start(dp)
client.register_handler_client(dp)
client.register_callback_query_handler(dp)
new_task.register_new_task_query_handler(dp)
new_task.register_handler_new_task(dp)
delete_task.register_delete_task_query_handler(dp)
delete_task.register_handler_delete_task(dp)
history.register_history_query_handler(dp)
admin.register_handler_admin(dp)
other.register_handler_other(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
