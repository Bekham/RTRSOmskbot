import json
import sqlite3
import sqlite3 as sq
import datetime
from handlers import new_task

# from create_bot import bot
from parse import holidays


def sql_start():
    global base, cur
    base = sq.connect('rtrs_omsk.db')
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
    base.execute("""CREATE TABLE IF NOT EXISTS 'trips'(
                         id INTEGER PRIMARY KEY,
                         trip_station TEXT,
                         trip_creator INTEGER,
                         trip_worker INTEGER,
                         trip_date TEXT, 
                         trip_desc TEXT,
                         createDate timestamp,
                         is_visible BOOL,
                         addition TEXT
                         )""")
    try:
        base.execute("alter table 'trips' add column '%s' 'integer'" % 'sunday')
    except sqlite3.OperationalError:
        pass
    add_data_table_stations()
    create_stations_db()
    add_first_admin()
    # load_data_users()
    add_user_id_users()
    base.commit()




def add_user_id_users():
    users = sql_read_all_user()
    for user in users:
        if user[8] == None:
            chat_id = user[1]
            user_id = user[1]
            try:
                cur.execute('''UPDATE 'users' SET chat_id = ? WHERE user_id = ?''', (chat_id, user_id))
                base.commit()
            except:
                pass


def add_data_table_stations():
    stations = sql_read_all_stations()
    if len(stations) == 0:
        with open('data_base/fixtures/stations.json', 'r', encoding='utf-8') as f:
            data = json.loads(f.read())
            # print(data)
            for item in data['stations']:
                # print(item)
                station_rus = item['station_rus']
                station_lat = item['station_lat']
                description = item['description']
                add_data = (station_rus, station_lat, description)
                cur.execute('INSERT INTO stations (station_rus, station_lat, description) VALUES (?, ?, ?)',
                            tuple(add_data))
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

def sql_find_name_station_trips(stations_lat):
    try:
        stations = stations_lat.split('_')
        stations_rus = ''
        for station_lat in stations:
            try:
                sqlite_select_query = """SELECT station_rus FROM stations WHERE station_lat=?"""
                station_rus = cur.execute(sqlite_select_query, (station_lat,)).fetchall()
                stations_rus += f', {station_rus[0][0]}'
            except:
                return None
        return stations_rus[2:]
    except:
        try:
            sqlite_select_query = """SELECT station_rus FROM stations WHERE station_lat=?"""
            station_rus = cur.execute(sqlite_select_query, (stations_lat,)).fetchall()
            return station_rus[0][0]
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

def sql_find_all_task_by_user_id (user_id):
    try:
        all_stations = sql_read_all_stations()
        create_tasks = 0
        close_tasks = 0
        for station in all_stations:
            station_tasks = sql_read_station(station[2])
            if station_tasks:
                for task in station_tasks:
                    user_create = task[2]
                    user_update = task[3]
                    is_active = task[6]
                    if user_create == user_id:
                        create_tasks += 1
                    if user_update == user_id and not is_active:
                        close_tasks += 1
        return (create_tasks, close_tasks)
    except Exception:
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

def add_first_admin():
    users = sql_read_all_user()
    if len(users) == 0:
        user_name = 'Антон'
        first_name = 'Антон'
        last_name = 'Беккер'
        user_id = 1650562601
        createDate = datetime.datetime.now()
        lastVisitDate = datetime.datetime.now()
        is_admin = 1
        user_data = (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin)
        cur.execute(
            """INSERT INTO 'users' (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin) VALUES (?, ?, ?, ?, ?, ?, ?)""",
            user_data)
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


