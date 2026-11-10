import os
import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_URL = "https://bitokauto-bot-3444.onrender.com/"


bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

@app.get("/", response_class=HTMLResponse)
async def root():
    if os.path.exists("index.html"):
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    return "<h1>BitokAuto.ua Backend is running!</h1>"

def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚗 Знайти тачку (Каталог)", url=WEB_URL)],
        [InlineKeyboardButton(text="💼 Кабінет дилера", callback_data="seller_menu")],
        [InlineKeyboardButton(text="🔍 Перевірити VIN", callback_data="check_vin")]
    ])

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привіт, Димончик!\n\nЦе офіційний бот **BitokAuto.ua** — аукційні авто із США та Європи.",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: types.CallbackQuery):
    await callback.message.edit_text("Головне меню BitokAuto.ua:", reply_markup=get_main_keyboard())

WEBHOOK_PATH = f"/bot/{BOT_TOKEN}"
WEBHOOK_URL = f"{WEB_URL}{WEBHOOK_PATH}"

@app.on_event("startup")
async def on_startup():
    logging.basicConfig(level=logging.INFO)
    # Сначала сбрасываем старый зависший вебхук Telegram
    await bot.delete_webhook(drop_pending_updates=True)
    # И принудительно вешаем на актуальный адрес с хвостом -3444
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
    print(f"WEBHOOK SET TO: {WEBHOOK_URL}")


@app.post(WEBHOOK_PATH)
async def bot_webhook(request: Request):
    json_data = await request.json()
    update = types.Update.model_validate(json_data, context={"bot": bot})
    await dp.feed_update(bot, update)
    return {"status": "ok"}
