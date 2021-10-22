import sqlite3 as sq
import datetime
# from create_bot import bot



def sql_start():
    global base, cur
    base = sq.connect('rtrs.db')
    cur = base.cursor()
    if base:
        print('Data base connected OK')

    base.execute("""CREATE TABLE IF NOT EXISTS stations(
                    id INTEGER PRIMARY KEY, 
                    station_rus TEXT, 
                    station_lat TEXT,
                    description TEXT)""")
    base.execute("""CREATE TABLE IF NOT EXISTS 'users'(
                    id INTEGER PRIMARY KEY, 
                 user_id INTEGER,
                 user_name TEXT NOT NULL,
                 createDate timestamp, 
                 lastVisitDate timestamp,
                 first_name TEXT,
                 last_name TEXT,
                 is_admin BOOL)""")
    base.commit()


#
# async def sql_read(message):
#     for ret in cur.execute('SELECT * FROM test').fetchall():
#         await bot.send_message(message.from_user.id, f'Название {ret[0]} \n Описание: {ret[1]} \n Цена: {ret[2]}')

async def sql_add_new_user(state, user_id, is_admin=0):
    async with state.proxy() as data:
        user_name = data.get('first_name').title()
        first_name = data.get('first_name').title()
        last_name = data.get('last_name').title()
    user_id = user_id
    createDate = datetime.datetime.now()
    lastVisitDate = datetime.datetime.now()
    user_data = (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin)
    cur.execute("""INSERT INTO 'users' (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)""", user_data)
    base.commit()

def sql_read_all_stations():
    try:
        sqlite_select_query = """SELECT * FROM stations"""
        records = cur.execute(sqlite_select_query).fetchall()
        return records
    except:
        return None

def sql_read_user(user_id):
    try:
        sqlite_select_query = """SELECT * FROM users"""
        records = cur.execute(sqlite_select_query).fetchall()
        for row in records:
            if user_id == row[1]:
                return row
    except:
        return None

def sql_update_user(user_id, username):
    try:
       cur.execute('''UPDATE 'users' SET user_name = ? WHERE user_id = ?''', (username, user_id))
       cur.execute('''UPDATE 'users' SET lastVisitDate = ? WHERE user_id = ?''', (datetime.datetime.now(), user_id))
    except:
        pass

def sql_update_date_user(user_id):
    try:
       cur.execute('''UPDATE 'users' SET lastVisitDate = ? WHERE user_id = ?''', (datetime.datetime.now(), user_id))
    except:
        pass


