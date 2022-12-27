import json
import os
from datetime import datetime
from typing import List, Union
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from requests.sessions import Session

load_dotenv()

SITE_LOGIN = os.environ.get("SITE_LOGIN")
SITE_PASSWORD = os.environ.get("SITE_PASSWORD")
URL_LOGIN = "https://фундучок.рф/lichnyj-kabinet/"
URL_ORDERS = "https://фундучок.рф/lichnyj-kabinet/zakazy/"
SITE_BASE = "https://фундучок.рф/"
DATE_FORMAT = "%d.%m.%Y %H:%M"


def authenthicate(session: Session) -> bool:
    # Запрос страницы логина
    login_page = session.get(URL_LOGIN)
    soup = BeautifulSoup(login_page.text, features="lxml")

    # Поиск тегов script, так как в одном из них находится csrf-токен и другая
    # информация для аутентификации
    scripts = soup.findAll("script")

    csrf = None
    page_id = None
    action_url = None

    # Проход по всем тегам в поисках нужного контента
    for script in scripts:
        if "OfficeConfig=" in script.text:
            # Контент найден, очистим от лишних данных и преобразуем в объект
            office_config = script.text.split("OfficeConfig=")
            json_str = office_config[1][::-1].replace(";", "")[::-1]
            json_obj = json.loads(json_str)

            # Получим нужные значения
            action_url = json_obj["actionUrl"]
            csrf = json_obj["csrf"]
            page_id = json_obj["pageId"]

    # Если ничего не нашли, то завершим работу
    if csrf is None:
        return False

    # Из формы вытянем другие необходимые данные
    form = soup.find("form", attrs={"id": "office-auth-login"})
    input_action = form.find("input", attrs={"name": "action"})["value"]
    input_return = form.find("input", attrs={"name": "return"})["value"]

    # Сформируем словарь с данными для аутентификации
    data = {
        "action": input_action,
        "return": input_return,
        "email": SITE_LOGIN,
        "password": SITE_PASSWORD,
        "pageId": page_id,
        "csrf": csrf
    }
    login_url = urljoin(SITE_BASE, action_url)

    # Совершим вход в личный кабинет
    result = session.post(login_url, data=data)
    return result.status_code == 200


def parse_table(session: Session, url: str, table_class: str) -> Union[bool, List]:
    orders_page = session.get(url)

    if orders_page.status_code != 200:
        return False

    soup = BeautifulSoup(orders_page.text, features='lxml')
    orders_table = soup.find("table", attrs={"class": table_class})

    thead = orders_table.find_all("th")
    header = [item.text.strip() for item in thead]

    data = []
    tbody = orders_table.find("tbody")
    rows = tbody.find_all("tr")

    for row in rows:
        item = dict()
        cells = row.find_all("td")
        for count, cell in enumerate(cells):
            cell_text = cell.text.strip()

            if count == 0:
                cell_text = datetime.strptime(cell_text, DATE_FORMAT)

            item[header[count]] = cell_text
        data.append(item)

    return data


def run():
    sess = requests.Session()

    if not authenthicate(sess):
        print("Login failed")
        quit()

    print(parse_table(sess, URL_ORDERS, "table--orders--lk"))


if __name__ == "__main__":
    run()
