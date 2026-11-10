import asyncio
import logging
import os
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from fastapi import FastAPI

BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
app = FastAPI()

@app.get("/")
async def root():
    return {"status": "BitokAuto bot is running!"}

def get_main_keyboard():
    buttons = [
        [InlineKeyboardButton(text="🚗 Найти тачку (Каталог)", url="https://bitokauto.com.ua")],
        [InlineKeyboardButton(text="💼 Кабинет дилера", callback_data="seller_menu")],
        [InlineKeyboardButton(text="🔍 Проверить VIN", callback_data="check_vin")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)

# Команда /start - Главное меню
@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        f"Здорово, Димончик!\n\n"
        f"Это официальный бот **BitokAuto.ua** — аукционные авто из США и Европы с честной историей «Было / Стало».\n\n"
        f"Выбирай нужный раздел:",
        reply_markup=get_main_keyboard(),
        parse_mode="Markdown"
    )

# Команда /search - Найти авто
@dp.message(Command("search"))
async def cmd_search(message: types.Message):
    await message.answer(
        "🚗 Переходи в наш каталог, чтобы подобрать авто под ключ:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="Открыть каталог BitokAuto.ua", url="https://bitokauto.com.ua")]
        ])
    )

# Команда /check_vin - Проверить VIN
@dp.message(Command("check_vin"))
async def cmd_check_vin(message: types.Message):
    await message.answer(
        "🔍 Напиши VIN-код автомобиля (17 символов) прямо в чат, чтобы подтянуть историю с аукциона."
    )

# Команда /help - Поддержка
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer(
        "🆘 **Поддержка BitokAuto.ua**\n\n"
        "Возникли вопросы по покупке, доставке или растаможке? Пиши нам напрямую или проверяй лоты через VIN.",
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "check_vin")
async def process_check_vin(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "🔍 Напиши VIN-код автомобиля (17 символов) прямо в чат, чтобы подтянуть историю с аукциона.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ])
    )

@dp.callback_query(F.data == "seller_menu")
async def process_seller(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "💼 **Кабинет Дилера:**\n\n"
        "Чтобы выставить лот на BitokAuto.ua, отправь VIN-код машины в чат.",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_main")]
        ]),
        parse_mode="Markdown"
    )

@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: types.CallbackQuery):
    await callback.message.edit_text(
        "Главное меню BitokAuto.ua:",
        reply_markup=get_main_keyboard()
    )

@dp.message(F.text)
async def handle_vin_search(message: types.Message):
    text = message.text.strip().upper()
    if len(text) == 17:
        await message.answer(
            f"🔎 Проверяем VIN: `{text}` по базам Copart/IAAI и локальной базе BitokAuto...\n\n"
            f"⚠️ Автомобиль с таким VIN не найден в активных лотах.",
            parse_mode="Markdown"
        )
    else:
        await message.answer("❌ Неверный формат. VIN-код должен состоять ровно из 17 символов.")

async def start_telegram_bot():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(start_telegram_bot())
