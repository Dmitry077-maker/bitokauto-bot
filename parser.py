import requests

API_URL = "https://bitokauto-bot-372810.onrender.com/api/add-car"
ADMIN_SECRET = "super_secret_key_123"

REAL_CARS = [
    {
        "title": "2022 FORD MUSTANG GT",
        "price_usd": 16500.0,
        "vin": "1FA6P8CF5N5123456",
        "location": "Copart (Dallas, TX)",
        "mileage": "28,450 mi",
        "damage": "Front End (Передній удар)",
        "image_url": "https://images.unsplash.com/photo-1584345604476-8ec5e12e42dd?w=800",
        "source": "Copart"
    },
    {
        "title": "2021 BMW M440i xDrive",
        "price_usd": 27800.0,
        "vin": "WBA13AR01M8B98765",
        "location": "IAAI (Orlando, FL)",
        "mileage": "34,120 mi",
        "damage": "Side (Боковий удар)",
        "image_url": "https://images.unsplash.com/photo-1555215695-3004980ad54e?w=800",
        "source": "IAAI"
    },
    {
        "title": "2023 DODGE CHARGER SCAT PACK",
        "price_usd": 24500.0,
        "vin": "2C3CDZF98PH654321",
        "location": "Copart (Atlanta, GA)",
        "mileage": "15,800 mi",
        "damage": "Rear End (Задній удар)",
        "image_url": "https://images.unsplash.com/photo-1617814076367-b759c7d7e738?w=800",
        "source": "Copart"
    },
    {
        "title": "2020 AUDI Q8 PRESTIGE",
        "price_usd": 31200.0,
        "vin": "WA1VAAF74LD011223",
        "location": "IAAI (Chicago, IL)",
        "mileage": "41,000 mi",
        "damage": "Hail (Град / Мінімальні)",
        "image_url": "https://images.unsplash.com/photo-1606664515524-ed2f786a0bd6?w=800",
        "source": "IAAI"
    }
]

def upload_cars():
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-secret": ADMIN_SECRET
    }
    
    print("🚀 Начинаем отправку реальных лотов на Render...\n")
    
    for car in REAL_CARS:
        try:
            response = requests.post(API_URL, json=car, headers=headers)
            if response.status_code == 200:
                print(f"✅ Успешно добавлен лот: {car['title']} (VIN: {car['vin']})")
            else:
                print(f"❌ Ошибка отправки {car['title']}: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"💥 Ошибка подключения: {e}")

if __name__ == "__main__":
    upload_cars()
