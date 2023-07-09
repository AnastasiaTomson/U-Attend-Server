import requests
import json
from bs4 import BeautifulSoup
import pandas as pd
import json
from datetime import datetime
import calendar
from django.utils import timezone
import time

GET_SCHEDULE_URL = "https://edu.sfu-kras.ru/api/timetable/get&target="
COOKIE = "SESS4b99abddd19aadf91f85ab66ce3493ff=ssr3oavc969o1uddkiha941lg7"

headers = {'Cookie': COOKIE}
WEEKDAY = {
    1: 'Пн',
    2: 'Вт',
    3: 'Ср',
    4: 'Чт',
    5: 'Пт',
    6: 'Сб',
    7: 'Вс',
}


def get_schedule(target):
    response = requests.request("GET", GET_SCHEDULE_URL + f'{target}')
    return json.loads(response.text)


# get_schedule('Кушнаренко А. В.')
# https://edu.sfu-kras.ru/api/timetable/get&target=КИ20-13б (2 подгруппа)КИ20-13б (2 подгруппа)

def get_week_num(day: int, month: int, year: int) -> int:
    calendar_ = calendar.TextCalendar(calendar.MONDAY)
    lines = calendar_.formatmonth(year, month).split('\n')
    days_by_week = [week.lstrip().split() for week in lines[2:]]
    str_day = str(day)
    for index, week in enumerate(days_by_week):
        if str_day in week:
            return index + 1
    raise ValueError(f'Нет дня с номером {day} в месяце с номером {month} в {year} году!')


def get_today_timetable(timetable):
    today_timetable = []
    now_date = datetime.now()
    
    # now_weekday = 5
    now_weekday = now_date.weekday() + 1
    event_week = 2 if get_week_num(now_date.day, now_date.month, now_date.year) % 2 == 0 else 1
    for table in timetable:
        if int(table.get('day')) == int(now_weekday) and int(table.get('week')) == int(event_week):
            table['weekday'] = WEEKDAY.get(int(table.get('day')))
            table['week'] = 'Нечетная неделя' if int(table.get('week')) == 1 else 'Четная неделя'
            table.pop('day')
            today_timetable.append(table)
    return today_timetable


def get_lesson_now(timetable):
    today_timetable = get_today_timetable(timetable)
    for today in today_timetable:
        start_time, end_time = today['time'].split('-')
        start_time = datetime.strptime(start_time, "%H:%M").time()
        end_time = datetime.strptime(end_time, "%H:%M").time()
        current = datetime.strptime('16:00', "%H:%M").time()
        # current = datetime.now().time()
        if start_time <= current <= end_time:
            return today
