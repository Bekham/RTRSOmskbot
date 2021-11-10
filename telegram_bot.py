from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db
from handlers import start, client, admin, other, new_task, history, delete_task, restore_task, full_delete_task, \
    mobility
import asyncio
from datetime import datetime
from parse import mobility_parse
PARSE_TIME_HOURS = 1/2
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
full_delete_task.register_full_delete_task_query_handler(dp)
full_delete_task.register_handler_full_delete_task(dp)
restore_task.register_restore_task_query_handler(dp)
restore_task.register_handler_restore_task(dp)
mobility.mobility_callback_query_handler(dp)
admin.admin_handler_start(dp)
admin.admin_callback_query_handler(dp)
other.register_handler_other(dp)


async def scheduled(wait_for):
  while True:
    await asyncio.sleep(wait_for)
    await mobility_parse.mobility_tasks()
    print('Парсинг мобилити')


if __name__ == '__main__':
  loop = asyncio.get_event_loop()
  loop.create_task(scheduled(PARSE_TIME_HOURS*60*60))
  executor.start_polling(dp, skip_updates=True, on_startup=on_startup)