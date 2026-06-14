# Currency Rate Telegram Bot

A small Telegram bot that pulls live exchange rates straight from the National Bank of Ukraine and shows them in chat. No API keys, no paid tiers — the NBU publishes its rates openly, and the bot just formats them nicely.

It tracks USD, EUR, PLN and GBP against the hryvnia (UAH). Tap an inline button to see one currency, or grab all of them at once.

## What it does

- Reads rates from the official NBU API (`bank.gov.ua`) — free, no token required
- Inline keyboard: pick a single currency or hit "All rates"
- Caches responses for 10 minutes so it doesn't hammer the NBU endpoint
- Built on aiogram 3.x with async `aiohttp` under the hood

## Running it

You'll need a bot token from [@BotFather](https://t.me/BotFather) and Python 3.11+.

```bash
pip install -r requirements.txt
BOT_TOKEN=<your-token> python bot.py
```

That's it. Send `/start` to your bot and the keyboard shows up.

## Stack

Python 3.11+, aiogram 3.x, aiohttp.

## License

MIT — do whatever you like with it.
