#!/usr/bin/env python3
"""
Step 4 — Test screener cache refresh behavior.

Simulates "Clear cache and refresh" by clearing MarketData + headline caches,
then re-scanning the smallest screener (ICE) within the 2-minute recovery target.

Usage:
    python admin_tools/test_cache_refresh.py
"""

from __future__ import annotations

import sys
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.validate_screeners import load_universe, screen_ticker  # noqa: E402
from app_config import SCREENER_CACHE_VERSION, get_screener_symbol_limit  # noqa: E402
from market_data import MarketData  # noqa: E402
from screener_headlines import _cached_news_items  # noqa: E402

ICE_PAGE = ROOT / "pages" / "6_ICE_Top_10.py"
MAX_RECOVERY_SEC = 120


def scan_universe(market_data: MarketData, tickers: list[str]) -> list[dict]:
    rows = []
    for ticker in tickers:
        row = screen_ticker(market_data, ticker)
        if row:
            rows.append(row)
    rows.sort(key=lambda item: item["pct_above_low"])
    return rows


def clear_caches(market_data: MarketData) -> None:
    market_data._daily_cache.clear()
    _cached_news_items.clear()


def main() -> int:
    symbol_limit = get_screener_symbol_limit()
    universe = load_universe(
        ICE_PAGE,
        "list(COMMODITY_NAMES.keys())",
        ("COMMODITY_NAMES",),
    )
    tickers = universe[:symbol_limit]

    market_data = MarketData()

    print("Cache refresh test — ICE screener (smallest universe)")
    print(f"Symbols: {len(tickers)}  Recovery target: {MAX_RECOVERY_SEC}s")
    print("-" * 60)

    print("1) Warm scan (populate caches)...")
    warm_start = time.perf_counter()
    warm_results = scan_universe(market_data, tickers)
    warm_elapsed = time.perf_counter() - warm_start
    print(f"   Results: {len(warm_results)}  Elapsed: {warm_elapsed:.1f}s")

    print("2) Cached scan (should be faster)...")
    cache_start = time.perf_counter()
    cached_results = scan_universe(market_data, tickers)
    cache_elapsed = time.perf_counter() - cache_start
    print(f"   Results: {len(cached_results)}  Elapsed: {cache_elapsed:.1f}s")

    print("3) Clear caches (simulates 'Clear cache and refresh')...")
    clear_caches(market_data)

    print("4) Cold recovery scan...")
    cold_start = time.perf_counter()
    cold_results = scan_universe(market_data, tickers)
    cold_elapsed = time.perf_counter() - cold_start
    timestamp = datetime.now().strftime("%b %d, %Y  %I:%M %p")
    print(f"   Results: {len(cold_results)}  Elapsed: {cold_elapsed:.1f}s")
    print(f"   Last updated: {timestamp}")

    cache_faster = cache_elapsed < warm_elapsed
    recovery_ok = cold_elapsed <= MAX_RECOVERY_SEC and len(cold_results) >= 10
    top10_ok = len(cold_results) >= 10

    print("-" * 60)
    print(f"Cache hit faster than warm: {'PASS' if cache_faster else 'WARN'}")
    print(f"Recovery within {MAX_RECOVERY_SEC}s: {'PASS' if recovery_ok else 'FAIL'}")
    print(f"Top 10 available after refresh: {'PASS' if top10_ok else 'FAIL'}")

    if cold_results:
        top10 = [row["ticker"] for row in cold_results[:10]]
        print(f"Top tickers: {', '.join(top10)}")

    passed = recovery_ok and top10_ok
    print(f"\nOverall: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
