import sqlite3 as sq
import datetime
from handlers import new_task

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
                 is_admin BOOL,
                 chat_id INTEGER)""")
    base.execute("""CREATE TABLE IF NOT EXISTS 'mobility_tasks'(
                     id INTEGER PRIMARY KEY, 
                     task_num TEXT NOT NULL,
                     task_station TEXT,
                     task_type TEXT,
                     task_desc TEXT,
                     task_date TEXT, 
                     createDate timestamp,
                     is_visible BOOL,
                     addition INTEGER)""")
    create_stations_db()
    # load_data_users()
    base.commit()

def load_data_users():
    users = sql_read_all_user()
    for user in users:
        user_id = user[1]
        user_name = user[2]
        createDate = user[3]
        lastVisitDate = user[4]
        first_name = user[5]
        last_name = user[6]
        is_admin = user[7]
        user_data = (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin)
        cur.execute(
            """INSERT INTO users (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            user_data)
        base.commit()
        print(user)


def create_stations_db():
    stations = sql_read_all_stations()
    if stations:
        for station in stations:
            # base.execute('DROP TABLE ' + station[2])
            base.execute('CREATE TABLE IF NOT EXISTS '
                         + station[2] +
                         '(id INTEGER PRIMARY KEY, '
                         'description TEXT, '
                         'userCreate INTEGER, '
                         'userUpdate INTEGER, '
                         'createDate timestamp, '
                         'updateDate timestamp, '
                         'is_active BOOL'
                         ')')


def sql_read_all_stations():
    try:
        sqlite_select_query = """SELECT * FROM stations"""
        records = cur.execute(sqlite_select_query).fetchall()
        return records
    except:
        return None

def sql_find_name_station(station_lat):
    try:
        sqlite_select_query = """SELECT station_rus FROM stations WHERE station_lat=?"""
        station_rus = cur.execute(sqlite_select_query, (station_lat,)).fetchall()
        return station_rus
    except:
        return None


def sql_read_station(station):
    try:
        sqlite_select_query = 'SELECT * FROM ' + station
        records = cur.execute(sqlite_select_query).fetchall()
        return records
    except:
        return None


async def sql_add_new_task(state, user_id, is_active=1):
    async with state.proxy() as data:
        station = data.get('station')
        description = data.get('description')
    userCreate = user_id
    userUpdate = user_id
    createDate = datetime.datetime.now()
    updateDate = datetime.datetime.now()
    new_task_data = (description, userCreate, userUpdate, createDate, updateDate, is_active)
    sqlite_select_query = "INSERT INTO " + station + " (description, userCreate, userUpdate, createDate, updateDate, is_active) VALUES (?, ?, ?, ?, ?, ?)"
    try:
        cur.execute(sqlite_select_query, new_task_data)
        base.commit()
        return True
    except:
        return False


async def sql_delete_task(state, user_id, is_active=0):
    async with state.proxy() as data:
        station = data.get('station')
        id = data.get('num_del')
    data_station = sql_read_station(station)
    for data in data_station:
        try:
            if data[0] == int(id):
                userUpdate = user_id
                updateDate = datetime.datetime.now()
                column_values = (userUpdate, updateDate, is_active, id)
                try:
                    sqlite_update_query = "UPDATE " + station + " SET userUpdate = ?, updateDate = ?, is_active = ? WHERE id = ?"
                    cur.execute(sqlite_update_query, column_values)
                    base.commit()
                    return True
                except:
                    return False
        except:
            return False

async def sql_restore_task(state, user_id, is_active=1):
    async with state.proxy() as data:
        station = data.get('station')
        id = data.get('restores_task')
    userUpdate = user_id
    updateDate = datetime.datetime.now()
    column_values = (userUpdate, updateDate, is_active, id)
    try:
        sqlite_update_query = "UPDATE " + station + " SET userUpdate = ?, updateDate = ?, is_active = ? WHERE id = ?"
        cur.execute(sqlite_update_query, column_values)
        base.commit()
        return True
    except:
        return False

async def sql_full_delete_task(station, id):
    # async with state.proxy() as data:
    #     station = data.get('station')
    #     id = data.get('full_delete_task')
    try:
        sqlite_update_query = "DELETE FROM " + station + " WHERE id = ?"
        cur.execute(sqlite_update_query, (id,))
        base.commit()
        return True
    except:
        return False

async def sql_add_new_user(state, user_id, is_admin=0):
    async with state.proxy() as data:
        user_name = data.get('first_name').title()
        first_name = data.get('first_name').title()
        last_name = data.get('last_name').title()
    user_id = user_id
    createDate = datetime.datetime.now()
    lastVisitDate = datetime.datetime.now()
    user_data = (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin)
    cur.execute(
        """INSERT INTO 'users' (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        user_data)
    base.commit()


def sql_read_user(user_id):
    try:
        sqlite_select_query = """SELECT * FROM users"""
        records = cur.execute(sqlite_select_query).fetchall()
        for row in records:
            if user_id == row[1]:
                return row
    except:
        return None

def sql_read_all_user():
    try:
        sqlite_select_query = """SELECT * FROM users"""
        records = cur.execute(sqlite_select_query).fetchall()
        return records
    except:
        return None


def sql_update_user(user_id, username):
    try:
        cur.execute('''UPDATE 'users' SET user_name = ? WHERE user_id = ?''', (username, user_id))
        cur.execute('''UPDATE 'users' SET lastVisitDate = ? WHERE user_id = ?''', (datetime.datetime.now(), user_id))
        base.commit()

    except:
        pass


def sql_update_date_user(user_id):
    try:
        cur.execute('''UPDATE 'users' SET lastVisitDate = ? WHERE user_id = ?''', (datetime.datetime.now(), user_id))
        base.commit()
    except:
        pass


def find_user(user_id):
    try:
        sqlite_select_query = "SELECT * FROM users WHERE user_id=?"
        records = cur.execute(sqlite_select_query, (user_id,)).fetchall()
        return records
    except:
        return None

def user_is_admin(user_id):
    try:
        sqlite_select_query = "SELECT is_admin FROM users WHERE user_id=?"
        records = cur.execute(sqlite_select_query, (user_id,)).fetchall()

        return records[0][0]
    except:
        return False

def sql_update_user_chat_id(user_id, chat_id):
    try:
        cur.execute('''UPDATE users SET chat_id = ? WHERE user_id = ?''', (chat_id, user_id))
        base.commit()
        return True
    except:
        return False


async def sql_add_new_mobility_task(tasks):
    for task_num in tasks.keys():
        try:
            sqlite_select_query_task_num = "SELECT * FROM mobility_tasks WHERE task_num=?"
            records = cur.execute(sqlite_select_query_task_num, (task_num,)).fetchall()

        except:
            records = None
        # print('test sql mobility', records)
        if records == []:
            task_station = tasks[task_num]['_station']
            task_type = tasks[task_num]['_type']
            task_desc = tasks[task_num]['_desc']
            task_date = tasks[task_num]['_date']
            createDate = datetime.datetime.now()
            is_visible = 1
            new_task_data = (task_num, task_station, task_type, task_desc, task_date, createDate, is_visible)
            sqlite_select_query = "INSERT IF EXISTS INTO mobility_tasks (task_num, task_station, task_type, task_desc, task_date, createDate, is_visible) VALUES (?, ?, ?, ?, ?, ?, ?)"
            try:
                cur.execute(sqlite_select_query, new_task_data)
                base.commit()


            except:
                pass
            await new_task.new_task_mobility(task=tasks[task_num])