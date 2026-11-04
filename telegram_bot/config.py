"""Configuration helpers for the FinanceHub Telegram bot.

The bot reads its secrets from the environment. A local ``.env`` file at the
repository root (or inside ``telegram_bot/``) is loaded automatically so the
same setup works on Windows and Linux.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(_PROJECT_ROOT / ".env")
load_dotenv(Path(__file__).resolve().parent / ".env")

_DEFAULT_SCRAPE_TIMEOUT = 8


def get_token() -> str:
    """Return the BotFather token or fail with a clear setup error."""
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError(
            "TELEGRAM_BOT_TOKEN is not set. Copy telegram_bot/.env.example "
            "to .env and add the token you received from BotFather."
        )
    return token


def get_scrape_timeout() -> int:
    """Return the HTTP timeout used by the price scraper, in seconds."""
    raw_value = os.environ.get("MARKET_SCRAPE_TIMEOUT", str(_DEFAULT_SCRAPE_TIMEOUT))
    try:
        return max(1, int(raw_value))
    except (TypeError, ValueError):
        return _DEFAULT_SCRAPE_TIMEOUT
