import re
from data_base import sqlite_db
import requests
from bs4 import BeautifulSoup

async def mobility_tasks():
    url = 'https://mobility.rtrn.ru/rtrn/cp/req/req_result'

    # Важно. По умолчанию requests отправляет вот такой
    # заголовок 'User-Agent': 'python-requests/2.22.0 ,  а это приводит к тому , что Nginx
    # отправляет 404 ответ. Поэтому нам нужно сообщить серверу, что запрос идет от браузера

    user_agent_val = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/95.0.4638.69 Safari/537.36'

    # Создаем сессию и указываем ему наш user-agent
    session = requests.Session()
    r = session.get(url, headers = {
        'User-Agent': user_agent_val
    })

    # Указываем referer. Иногда , если не указать , то приводит к ошибкам.
    session.headers.update({'Referer':url})

    #Хотя , мы ранее указывали наш user-agent и запрос удачно прошел и вернул
    # нам нужный ответ, но user-agent изменился на тот , который был
    # по умолчанию. И поэтому мы обновляем его.
    session.headers.update({'User-Agent':user_agent_val})

    # Получаем значение _xsrf из cookies
    # _xsrf = session.cookies.get('_xsrf', domain=".atrium-omsk.ru")
    login_submit_button = session.cookies.get('login_submit_button', domain=".rtrn.ru")
    # print(login_submit_button)

    # Осуществляем вход с помощью метода POST с указанием необходимых данных
    post_request = session.post(url, {
         'time_zone_offset': '-360',
         'requested_url': 'https://mobility.rtrn.ru/rtrn/cp/',
         'userLogin': 'abekker',
         'userPassword': 'Medvedevmydak2021',
         # '_xsrf':_xsrf,
         # 'login_submit_button':'yes',
    })
    soup = BeautifulSoup(post_request.text, 'lxml')
    task_num = soup.find_all('p', class_='num')
    task_station = soup.find_all('p', class_='mt-5 l-4xs')
    task_type = soup.find_all('td', class_=re.compile("^table__cell work-td"))
    task_desc = soup.find_all('div', class_='link link_style_6 l-4s bold')
    task_date = soup.find_all('td', class_='table__cell wp-120')
    tasks = {}
    # print(task_type)
    for i in range(len(task_num)):
    # for num in task_num:
        _num = task_num[i].text.replace('	', '').replace('\n','')
        _station = task_station[i].text.replace('	', '').replace('\n', '')
        _type = task_type[i].text.replace('	', '').replace('\n','').replace('приоритет:',' ')
        _desc = task_desc[i].text.replace('	', '').replace('\n','')
        _date = task_date[i].text.replace('	', '').replace('\n','').replace(' ','').replace(',','').replace('\xa0',' ')[:16]
        # print(num, type, desc, date)
        tasks[_num] = {
            '_station': _station,
            '_type': _type,
            '_desc': _desc,
            '_date': _date
        }

    if tasks:
        print('Скачано с сайта')
        await sqlite_db.sql_add_new_mobility_task(tasks)
    #     # print(task_num[i].text.replace('	', '').replace('\n',''))
    # print(tasks)
    # print(task_type)
    # print(task_desc)
    # print(task_date)
    #Вход  успешно воспроизведен и мы сохраняем страницу в html файл
    # with open("hh_success.html","w",encoding="utf-8") as f:
    #     f.write(post_request.text)