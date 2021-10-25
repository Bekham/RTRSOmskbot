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
    create_stations_db()
    base.commit()


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


def find_user(user_id):
    try:
        sqlite_select_query = "SELECT * FROM users WHERE user_id=?"
        records = cur.execute(sqlite_select_query, (user_id,)).fetchall()
        return records
    except:
        return None
