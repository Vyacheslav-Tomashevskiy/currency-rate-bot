# 💱 Currency Rate Telegram Bot

Telegram-бот, що показує **актуальні курси валют НБУ** (USD/EUR/PLN/GBP до гривні) з офіційного API Національного банку України. Inline-кнопки для швидкого вибору валюти, кеш на 10 хв.

## Можливості
- Курси з офіційного API НБУ (без ключів, безкоштовно)
- Inline-клавіатура: окрема валюта або «Всі курси»
- Кешування (10 хв) — не навантажує API НБУ
- aiogram 3.x, async/aiohttp, чистий код

## Запуск
```bash
pip install -r requirements.txt
BOT_TOKEN=<ваш_токен_від_BotFather> python bot.py
```

## Стек
Python 3.11+, aiogram 3.x, aiohttp.

---

# 💱 Currency Rate Telegram Bot (EN)

Telegram bot showing live **NBU exchange rates** (USD/EUR/PLN/GBP to UAH) from the official National Bank of Ukraine API. Inline buttons, 10-min cache, aiogram 3.x.

```bash
pip install -r requirements.txt
BOT_TOKEN=<token> python bot.py
```
