"""All user-facing Persian text and report formatting for the bot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal, InvalidOperation, ROUND_HALF_UP
from typing import TYPE_CHECKING
from zoneinfo import ZoneInfo

import jdatetime
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

if TYPE_CHECKING:
    from telegram_bot.rates import MarketSnapshot

TEHRAN_TZ = ZoneInfo("Asia/Tehran")

CALLBACK_PRICES = "prices"
CALLBACK_METALS = "metals"
CALLBACK_CURRENCY = "currency"
CALLBACK_HELP = "help"

WELCOME = (
    "👋 به فاینانس‌هاب خوش آمدید.\n\n"
    "اینجا می‌توانید نرخ لحظه‌ای ارز، طلا و نقره را ببینید.\n"
    "یکی از گزینه‌های زیر را انتخاب کنید:"
)

LOADING = "⏳ در حال دریافت نرخ‌ها…"

ERROR = (
    "⚠️ دریافت نرخ‌ها در این لحظه ممکن نشد.\n"
    "لطفاً چند لحظه دیگر دوباره تلاش کنید."
)

UNKNOWN = (
    "متوجه درخواست شما نشدم.\n"
    "از دکمه‌های منو استفاده کنید یا /help را بزنید."
)

HELP = (
    "ℹ️ راهنما\n\n"
    "• /start — شروع و نمایش منو\n"
    "• /prices — همه نرخ‌ها\n"
    "• /gold — طلا و نقره\n"
    "• /currency — ارز\n"
    "• /help — همین راهنما\n\n"
    "نرخ‌ها از tgju.org دریافت می‌شوند."
)

STATUS_LIVE = "🟢 وضعیت: به‌روز"
STATUS_STALE = "🟡 وضعیت: آخرین داده معتبر"
STALE_WARNING = "⚠️ دریافت داده تازه ممکن نشد؛ نرخ‌های زیر ممکن است به‌روز نباشند."
SOURCE_LINE = "🔗 منبع: tgju.org"

_TRANSLATION = str.maketrans(
    {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
        ",": "٬",
        ".": "٫",
        "-": "−",
    }
)


@dataclass(frozen=True)
class RateRow:
    key: str
    label: str
    unit: str
    group: str
    decimals: int = 0


RATE_ROWS = (
    RateRow("usd", "دلار آمریکا", "ریال", "currency"),
    RateRow("iqd", "دینار عراق", "ریال", "currency"),
    RateRow("gold_18k", "طلای ۱۸ عیار (هر گرم)", "ریال", "gold"),
    RateRow("gold_24k", "طلای ۲۴ عیار (هر گرم)", "ریال", "gold"),
    RateRow("gold_oz", "انس طلا", "دلار", "gold", decimals=2),
    RateRow("silver_gram", "نقره (هر گرم)", "ریال", "silver"),
    RateRow("silver_oz", "انس نقره", "دلار", "silver", decimals=2),
)


def to_persian_digits(text: str) -> str:
    """Convert Latin digits and numeric separators to Persian forms."""
    return str(text).translate(_TRANSLATION)


def format_amount(value: float | None, decimals: int = 0) -> str:
    """Format a price with rounded decimals, grouping, and Persian digits."""
    if value is None:
        return "—"

    try:
        quantizer = Decimal(1).scaleb(-decimals)
        amount = Decimal(str(value)).quantize(quantizer, rounding=ROUND_HALF_UP)
    except (InvalidOperation, TypeError, ValueError):
        return "—"

    text = f"{amount:,.{decimals}f}"
    if decimals:
        text = text.rstrip("0").rstrip(".")
    return to_persian_digits(text)


def format_jalali_datetime(value: datetime) -> str:
    """Render a timezone-aware datetime in the Jalali calendar, Tehran time."""
    local_value = value.astimezone(TEHRAN_TZ).replace(tzinfo=None)
    jalali_value = jdatetime.datetime.fromgregorian(datetime=local_value)
    return to_persian_digits(jalali_value.strftime("%Y/%m/%d ساعت %H:%M"))


def _header(title: str, snapshot: "MarketSnapshot") -> list[str]:
    lines = [
        title,
        STATUS_LIVE if snapshot.is_live else STATUS_STALE,
        f"🕒 آخرین به‌روزرسانی: {format_jalali_datetime(snapshot.fetched_at)}",
    ]
    if not snapshot.is_live:
        lines.extend(["", STALE_WARNING])
    lines.append("")
    return lines


def _rows(snapshot: "MarketSnapshot", group: str) -> list[str]:
    return [
        f"• {row.label}: {format_amount(snapshot.values.get(row.key), row.decimals)} {row.unit}"
        for row in RATE_ROWS
        if row.group == group
    ]


def full_report(snapshot: "MarketSnapshot") -> str:
    lines = _header("📊 نرخ لحظه‌ای بازار", snapshot)
    lines.append("💵 ارز")
    lines.extend(_rows(snapshot, "currency"))
    lines.extend(["", "🥇 طلا"])
    lines.extend(_rows(snapshot, "gold"))
    lines.extend(["", "🥈 نقره"])
    lines.extend(_rows(snapshot, "silver"))
    lines.extend(["", SOURCE_LINE])
    return "\n".join(lines)


def metals_report(snapshot: "MarketSnapshot") -> str:
    lines = _header("🥇 طلا و نقره", snapshot)
    lines.extend(_rows(snapshot, "gold"))
    lines.extend(_rows(snapshot, "silver"))
    lines.extend(["", SOURCE_LINE])
    return "\n".join(lines)


def currency_report(snapshot: "MarketSnapshot") -> str:
    lines = _header("💵 نرخ ارز", snapshot)
    lines.extend(_rows(snapshot, "currency"))
    lines.extend(["", SOURCE_LINE])
    return "\n".join(lines)


def build_report(kind: str, snapshot: "MarketSnapshot") -> str:
    if kind == CALLBACK_PRICES:
        return full_report(snapshot)
    if kind == CALLBACK_METALS:
        return metals_report(snapshot)
    if kind == CALLBACK_CURRENCY:
        return currency_report(snapshot)
    return UNKNOWN


def main_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("📊 نرخ لحظه‌ای", callback_data=CALLBACK_PRICES)],
            [
                InlineKeyboardButton("🥇 طلا و نقره", callback_data=CALLBACK_METALS),
                InlineKeyboardButton("💵 ارز", callback_data=CALLBACK_CURRENCY),
            ],
            [InlineKeyboardButton("ℹ️ راهنما", callback_data=CALLBACK_HELP)],
        ]
    )
