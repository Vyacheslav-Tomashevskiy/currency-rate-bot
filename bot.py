"""
Telegram-бот курсів валют (НБУ) на aiogram 3.x.
Показує актуальні курси USD/EUR/PLN/GBP до гривні з офіційного API НБУ,
кешує відповідь на 10 хв, має inline-кнопки для швидкого вибору валюти.

Запуск:  BOT_TOKEN=<token> python bot.py
"""
import asyncio
import logging
import os
import time

import aiohttp
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

logging.basicConfig(level=logging.INFO)

NBU_API = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"
WATCHED = ("USD", "EUR", "PLN", "GBP")
_CACHE: dict[str, object] = {"ts": 0.0, "rates": {}}
CACHE_TTL = 600  # 10 хв


async def fetch_rates() -> dict[str, float]:
    """Тягне курси з API НБУ з простим кешем, щоб не довбати сервіс."""
    now = time.time()
    if now - _CACHE["ts"] < CACHE_TTL and _CACHE["rates"]:
        return _CACHE["rates"]  # type: ignore[return-value]

    async with aiohttp.ClientSession() as session:
        async with session.get(NBU_API, timeout=aiohttp.ClientTimeout(total=10)) as resp:
            resp.raise_for_status()
            data = await resp.json()

    rates = {item["cc"]: float(item["rate"]) for item in data if item["cc"] in WATCHED}
    _CACHE.update(ts=now, rates=rates)
    return rates


def rates_keyboard() -> InlineKeyboardMarkup:
    buttons = [InlineKeyboardButton(text=cc, callback_data=f"rate:{cc}") for cc in WATCHED]
    return InlineKeyboardMarkup(inline_keyboard=[buttons, [
        InlineKeyboardButton(text="🔄 Всі курси", callback_data="rate:ALL")
    ]])


def format_all(rates: dict[str, float]) -> str:
    lines = ["💱 <b>Курси НБУ</b> (грн за 1 одиницю):"]
    flags = {"USD": "🇺🇸", "EUR": "🇪🇺", "PLN": "🇵🇱", "GBP": "🇬🇧"}
    for cc in WATCHED:
        if cc in rates:
            lines.append(f"{flags.get(cc, '')} <b>{cc}</b> — {rates[cc]:.2f} ₴")
    return "\n".join(lines)


dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        "Привіт! Я показую актуальні курси валют від НБУ.\n"
        "Обери валюту або натисни «Всі курси».",
        reply_markup=rates_keyboard(),
    )


@dp.callback_query(F.data.startswith("rate:"))
async def on_rate(call: CallbackQuery) -> None:
    cc = call.data.split(":", 1)[1]
    try:
        rates = await fetch_rates()
    except Exception:
        await call.answer("Сервіс НБУ тимчасово недоступний, спробуйте пізніше", show_alert=True)
        return

    if cc == "ALL":
        text = format_all(rates)
    elif cc in rates:
        text = f"<b>{cc}</b> — {rates[cc]:.2f} ₴ (курс НБУ)"
    else:
        text = "Невідома валюта."

    await call.message.edit_text(text, reply_markup=rates_keyboard())
    await call.answer()


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        raise SystemExit("Вкажи BOT_TOKEN у змінній середовища")
    bot = Bot(token=token, parse_mode="HTML")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
