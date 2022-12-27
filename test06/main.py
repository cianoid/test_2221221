import os
import smtplib
from datetime import datetime, timedelta

import pandas
from dotenv import load_dotenv

load_dotenv()


EMAIL_HOST = os.environ.get("EMAIL_HOST")
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
EMAIL_SENDTO = os.environ.get("EMAIL_SENDTO")
EMAIL_PORT = 465
EMAIL_TIMEOUT = 10

DATE_FORMAT = "%Y-%m-%d"


def send_email(message):
    with smtplib.SMTP_SSL(EMAIL_HOST, EMAIL_PORT, timeout=EMAIL_TIMEOUT) as connection:
        connection.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        connection.sendmail(EMAIL_HOST_USER, EMAIL_SENDTO, message)
        connection.quit()


if __name__ == "__main__":
    df_original = pandas.read_excel("test.xlsx")

    yesterday = (datetime.now() - timedelta(days=1)).strftime(DATE_FORMAT)
    df_original["upd_date"] = pandas.to_datetime(
        df_original["upd_date"], format=DATE_FORMAT
    )
    df = df_original[(df_original["upd_date"] == yesterday)]

    send_email(df.to_string())
