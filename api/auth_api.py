import requests
import json
from bs4 import BeautifulSoup
import re

AUTH_URL = "https://users.sfu-kras.ru/php/auth.php"
GROUPS_URL = "https://edu.sfu-kras.ru/api/timetable/groups/"
LOGOUT_URL = "https://users.sfu-kras.ru/php/logout.php"
GET_INFO_URL = "https://users.sfu-kras.ru/php/login_info.php"
COOKIE = "PHPSESSID=dfmjd8vtbvmn0j4r84dsfh8fi8"


def registration_api(login, password, is_staff=False, **extra_fields):
    """
        Проверка пользователя через сайт "Мой СФУ"
        Получение данных о пользователе через сайт
    """

    headers = {'Cookie': COOKIE}
    requests.request("POST", LOGOUT_URL, headers=headers, data={}, verify=False)
    response = requests.request("POST", AUTH_URL, headers=headers,
                                data={'login': login, 'password': password}, verify=False)

    if response.status_code == 200 and json.loads(response.text).get('data') == 'SUCCESS':
        response = requests.request("GET", GET_INFO_URL, headers=headers, verify=False)
        if response.status_code == 200 and response.text.find('http-equiv="refresh"') == -1:
            soup = BeautifulSoup(response.text, 'html.parser')
            fio = soup.find("div", class_='fioview').text.split(' ')
            student = False
            group = ''
            for tr in soup.find_all("tr"):
                if tr.text.find('Должность') != -1 and tr.find_all('td')[1].text == 'Студент':
                    student = True
                if tr.text.find('Группа') != -1:
                    group = tr.find_all('td')[1].text
            if is_staff and student:
                return False, 'Вы не являетесь преподавателем'
            elif is_staff and not student:
                return True, {'surname': fio[0], 'first_name': fio[1], 'patronymic': fio[2]}
            elif not is_staff and not student:
                return False, 'Вы не являетесь студентом'
            elif not is_staff and student:
                return True, {'surname': fio[0], 'first_name': fio[1], 'patronymic': fio[2], 'group': group}
    return False, 'Неверный логин или пароль'


def check_api(login, password, is_staff=False, **extra_fields):
    """
        Проверка пользователя через сайт "Мой СФУ"
        Получение данных о пользователе через сайт
    """

    headers = {'Cookie': COOKIE}
    requests.request("POST", LOGOUT_URL, headers=headers, data={}, verify=False)
    response = requests.request("POST", AUTH_URL, headers=headers,
                                data={'login': login, 'password': password}, verify=False)

    if response.status_code == 200 and json.loads(response.text).get('data') == 'SUCCESS':
        response = requests.request("GET", GET_INFO_URL, headers=headers, verify=False)
        if response.status_code == 200 and response.text.find('http-equiv="refresh"') == -1:
            soup = BeautifulSoup(response.text, 'html.parser')
            student = False
            for tr in soup.find_all("tr"):
                if tr.text.find('Должность') != -1 and tr.find_all('td')[1].text == 'Студент':
                    student = True
            if is_staff and student:
                return False, 'Вы не являетесь преподавателем'
            elif is_staff and not student:
                return True, {'surname': fio[0], 'first_name': fio[1], 'patronymic': fio[2]}
            elif not is_staff and not student:
                return False, 'Вы не являетесь студентом'
            elif not is_staff and student:
                return True, {'surname': fio[0], 'first_name': fio[1], 'patronymic': fio[2], 'group': group}
    return False, 'Неверный логин или пароль'


def get_subgroups_from_group(group):
    headers = {'Cookie': COOKIE}
    response = requests.request("GET", GROUPS_URL, headers=headers)
    group_objects = []
    if response.status_code == 200:
        data = json.loads(response.text)
        try:
            for item in data:
                re_group = re.search(r"([^\s()]+)(?:\s\(([^()]*)\))?", item.get('name'))
                if re_group:
                    row_group = re_group.groups()
                    if row_group[0].upper() == group.upper():
                        subgroup = row_group[1]
                        # if subgroup is not None:
                        #     subgroup = subgroup.split(' ')
                        #     subgroup.reverse()
                        #     subgroup = ' '.join(subgroup)
                        group_objects.append({'name': row_group[0].upper(), 'subgroup': subgroup})
                    elif row_group[0].upper() != group.upper() and len(group_objects):
                        group_objects.reverse()
                        return 200, group_objects
        except:
            pass
    return 500, 'Группа не найдена'
