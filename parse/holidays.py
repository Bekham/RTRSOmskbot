import json
import requests


def find_holiday(date):
    year = date.split('-')[0]
    url = 'https://raw.githubusercontent.com/d10xa/holidays-calendar/master/json/consultant' + year + '.json'
    r = requests.get(url)
    cal = json.loads(r.text)
    return cal["holidays"].count(date)
