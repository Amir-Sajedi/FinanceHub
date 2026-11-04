# FinanceHub Telegram Bot

A small Persian-language Telegram bot that returns the same live market data
scraped by the FinanceHub website (`conversionapp/scraper.py`).

## Features

- Persian-only user-facing messages.
- Prices for USD, IQD, 18K/24K gold, gold ounce, silver gram, and silver ounce.
- 4-minute cache and a 24-hour last-good fallback.
- On-demand scraping through the existing project scraper.
- Long polling, so no public webhook/HTTPS endpoint is required.

## 1. Create the bot with BotFather

1. Open Telegram and start a chat with **@BotFather**.
2. Send `/newbot`.
3. Choose a display name and a username ending in `bot`.
4. Copy the token BotFather gives you.

BotFather only registers the bot and issues the token. The bot still needs to
run on a machine that can reach the Telegram API.

Register the command list with `/setcommands`:

```text
start - شروع و نمایش منو
prices - نرخ لحظه‌ای بازار
gold - طلا و نقره
currency - ارز
help - راهنما
```

## 2. Install

From the repository root:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# Linux/macOS
# source .venv/bin/activate

python -m pip install -r telegram_bot/requirements.txt
```

## 3. Configure

Copy the example file and add the BotFather token:

```bash
# Windows
copy telegram_bot\.env.example .env

# Linux/macOS
cp telegram_bot/.env.example .env
```

Edit `.env`:

```dotenv
TELEGRAM_BOT_TOKEN=123456789:your-real-token
MARKET_SCRAPE_TIMEOUT=8
```

Never commit `.env`; it is ignored by Git.

## 4. Run

```bash
python -m telegram_bot.bot
```

You can also run `python telegram_bot/bot.py`; the entry point adds the
repository root to `sys.path` automatically.

## 5. Keep it running

On a Linux server, a systemd unit is the simplest option:

```ini
[Unit]
Description=FinanceHub Telegram Bot
After=network-online.target

[Service]
WorkingDirectory=/opt/FinanceHub
EnvironmentFile=/opt/FinanceHub/.env
ExecStart=/opt/FinanceHub/.venv/bin/python -m telegram_bot.bot
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Then enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now financehub-bot
sudo journalctl -u financehub-bot -f
```

## Tests

```bash
python -m unittest discover -s telegram_bot/tests -v
```

## Project layout

```text
telegram_bot/
  bot.py           # Telegram handlers, commands, and keyboards
  config.py        # environment and .env loading
  messages.py      # all Persian text and report templates
  rates.py         # scraper wrapper, cache, and fallback
  requirements.txt
  .env.example
  tests/
```

## Notes

- Prices are shown in **ریال** to match the website.
- Ounce prices are shown in **دلار**.
- Dates use the Jalali calendar and `Asia/Tehran`.
- If tgju.org is unavailable, the bot serves the last successful snapshot for
  up to 24 hours and marks it as «آخرین داده معتبر».
- The scraper is synchronous; the bot runs it in a worker thread so Telegram
  updates stay responsive.
