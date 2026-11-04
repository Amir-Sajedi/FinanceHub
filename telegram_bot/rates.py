"""Price loading, caching, and fallback for the Telegram bot.

The bot deliberately reuses the website's scraper instead of duplicating the
tgju.org parsing logic. Successful snapshots are cached for four minutes and
the last good snapshot is kept for 24 hours, matching the website's behaviour.
"""

from __future__ import annotations

import logging
import sys
import threading
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(_PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(_PROJECT_ROOT))

from bkiblog.conversionapp.scraper import scrape_market_prices  # noqa: E402

from telegram_bot.config import get_scrape_timeout  # noqa: E402

logger = logging.getLogger(__name__)

USD_IQD_PEG = 1310.0
CACHE_TTL_SECONDS = 240
LAST_GOOD_TTL_SECONDS = 86400

_SCRAPE_TIMEOUT = get_scrape_timeout()
_SCRAPED_KEYS = (
    "usd",
    "gold_18k",
    "gold_24k",
    "gold_oz",
    "silver_gram",
    "silver_oz",
)

_lock = threading.Lock()
_cached: "MarketSnapshot | None" = None
_cached_at = 0.0
_last_good: "MarketSnapshot | None" = None
_last_good_at = 0.0


@dataclass(frozen=True)
class MarketSnapshot:
    """A normalized set of market values plus the time they were fetched."""

    values: dict[str, float]
    fetched_at: datetime
    is_live: bool = True


def _normalize(raw_data: dict[str, Any]) -> dict[str, float]:
    values: dict[str, float] = {}

    for key in _SCRAPED_KEYS:
        raw_value = raw_data.get(key)
        if raw_value is None:
            continue
        try:
            value = float(raw_value)
        except (TypeError, ValueError):
            logger.warning("Ignoring non-numeric market value for %s: %r", key, raw_value)
            continue
        if value > 0:
            values[key] = value

    usd = values.get("usd")
    if usd:
        # IQD is pegged at ~1310 IQD per USD, so one IQD is USD / 1310.
        values["iqd"] = usd / USD_IQD_PEG

    return values


def _fallback(now: float) -> MarketSnapshot | None:
    if _last_good is not None and now - _last_good_at < LAST_GOOD_TTL_SECONDS:
        return replace(_last_good, is_live=False)
    return None


def get_market_snapshot() -> MarketSnapshot | None:
    """Return a market snapshot, or ``None`` when no data is available.

    A fresh scrape is attempted only after the four-minute cache expires. If the
    scrape fails, the last successful snapshot is returned for up to 24 hours
    with ``is_live=False``.
    """
    global _cached, _cached_at, _last_good, _last_good_at

    now = time.monotonic()
    with _lock:
        if _cached is not None and now - _cached_at < CACHE_TTL_SECONDS:
            return _cached

        try:
            raw_data = scrape_market_prices(timeout=_SCRAPE_TIMEOUT)
        except Exception as exc:  # scraper and network errors share this path
            logger.warning("Market scrape failed, using last good snapshot: %s", exc)
            return _fallback(time.monotonic())

        values = _normalize(raw_data)
        if not values:
            logger.warning("Market scrape returned no usable values")
            return _fallback(time.monotonic())

        snapshot = MarketSnapshot(
            values=values,
            fetched_at=datetime.now(timezone.utc),
            is_live=True,
        )
        _cached = snapshot
        _cached_at = time.monotonic()
        _last_good = snapshot
        _last_good_at = _cached_at
        return snapshot


def reset_cache() -> None:
    """Clear all in-memory state. Intended for tests and manual recovery."""
    global _cached, _cached_at, _last_good, _last_good_at

    with _lock:
        _cached = None
        _cached_at = 0.0
        _last_good = None
        _last_good_at = 0.0
