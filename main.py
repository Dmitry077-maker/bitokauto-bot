import os
import logging
import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = "https://bitokauto-bot-3444.onrender.com"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🚗 Відкрити каталог", web_app=WebAppInfo(url=WEB_URL))
        ],
        [
            InlineKeyboardButton(text="💼 Кабінет дилера", callback_data="seller_menu"),
            InlineKeyboardButton(text="🔍 Перевірити VIN", callback_data="check_vin")
        ]
    ])

# --- ХЭНДЛЕРЫ БОТА ---
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 **Вітаємо в BitokAuto.ua!**\n\n"
        "Тут ти можеш підібрати та розрахувати вартість аукціонних авто із США та Європи під ключ в Україні.\n\n"
        "Обирай потрібний розділ нижче 👇",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "seller_menu")
async def seller_menu(callback: types.CallbackQuery):
    await callback.message.answer("💼 Розділ для дилерів у розробці.")
    await callback.answer()

@dp.callback_query(F.data == "check_vin")
async def check_vin(callback: types.CallbackQuery):
    await callback.message.answer("🔍 Надішліть VIN-код вашого авто для перевірки.")
    await callback.answer()

# --- LIFESPAN ДЛЯ FASTAPI (Правильный запуск фона на современных версиях) ---
@asynccontextmanager
async def lifespan(app: FastAPI):
    logging.basicConfig(level=logging.INFO)
    # Сбрасываем вебхуки, чтобы Telegram отдавал апдейты через polling
    await bot.delete_webhook(drop_pending_updates=True)
    # Запускаем поллинг бота в отдельной фоновой задаче
    polling_task = asyncio.create_task(dp.start_polling(bot))
    print(">>> BOT STARTED VIA LONG POLLING <<<")
    yield
    # Отмена задачи при остановке сервера
    polling_task.cancel()

app = FastAPI(lifespan=lifespan)

# --- РУТЫ ВЕБ-САЙТА ---
@app.get("/", response_class=