async def sql_add_new_user(state, user_id, is_admin=0):
    async with state.proxy() as data:
        user_name = data.get('first_name').title()
        first_name = data.get('first_name').title()
        last_name = data.get('last_name').title()
    user_id = user_id
    createDate = datetime.datetime.now()
    lastVisitDate = datetime.datetime.now()
    chat_id = user_id
    user_data = (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin, chat_id)
    cur.execute(
        """INSERT INTO 'users' (user_id, user_name, createDate, lastVisitDate, first_name, last_name, is_admin, chat_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
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

def sql_update_user_visit(user_id):
    try:
        cur.execute('''UPDATE 'users' SET lastVisitDate = ? WHERE user_id = ?''', (datetime.datetime.now(), user_id))
        base.commit()
    except:
        pass

def sql_admin_update_user(user_pk, fields):
    for key, item in fields.items():

        try:

            user_data = (str(item), int(user_pk))

            if key == 'Имя':
                print('Name')
                cur.execute('''UPDATE 'users' SET first_name = ? WHERE id = ?''', (user_data))
            elif key == 'Фамилия':
                cur.execute('''UPDATE 'users' SET last_name = ? WHERE id = ?''', (user_data))
            elif key == 'Admin':
                cur.execute('''UPDATE 'users' SET is_admin = ? WHERE id = ?''', (user_data))
            else:
                return False
            base.commit()
            return True
        except:
            return False






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
            sqlite_select_query_task_num = """SELECT * FROM mobility_tasks WHERE task_num=?"""
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
            sqlite_select_query = """INSERT INTO mobility_tasks (task_num, task_station, task_type, task_desc, task_date, createDate, is_visible) VALUES (?, ?, ?, ?, ?, ?, ?)"""
            try:
                cur.execute(sqlite_select_query, new_task_data)
                base.commit()
            except:
                pass
            if tasks[task_num]['_type'].startswith('Плановое') \
                    or tasks[task_num]['_task_status'].startswith('оценкавыставлена')\
                    or tasks[task_num]['_task_status'].startswith('выполнено'):
                # print(tasks[task_num])
                pass
            else:
                # print('Alarma',tasks[task_num])
                await new_task.new_task_mobility(task=tasks[task_num])

async def sql_find_old_mobility_task(tasks):
    try:
        sqlite_select_query_task_num = """SELECT * FROM mobility_tasks"""
        records = cur.execute(sqlite_select_query_task_num).fetchall()
    except:
        records = None
    for record in records:
        if record[1] not in tasks.keys():
            is_visible = 0
            try:
                cur.execute('''DELETE FROM mobility_tasks WHERE task_num = ?''', (record[1],))
                base.commit()

            except:
                pass
        for task_num in tasks.keys():
            # print(tasks[task_num], record[1])
            # if task_num == record[1]:
            #     print(task_num, record[1], tasks[task_num]['_task_status'].startswith('оценкавыставлена'), tasks[task_num]['_task_status'].startswith('выполнено'))
            if task_num == record[1] and (tasks[task_num]['_task_status'].startswith('оценкавыставлена')
                                                 or tasks[task_num]['_task_status'].startswith('выполнено')):
                is_visible = 0
                try:
                    cur.execute('''UPDATE mobility_tasks SET is_visible = ? WHERE task_num = ?''',
                                (is_visible, record[1]))
                    base.commit()

                except:
                    pass


def sql_read_all_mobility():
    try:
        sqlite_select_query = """SELECT * FROM mobility_tasks"""
        records = cur.execute(sqlite_select_query).fetchall()
        return records
    except:
        return None


def load_data_trips(trip):
    try:
        all_worker_trips = read_data_trips(trip['trip_worker'])
        stations = trip['trip_station'].split('_')
        for trip_db in all_worker_trips:
            trip_date = trip_db[4]
            if trip_date == str(trip['trip_date']):
                for station in stations:
                    if station in trip_db[1].split('_'):
                        return False
        trip_data = (trip['trip_station'],
                     trip['trip_creator'],
                     trip['trip_worker'],
                     trip['trip_date'],
                     trip['trip_desc'],
                     datetime.datetime.now(),
                     trip['trip_days'],
                     1,
                     trip['holi_days'])

        cur.execute(
            """INSERT INTO 'trips' (
                trip_station, 
                trip_creator, 
                trip_worker, 
                trip_date, 
                trip_desc, 
                createDate,
                addition, 
                is_visible,
                sunday) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", trip_data)
        base.commit()
        return True
    except Exception:
        return False

def read_data_trips(user_id=None):
    if user_id:
        try:
            sqlite_select_query = """SELECT * FROM 'trips' WHERE trip_worker=?"""
            trips_user = cur.execute(sqlite_select_query, (user_id,)).fetchall()
            return trips_user
        except Exception:
            return False
    else:
        try:
            sqlite_select_query = """SELECT * FROM 'trips'"""
            trips_user = cur.execute(sqlite_select_query).fetchall()
            return trips_user
        except Exception:
            return False

async def sql_delete_trip(state, is_active=0):
    async with state.proxy() as data:
        id = int(data.get('num_del'))
    column_values = (is_active, id)
    try:
        sqlite_update_query = "UPDATE 'trips' SET is_visible = ? WHERE id = ?"
        cur.execute(sqlite_update_query, column_values)
        base.commit()
        return True
    except:
        return False

def sql_find_all_trips_count_by_user_id (user_id):
    try:
        all_trips = read_data_trips(user_id)
        count = 0
        if len(all_trips):
            for trip in all_trips:
                if trip[7]:
                    count += 1
        return count

    except Exception:
        return 0
