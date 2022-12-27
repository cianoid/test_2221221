import os

import oracledb
from dotenv import load_dotenv

# Загрузка значение из файла .env
load_dotenv()


DB_IP = os.environ.get("DB_IP")
DB_PORT = os.environ.get("DB_PORT")
DB_SERVICE_NAME = os.environ.get("DB_SERVICE_NAME")
DB_LOGIN = os.environ.get("DB_LOGIN")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_SCHEME = os.environ.get("DB_SCHEME")

DSN = f"{DB_IP}:{DB_PORT}/{DB_SCHEME}"

# Подключение к БД
con = oracledb.connect(
    user=DB_LOGIN,
    password=DB_PASSWORD,
    dsn=DSN,
    service_name=DB_SERVICE_NAME)

cursor = con.cursor()

# Запрос данных
data = cursor.execute("SELECT * FROM clients LIMIT 5;")

# Вывод данных
for row in data:
    print(row)
