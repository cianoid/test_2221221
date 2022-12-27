import requests

API_URL = "http://10.23.10.67:9201/extraction_inf"


if __name__ == "__main__":
    data = {
        "user_name": "Ivan Ivanov",
        "data_type": "AG_INF",
    }
    result = requests.post(API_URL, json=data)

    print(result.raw)
