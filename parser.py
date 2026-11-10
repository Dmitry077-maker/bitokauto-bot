import requests
import json

API_URL = "https://bitokauto-bot-372810.onrender.com/api/add-car"
ADMIN_SECRET = "super_secret_key_123"

COPART_SEARCH_URL = "https://www.copart.com/public/lots/search"

def fetch_copart_cars():
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1",
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*"
    }
    
    # Запрос к API Copart: ищем популярные тачки (Ford, BMW, Audi, Dodge, Tesla)
    payload = {
        "query": ["Ford", "BMW", "Audi", "Dodge", "Tesla"],
        "filter": {},
        "page": 0,
        "size": 10,
        "sort": ["sale_date desc"]
    }

    cars = []
    print("🚀 Тянем реальные лоты с API Copart...")

    try:
        res = requests.post(COPART_SEARCH_URL, json=payload, headers=headers, timeout=15)
        if res.status_code != 200:
            print(f"❌ Copart вернул ошибку: {res.status_code}")
            return []

        data = res.json()
        results = data.get("data", {}).get("results", {}).get("content", [])

        for item in results:
            # Вытягиваем реальные поля Copart
            lot_number = item.get("ln")
            make = item.get("mfr", "").capitalize()
            model = item.get("mld", "")
            year = item.get("lcy", "")
            title = f"{year} {make} {model}".strip()
            
            price = float(item.get("hb", 0) or 5000.0)
            vin = item.get("fv", f"COPART{lot_number}")
            location = f"Copart ({item.get('yn', 'USA')})"
            mileage = f"{item.get('orr', 0):,} mi"
            damage = item.get("dd", "Основне пошкодження")
            
            # Формируем ссылку на фотку лота Copart
            image_url = item.get("fullThumbnailUrl") or f"https://cs.copart.com/v1/AUTH_svc.copart.images/ImageProcessing/{lot_number}_1X.JPG"

            cars.append({
                "title": title if title else "Copart Vehicle",
                "price_usd": price,
                "vin": vin,
                "location": location,
                "mileage": mileage,
                "damage": damage,
                "image_url": image_url,
                "source": "Copart"
            })
            
    except Exception as e:
        print(f"💥 Ошибка при подключении к Copart: {e}")

    return cars

def upload_to_db(cars):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "x-secret": ADMIN_SECRET
    }
    for car in cars:
        try:
            r = requests.post(API_URL, json=car, headers=headers)
            if r.status_code == 200:
                print(f"✅ Добавлен реальный лот Copart: {car['title']} (VIN: {car['vin']})")
            else:
                print(f"❌ Ошибка отправки: {r.text}")
        except Exception as e:
            print(f"💥 Сбой бэкенда: {e}")

if __name__ == "__main__":
    copart_cars = fetch_copart_cars()
    if copart_cars:
        upload_to_db(copart_cars)
    else:
        print("⚠️ Не удалось получить список лотов. Запустим повторно.")
