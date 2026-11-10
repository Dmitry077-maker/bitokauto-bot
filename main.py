import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = "https://bitokauto-bot.onrender.com"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

# --- КАТАЛОГ И ВЕБ-ЧАСТЬ ---
@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>BitokAuto.ua Backend is running! index.html not found.</h1>"

# --- КЛАВИАТУРЫ БОТА ---
def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🚗 Знайти тачку (Каталог)", url=WEB_URL)],
        [InlineKeyboardButton(text="💼 Кабінет дилера", callback_data="seller_menu")],
        [InlineKeyboardButton(text="🔍 Перевірити VIN", callback_data="check_vin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# --- ЛОГИКА TELEGRAM БОТА ---
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Здорово, Димончик!\n\n"
        f"Це офіційний бот **BitokAuto.ua** — аукційні авто із США та Європи з чесною історією «Було / Стало».\n\n"
        f"Обирай потрібний розділ:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer(
        "🚗 Переходь до нашого каталогу, щоб підібрати авто під ключ:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Відкрити каталог BitokAuto.ua", url=WEB_URL)]
        ])
    )

@dp.message(Command("check_vin"))
async def cmd_check_vin(message: types.Message):
    await message.answer(
        "🔍 Напиши VIN-код автомобіля (17 символів) прямо в чат, щоб підтягнути історію з аукціону."
    )

@dp.callback_query(F.data == "check_vin")
async def process_check_vin(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔍 Напиши VIN-код автомобіля (17 символів) прямо в чат, щоб підтягнути історію з аукціону.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(F.data == "seller_menu")
async def process_seller(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💼 **Кабінет Дилера:**\n\n"
        "Щоб виставити лот на BitokAuto.ua, надішли VIN-код машини в чат.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Головне меню BitokAuto.ua:",
        reply_
