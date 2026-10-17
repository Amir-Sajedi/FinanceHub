"""Single source of truth for live market rates.

Both the converter/net-worth views and the public home page share this
helper so tgju.org slowness or failure never blocks a page: results are
cached for a few minutes and the last good result is kept longer as a
fallback. The returned shape matches what the converter template already
expects, plus a ``fetched_at`` timestamp (seconds since epoch).
"""

import logging
import time

from django.core.cache import caches

from .scraper import scrape_market_prices, PriceScraperError

logger = logging.getLogger(__name__)

CACHE_KEY = 'financehub:market_rates'
LAST_GOOD_KEY = 'financehub:market_rates:last_good'
CACHE_TIMEOUT = 240
LAST_GOOD_TIMEOUT = 86400
USD_IQD_PEG = 1310.0


def _build_rates(raw_data):
    exchange_rates = {}
    if 'gold_18k' in raw_data:
        exchange_rates['gold_18k'] = {'price': raw_data['gold_18k']}
    if 'gold_24k' in raw_data:
        exchange_rates['gold_24k'] = {'price': raw_data['gold_24k']}
    if 'gold_oz' in raw_data:
        exchange_rates['gold_oz'] = {'price': raw_data['gold_oz']}
    if 'silver_gram' in raw_data:
        exchange_rates['silver_gram'] = {'price': raw_data['silver_gram']}
    if 'silver_oz' in raw_data:
        exchange_rates['silver_oz'] = {'price': raw_data['silver_oz']}
    if 'usd' in raw_data:
        exchange_rates['usd'] = raw_data['usd']
        # IQD is pegged at ~1310 IQD per 1 USD,
        # so IRR per IQD = (IRR per USD) / 1310.
        try:
            usd_val = float(raw_data['usd'])
            if usd_val > 0:
                exchange_rates['iqd'] = usd_val / USD_IQD_PEG
                exchange_rates['usd_iqd'] = USD_IQD_PEG
        except (TypeError, ValueError):
            pass
    return exchange_rates


def get_market_rates(timeout=4):
    """Return ``(rates_dict, is_live)``; never raises.

    ``rates_dict`` keeps the converter-template shape plus ``fetched_at``.
    ``is_live`` is True when the data is current (fresh scrape or unexpired
    short cache), False when serving the longer last-good fallback.
    An empty dict means no data is available at all.
    """
    cache = caches['default']

    # Fresh copy (short TTL) answers instantly; tgju.org is only scraped once
    # the short cache has expired, so page loads never wait on the network.
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached, True

    try:
        raw_data = scrape_market_prices(timeout=timeout)
    except (PriceScraperError, Exception) as exc:
        logger.warning('Market scrape failed, using last good rates: %s', exc)
        last_good = cache.get(LAST_GOOD_KEY)
        if last_good:
            return last_good, False
        return {}, False

    rates = _build_rates(raw_data)
    if not rates:
        last_good = cache.get(LAST_GOOD_KEY)
        return (last_good, False) if last_good else ({}, False)

    rates['fetched_at'] = time.time()
    cache.set(CACHE_KEY, rates, CACHE_TIMEOUT)
    cache.set(LAST_GOOD_KEY, rates, LAST_GOOD_TIMEOUT)
    return rates, True
