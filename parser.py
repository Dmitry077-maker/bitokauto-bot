import requests

SERVER_URL = "https://bitokauto-bot-372810.onrender.com/api/add-car"
ADMIN_SECRET = "super_secret_key_123"

# Демо-функция сбора лотов (сюда вставим парсинг конкретного сайта)
def run_parser():
    test_cars = [
        {
            "title": "2022 Ford Mustang GT",
            "price_usd": 18500.0,
            "vin": "1FA6P8CF3M510XXXX",
            "location": "Copart (Texas)",
            "mileage": "28 тыс. миль",
            "damage": "Передний удар",
            "image_url": "https://via.placeholder.com/400x250",
            "source": "Copart"
        },
        {
            "title": "2020 BMW X5 xDrive40i",
            "price_usd": 24000.0,
            "vin": "5UXKR0C50L0XXXXXX",
            "location": "IAAI (Florida)",
            "mileage": "45 тыс. миль",
            "damage": "Боковой удар",
            "image_url": "https://via.placeholder.com/400x250",
            "source": "IAAI"
        }
    ]

    headers = {"x-secret": ADMIN_SECRET}

    for car in test_cars:
        response = requests.post(SERVER_URL, json=car, headers=headers)
        print(f"Отправка {car['title']}: Status {response.status_code}, Response: {response.json()}")

if __name__ == "__main__":
    run_parser()
