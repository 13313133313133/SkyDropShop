import os
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime

# ---------------- CONFIG ----------------
BOT_TOKEN = "YOUR_TOKEN_HERE"  # вставь сюда свой токен
OWNER_USERNAME = "tyxaye"
REVIEWS_LINK = "https://t.me/SkyDropShop_reviews"
SUPPORT_LINK = "https://t.me/tyxaye"
ADMIN_GROUP_ID = -4998203434

# Оплата
PAYMENT_INFO = {
    "ru": "🇷🇺 Оплата с русской карты — напишите в поддержку: @tyxaye",
    "ua": (
        "🇺🇦 Оплата на карту Украины:\n\n"
        "Monobank: <code>4441111023152402</code>\n"
        "Privat24: <code>5168752022974177</code>\n\n"
        "После оплаты нажмите 'Я оплатил' и отправьте скрин."
    )
}

# Цены
PRICES = {
    "fortnite_account": {
        "В-баксы (на акк)": [
            ("1000 В-баксов", "597₽ / 269₴ / 6.65$"),
            ("2800 В-баксов", "1407₽ / 633₴ / 15.65$"),
            ("5000 В-баксов", "2223₽ / 1000₴ / 24.70$"),
            ("13500 В-баксов", "5297₽ / 2384₴ / 58.85$"),
            ("27000 В-баксов", "10397₽ / 4680₴ / 115.50$"),
            ("40500 В-баксов", "15297₽ / 6884₴ / 170.00$"),
        ],
        "В-баксы подарком": [
            ("200 В-Баксов", "96₽ / 43₴ / 1.05$"),
            ("300 В-Баксов", "145₽ / 65₴ / 1.60$"),
            ("500 В-Баксов", "243₽ / 109₴ / 2.70$"),
            ("800 В-Баксов", "390₽ / 176₴ / 4.30$"),
            ("1000 В-Баксов", "488₽ / 220₴ / 5.40$"),
            ("1200 В-Баксов", "586₽ / 264₴ / 6.50$"),
            ("1400 В-Баксов", "684₽ / 308₴ / 7.60$"),
            ("1500 В-Баксов", "733₽ / 330₴ / 8.15$"),
            ("1600 В-Баксов", "782₽ / 352₴ / 8.70$"),
            ("1800 В-Баксов", "880₽ / 396₴ / 9.80$"),
            ("1900 В-Баксов", "929₽ / 418₴ / 10.30$"),
            ("2000 В-Баксов", "978₽ / 440₴ / 10.90$"),
            ("2500 В-Баксов", "1223₽ / 550₴ / 13.60$"),
            ("2800 В-Баксов", "1370₽ / 617₴ / 15.20$"),
            ("3000 В-Баксов", "1468₽ / 661₴ / 16.30$"),
        ],
        "Наборы": [("Пример набора", "Свяжитесь с поддержкой для уточнения.")],
        "Отряд Fortnite": [("Подписка Отряд", "Свяжитесь с поддержкой для уточнения.")],
    },
    "telegram_stars": [
        ("50 ⭐️", "44 ₴ / 0.9 $ / 85.5 ₽"),
        ("100 ⭐️", "84 ₴ / 1.75 $ / 166.25 ₽"),
        ("250 ⭐️", "205 ₴ / 4.25 $ / 403.75 ₽"),
        ("500 ⭐️", "410 ₴ / 8.5 $ / 807.5 ₽"),
        ("1000 ⭐️", "805 ₴ / 17 $ / 1615 ₽"),
    ],
}

# ---------------- INIT ----------------
logging.basicConfig(level=logging.INFO, filename="orders.log", filemode="a", format="%(asctime)s | %(message)s")
bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# ---------------- MAIN MENU ----------------
def main_menu():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Магазин 🔥", callback_data="shop")],
        [
            InlineKeyboardButton(text="Отзывы ⭐", url=REVIEWS_LINK),
            InlineKeyboardButton(text="Поддержка 👮", url=SUPPORT_LINK),
        ],
    ])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("💎 Добро пожаловать в SkyDropShop!\nВыберите категорию ниже 👇", reply_markup=main_menu())

# ---------------- SHOP ----------------
@dp.callback_query(F.data == "shop")
async def open_shop(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Fortnite 🎮", callback_data="fortnite")],
        [InlineKeyboardButton(text="Telegram ⭐ Звёзды", callback_data="telegram_stars")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_main")]
    ])
    await callback.message.edit_text("🛍 Выберите категорию:", reply_markup=kb)

@dp.callback_query(F.data == "back_main")
async def back_main(callback: types.CallbackQuery):
    await callback.message.edit_text("💎 Добро пожаловать в SkyDropShop!\nВыберите категорию ниже 👇", reply_markup=main_menu())

# Fortnite
@dp.callback_query(F.data == "fortnite")
async def fortnite_menu(callback: types.CallbackQuery):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=k, callback_data=f"fortnite_{k}") for k in PRICES["fortnite_account"].keys()],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")]
    ])
    await callback.message.edit_text("🎮 Fortnite — выберите подкатегорию:", reply_markup=kb)

# Telegram Stars
@dp.callback_query(F.data == "telegram_stars")
async def telegram_stars(callback: types.CallbackQuery):
    text = "⭐ Цены на Telegram Stars:\n\n"
    for name, price in PRICES["telegram_stars"]:
        text += f"<b>{name}</b> — {price}\n"
    text += "\nВыберите способ оплаты:"
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🇷🇺 Русская карта", callback_data="pay_ru"),
         InlineKeyboardButton(text="🇺🇦 Украинская карта", callback_data="pay_ua")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")]
    ])
    await callback.message.edit_text(text, reply_markup=kb)

# Оплата
@dp.callback_query(F.data.startswith("pay_"))
async def show_payment(callback: types.CallbackQuery):
    method = callback.data.split("_")[1]
    await callback.message.edit_text(PAYMENT_INFO[method], reply_markup=InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Я оплатил / Отправить скрин 📸", callback_data="paid")],
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="shop")]
    ]))

# Получение скринов
@dp.callback_query(F.data == "paid")
async def paid(callback: types.CallbackQuery):
    await callback.message.answer("📸 Отправьте скриншот оплаты сюда.")

@dp.message(F.photo)
async def handle_photo(message: types.Message):
    caption = f"💰 Новый заказ!\n👤 @{message.from_user.username} (ID: {message.from_user.id})"
    await message.bot.send_photo(chat_id=ADMIN_GROUP_ID, photo=message.photo[-1].file_id, caption=caption)
    logging.info(f"NEW ORDER from {message.from_user.id} (@{message.from_user.username})")

# ---------------- RUN ----------------
if __name__ == "__main__":
    import asyncio
    async def main():
        await dp.start_polling(bot)
    asyncio.run(main())
