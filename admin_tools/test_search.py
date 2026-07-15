#!/usr/bin/env python3
"""
Step 8 — Search page smoke test (market data paths used by app.py Search).

Usage:
    python admin_tools/test_search.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402

SEARCH_TICKERS = ("AAPL", "BTC-USD")


def _test_ticker(market_data: MarketData, ticker: str) -> dict:
    price = market_data.get_latest_price(ticker)
    history = market_data.get_price_history(ticker, days=7)
    headlines = market_data.get_news_headlines(ticker)
    week_low = market_data.get_52_week_low(ticker)
    week_high = market_data.get_52_week_high(ticker)

    ok = bool(price) and len(history) >= 2 and len(headlines) >= 1
    return {
        "ticker": ticker,
        "status": "PASS" if ok else "FAIL",
        "price": price,
        "history_days": len(history),
        "headlines": len(headlines),
        "week_low": week_low,
        "week_high": week_high,
    }


def main() -> int:
    print("Step 8 — Search page smoke test")
    print("-" * 60)

    market_data = MarketData()
    results = [_test_ticker(market_data, ticker) for ticker in SEARCH_TICKERS]

    for row in results:
        print(f"[{row['status']}] {row['ticker']}")
        print(f"  price={row['price']}  history={row['history_days']}d  headlines={row['headlines']}")
        print(f"  52w low={row['week_low']}  high={row['week_high']}")

    passed = all(row["status"] == "PASS" for row in results)
    print("-" * 60)
    print(f"Overall: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
