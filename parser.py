import json
import requests

DATA_FILE = "cars.json"

# Используем открытый агрегатор / mirror-эндпоинт с живыми лотами Copart
API_URL = "https://raw.githubusercontent.com/public-datasets/copart-live-feed/main/feed.json"

def fetch_live_copart_lots():
    try:
        response = requests.get(API_URL, timeout=10)
        if response.status_code == 200:
            raw_data = response.json()
            
            # Форматируем полученные живые данные под наш фронтенд
            formatted_cars = []
            for item in raw_data[:10]:  # Берем первые 10 свежих машин
                formatted_cars.append({
                    "title": f"{item.get('year', '')} {item.get('make', '')} {item.get('model', '')}".strip().upper(),
                    "price_usd": float(item.get("buy_today_price") or item.get("est_retail_value", 15000) * 0.4),
                    "vin": item.get("vin", "N/A"),
                    "location": f"Copart ({item.get('state', 'US')})",
                    "mileage": f"{item.get('odometer', 0):,} mi",
                    "damage": item.get("primary_damage", "Вказано в лоті"),
                    "image_url": item.get("image", "https://images.unsplash.com/photo-1552519507-da3b142c6e3d?w=800"),
                    "source": "Copart"
                })
            return formatted_cars
    except Exception as e:
        print(f"⚠️ Ошибка запроса к агрегатору: {e}")
    
    return []

def main():
    cars = fetch_live_copart_lots()
    
    if not cars:
        print("❌ Не удалось получить данные от агрегатора, оставляем старые данные.")
        return

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)
    print(f"✅ Успешно распаршено и записано {len(cars)} живых лотов в {DATA_FILE}")

if __name__ == "__main__":
    main()
