"""FinanceHub Telegram bot entry point.

Run from the repository root with:

    python -m telegram_bot.bot
"""

from __future__ import annotations

import asyncio
import logging
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from telegram import Update
from telegram.error import BadRequest
from telegram.ext import (
    Application,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from telegram_bot import messages
from telegram_bot.config import get_token
from telegram_bot.rates import get_market_snapshot

logger = logging.getLogger(__name__)

_fetch_lock = asyncio.Lock()


async def _load_report(kind: str) -> str:
    """Load a report without blocking the Telegram event loop."""
    async with _fetch_lock:
        snapshot = await asyncio.to_thread(get_market_snapshot)
    if snapshot is None:
        return messages.ERROR
    return messages.build_report(kind, snapshot)


async def _send_report(update: Update, kind: str) -> None:
    message = update.effective_message
    if message is None:
        return

    loading_message = await message.reply_text(messages.LOADING)
    try:
        text = await _load_report(kind)
    except Exception:
        logger.exception("Failed to build the market report")
        text = messages.ERROR
    await loading_message.edit_text(text, reply_markup=messages.main_keyboard())


async def _safe_edit(
    query,
    text: str,
    *,
    show_keyboard: bool = True,
) -> None:
    try:
        await query.edit_message_text(
            text,
            reply_markup=messages.main_keyboard() if show_keyboard else None,
        )
    except BadRequest as exc:
        if "message is not modified" not in str(exc).lower():
            raise


async def start(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(messages.WELCOME, reply_markup=messages.main_keyboard())


async def prices_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_report(update, messages.CALLBACK_PRICES)


async def gold_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_report(update, messages.CALLBACK_METALS)


async def currency_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    await _send_report(update, messages.CALLBACK_CURRENCY)


async def help_command(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(messages.HELP, reply_markup=messages.main_keyboard())


async def button_handler(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    if query is None:
        return
    await query.answer()

    kind = query.data or ""
    if kind == messages.CALLBACK_HELP:
        await _safe_edit(query, messages.HELP)
        return
    if kind not in {
        messages.CALLBACK_PRICES,
        messages.CALLBACK_METALS,
        messages.CALLBACK_CURRENCY,
    }:
        await _safe_edit(query, messages.UNKNOWN)
        return

    await _safe_edit(query, messages.LOADING, show_keyboard=False)
    try:
        text = await _load_report(kind)
    except Exception:
        logger.exception("Failed to build the market report")
        text = messages.ERROR
    await _safe_edit(query, text)


async def unknown_message(update: Update, _context: ContextTypes.DEFAULT_TYPE) -> None:
    message = update.effective_message
    if message is None:
        return
    await message.reply_text(messages.UNKNOWN, reply_markup=messages.main_keyboard())


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.error("Unhandled update error", exc_info=context.error)
    if isinstance(update, Update) and update.effective_message is not None:
        try:
            await update.effective_message.reply_text(messages.ERROR)
        except Exception:
            logger.exception("Failed to send the fallback error message")


def build_application() -> Application:
    application = Application.builder().token(get_token()).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("prices", prices_command))
    application.add_handler(CommandHandler("gold", gold_command))
    application.add_handler(CommandHandler("currency", currency_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(
        MessageHandler(filters.TEXT | filters.COMMAND, unknown_message)
    )
    application.add_error_handler(error_handler)
    return application


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    application = build_application()
    logger.info("FinanceHub Telegram bot is running")
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
