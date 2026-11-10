<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BitokAuto.ua — Каталог авто</title>
    <script src="https://telegram.org/js/telegram-web-app.js"></script>
    <style>
        :root {
            --bg-color: #0f0f0f;
            --card-bg: #1a1a1a;
            --text-color: #f3f3f3;
            --text-secondary: #aaaaaa;
            --accent-color: #ffffff;
            --border-color: #333333;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            margin: 0;
            padding: 16px;
        }
        h1 {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 4px;
            letter-spacing: -0.5px;
        }
        .subtitle {
            color: var(--text-secondary);
            font-size: 14px;
            margin-bottom: 20px;
        }
        .cars-grid {
            display: flex;
            flex-direction: column;
            gap: 16px;
        }
        .car-card {
            background-color: var(--card-bg);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
        }
        .car-img {
            width: 100%;
            height: 180px;
            object-fit: cover;
            background-color: #222;
        }
        .car-content {
            padding: 14px;
        }
        .car-title {
            font-size: 16px;
            font-weight: 600;
            margin-bottom: 8px;
            color: var(--accent-color);
        }
        .car-price {
            font-size: 18px;
            font-weight: 700;
            color: #4cd964;
            margin-bottom: 10px;
        }
        .car-info {
            display: flex;
            justify-content: space-between;
            font-size: 13px;
            color: var(--text-secondary);
            margin-bottom: 6px;
        }
        .car-damage {
            font-size: 13px;
            color: #ff9500;
            margin-top: 6px;
            font-weight: 500;
        }
        .empty-state {
            text-align: center;
            color: var(--text-secondary);
            margin-top: 40px;
            font-size: 15px;
        }
    </style>
</head>
<body>

    <h1>BitokAuto.ua</h1>
    <div class="subtitle">Свіжі лоти зі США та Європи</div>

    <div id="cars-container" class="cars-grid">
        <div class="empty-state">Завантаження каталогів...</div>
    </div>

    <script>
        // Инициализация Telegram WebApp
        const tg = window.Telegram.WebApp;
        tg.expand();

        async function loadCars() {
            try {
                const response = await fetch('/api/cars');
                const cars = await response.json();
                
                const container = document.getElementById('cars-container');
                
                if (cars.length === 0) {
                    container.innerHTML = '<div class="empty-state">Наразі каталог порожній. Очікуємо надходження лотів!</div>';
                    return;
                }

                container.innerHTML = '';
                cars.forEach(car => {
                    const card = document.createElement('div');
                    card.className = 'car-card';
                    card.innerHTML = `
                        <img src="${car.image_url || 'https://via.placeholder.com/400x250'}" class="car-img" alt="${car.title}">
                        <div class="car-content">
                            <div class="car-title">${car.title}</div>
                            <div class="car-price">$${car.price_usd.toLocaleString()}</div>
                            <div class="car-info">
                                <span>📍 ${car.location}</span>
                                <span>🛣️ ${car.mileage}</span>
                            </div>
                            <div class="car-damage">⚠️ Пошкодження: ${car.damage}</div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            } catch (err) {
                console.error(err);
                document.getElementById('cars-container').innerHTML = '<div class="empty-state">Помилка завантаження каталогу.</div>';
            }
        }

        loadCars();
    </script>
</body>
</html>
