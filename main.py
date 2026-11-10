import os
import json
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from aiogram.filters import Command

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = "https://bitokauto-bot-372810.onrender.com"
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "super_secret_key_123")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

DATA_FILE = "cars.json"

def load_cars():
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def save_cars(cars):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(cars, f, ensure_ascii=False, indent=4)

class CarItem(BaseModel):
    title: str
    price_usd: float
    vin: str
    location: str
    mileage: str
    damage: str
    image_url: str
    source: str

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Відкрити каталог", web_app=WebAppInfo(url=WEB_URL))],
        [InlineKeyboardButton(text="🔍 Перевірити VIN", callback_data="check_vin")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("👋 **Вітаємо в BitokAuto.ua!**\n\nОбирай потрібний розділ нижче 👇", reply_markup=get_main_keyboard(), parse_mode="Markdown")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    await bot.delete_webhook(drop_pending_updates=True)
    polling_task = asyncio.create_task(dp.start_polling(bot))
    print(">>> BOT STARTED VIA LONG POLLING <<<")
    yield
    polling_task.cancel()

app = FastAPI(lifespan=lifespan)

@app.get("/api/cars")
async def get_cars():
    cars = load_cars()
    return JSONResponse(content=cars, media_type="application/json; charset=utf-8")

@app.post("/api/add-car")
async def add_car(car: CarItem, x_secret: str = Header(None)):
    if x_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    
    cars = load_cars()
    # Удаляем старую машину с таким же VIN, если есть, и добавляем новую в начало
    cars = [c for c in cars if c.get("vin") != car.vin]
    cars.insert(0, car.dict())
    save_cars(cars)
    return {"status": "success", "vin": car.vin}

@app.post("/api/clear-cars")
async def clear_cars(x_secret: str = Header(None)):
    if x_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    save_cars([])
    return {"status": "cleared"}

@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>BitokAuto.ua Backend is running!</h1>"
