from __future__ import annotations

import unittest
from dataclasses import replace
from datetime import datetime, timezone
from unittest.mock import patch

from telegram_bot import messages
from telegram_bot.rates import (
    MarketSnapshot,
    get_market_snapshot,
    reset_cache,
)


def _snapshot(**overrides) -> MarketSnapshot:
    values = {
        "usd": 1_000_000.0,
        "iqd": 1_000_000.0 / 1310.0,
        "gold_18k": 78_500_000.0,
        "gold_24k": 104_666_667.0,
        "gold_oz": 4050.25,
        "silver_gram": 1_250_000.0,
        "silver_oz": 50.5,
    }
    values.update(overrides)
    return MarketSnapshot(
        values=values,
        fetched_at=datetime(2026, 11, 4, 10, 30, tzinfo=timezone.utc),
        is_live=True,
    )


class MessageFormattingTests(unittest.TestCase):
    def test_full_report_contains_persian_labels_and_digits(self) -> None:
        text = messages.full_report(_snapshot())

        self.assertIn("دلار آمریکا", text)
        self.assertIn("طلای ۱۸ عیار (هر گرم)", text)
        self.assertIn("۱٬۰۰۰٬۰۰۰ ریال", text)
        self.assertIn("۴٬۰۵۰٫۲۵ دلار", text)
        self.assertIn("🟢 وضعیت: به‌روز", text)
        self.assertIn("tgju.org", text)
        self.assertFalse(any(char in text for char in "0123456789"))

    def test_missing_value_is_rendered_without_breaking_the_report(self) -> None:
        snapshot = _snapshot()
        del snapshot.values["silver_oz"]

        text = messages.metals_report(snapshot)

        self.assertIn("انس نقره: — دلار", text)
        self.assertIn("انس طلا: ۴٬۰۵۰٫۲۵ دلار", text)

    def test_stale_report_shows_warning(self) -> None:
        snapshot = replace(_snapshot(), is_live=False)

        text = messages.currency_report(snapshot)

        self.assertIn("🟡 وضعیت: آخرین داده معتبر", text)
        self.assertIn("ممکن است به‌روز نباشند", text)


class SnapshotCacheTests(unittest.TestCase):
    def setUp(self) -> None:
        reset_cache()

    def tearDown(self) -> None:
        reset_cache()

    @patch("telegram_bot.rates.scrape_market_prices")
    def test_successful_scrape_is_cached_and_iqd_is_derived(self, scrape) -> None:
        scrape.return_value = {
            "usd": 1310,
            "gold_18k": 10,
            "gold_24k": 20,
            "gold_oz": 30,
            "silver_gram": 40,
            "silver_oz": 50,
        }

        first = get_market_snapshot()
        second = get_market_snapshot()

        self.assertIsNotNone(first)
        self.assertIs(first, second)
        self.assertTrue(first.is_live)
        self.assertAlmostEqual(first.values["iqd"], 1.0)
        self.assertEqual(scrape.call_count, 1)

    @patch("telegram_bot.rates.scrape_market_prices")
    def test_failed_scrape_falls_back_to_last_good(self, scrape) -> None:
        raw_data = {
            "usd": 1000,
            "gold_18k": 10,
            "gold_24k": 20,
            "gold_oz": 30,
            "silver_gram": 40,
            "silver_oz": 50,
        }
        scrape.side_effect = [raw_data, RuntimeError("network down")]

        with patch("telegram_bot.rates.CACHE_TTL_SECONDS", 0.0):
            live = get_market_snapshot()
            stale = get_market_snapshot()

        self.assertIsNotNone(live)
        self.assertIsNotNone(stale)
        self.assertTrue(live.is_live)
        self.assertFalse(stale.is_live)
        self.assertEqual(live.values, stale.values)
        self.assertEqual(scrape.call_count, 2)

    @patch("telegram_bot.rates.scrape_market_prices")
    def test_no_data_returns_none(self, scrape) -> None:
        scrape.side_effect = RuntimeError("network down")

        self.assertIsNone(get_market_snapshot())


if __name__ == "__main__":
    unittest.main()
