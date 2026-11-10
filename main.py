import os
import sqlite3
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException, Header
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = "https://bitokauto-bot-372810.onrender.com"
ADMIN_SECRET = os.getenv("ADMIN_SECRET", "super_secret_key_123")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def init_db():
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cars (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            price_usd REAL,
            vin TEXT UNIQUE,
            location TEXT,
            mileage TEXT,
            damage TEXT,
            image_url TEXT,
            source TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

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
    conn = sqlite3.connect("cars.db")
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM cars ORDER BY id DESC LIMIT 50")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@app.post("/api/add-car")
async def add_car(car: CarItem, x_secret: str = Header(None)):
    if x_secret != ADMIN_SECRET:
        raise HTTPException(status_code=403, detail="Unauthorized")
    conn = sqlite3.connect("cars.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR REPLACE INTO cars (title, price_usd, vin, location, mileage, damage, image_url, source) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (car.title, car.price_usd, car.vin, car.location, car.mileage, car.damage, car.image_url, car.source))
    conn.commit()
    conn.close()
    return {"status": "success", "vin": car.vin}

@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>BitokAuto.ua Backend is running!</h1>"
