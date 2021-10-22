# from data_base import sqlite_db
import sqlite3 as sq
# import datetime
import json
# import os


def sql_add_stations(data):
    for item in data:
        station_rus = item['station_rus']
        station_lat = item['station_lat']
        description = item['description']
        add_data = (station_rus, station_lat, description)
        cur.execute('INSERT INTO stations (station_rus, station_lat, description) VALUES (?, ?, ?)', tuple(add_data))
    base.commit()


# db_path = os.chdir("../")
base = sq.connect('../rtrs.db')
cur = base.cursor()

with open('fixtures/stations.json', 'r', encoding='utf-8') as f:
    data = json.loads(f.read())
sql_add_stations(data['stations'])
# db_path = os.chdir("../data_base")
