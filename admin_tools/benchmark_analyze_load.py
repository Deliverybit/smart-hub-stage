#!/usr/bin/env python3
"""Benchmark Analyze page data-loading steps by asset class."""

from __future__ import annotations

import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from analyze_page import SCREENER_SNAPSHOT_KEY_BY_PATH  # noqa: E402
from market_data import MarketData  # noqa: E402
from predictor import Predictor  # noqa: E402
from screener_headlines import get_cached_news_items, normalize_screener_ticker  # noqa: E402
from sentiment_engine import SentimentEngine  # noqa: E402

CASES = [
    ("NYSE", "NKE", "/NYSE_Top_10"),
    ("NASDAQ", "AAPL", "/NASDAQ_Top_10"),
    ("Crypto (BTC)", "BTC-USD", "/Crypto_Top_10"),
    ("Crypto (DOGE)", "DOGE-USD", "/Crypto_Top_10"),
    ("CME", "CL=F", "/CME_Top_10"),
    ("ICE", "BZ=F", "/ICE_Top_10"),
]


def _ms(start: float) -> float:
    return round((time.perf_counter() - start) * 1000, 1)


def benchmark_case(label: str, ticker: str, from_path: str, days: int = 30) -> dict:
    sym = normalize_screener_ticker(ticker)
    screener_key = SCREENER_SNAPSHOT_KEY_BY_PATH.get(from_path)
    market = MarketData()
    sentiment = SentimentEngine()
    predictor = Predictor()

    t0 = time.perf_counter()
    price = market.get_analyze_price_bundle(sym, days)
    price_ms = _ms(t0)
    history_rows = len(price["history"]) if price else 0
    daily_rows = 0
    if price:
        cache_key = market._daily_cache_key(sym, "full")
        frame = market._daily_cache.get(cache_key)
        daily_rows = len(frame) if frame is not None else history_rows

    t1 = time.perf_counter()
    news_items = get_cached_news_items(sym, screener_key=screener_key)
    news_ms = _ms(t1)
    news_source = "snapshot" if screener_key else "unknown"

    t2 = time.perf_counter()
    headlines = [item["title"] for item in news_items]
    sent_result = sentiment.analyze_headlines(sym, headlines)
    sent_ms = _ms(t2)

    t3 = time.perf_counter()
    latest_price = price["latest_price"] if price else 0
    history = price["history"] if price else []
    if len(history) >= 2:
        prev_price = history[-2]["price"]
        price_change_pct = (latest_price - prev_price) / prev_price if prev_price else 0
    else:
        price_change_pct = 0
    predictor.predict(
        sym,
        headlines,
        market_data=market,
        latest_price=latest_price,
        price_change_pct=price_change_pct,
    )
    predict_ms = _ms(t3)

    total_ms = round(price_ms + news_ms + sent_ms + predict_ms, 1)

    # Detect whether headlines came from snapshot
    from screener_headlines import news_items_from_snapshot

    if news_items_from_snapshot(sym, screener_key or ""):
        news_source = "snapshot"
    elif news_items:
        news_source = "api/cache"

    return {
        "label": label,
        "ticker": sym,
        "screener_key": screener_key,
        "price_ms": price_ms,
        "daily_rows": daily_rows,
        "chart_rows": history_rows,
        "news_ms": news_ms,
        "news_source": news_source,
        "headline_count": len(news_items),
        "sent_ms": sent_ms,
        "predict_ms": predict_ms,
        "total_ms": total_ms,
        "ok": price is not None,
    }


def main() -> int:
    print("Analyze load benchmark (cold MarketData cache per run)")
    print("=" * 72)
    rows = []
    for label, ticker, from_path in CASES:
        market = MarketData()
        market._daily_cache.clear()
        market._news_cache.clear()
        row = benchmark_case(label, ticker, from_path)
        rows.append(row)
        status = "OK" if row["ok"] else "FAIL"
        print(
            f"[{status}] {row['label']:<14} {row['ticker']:<10} "
            f"total={row['total_ms']:>7.1f}ms  price={row['price_ms']:>7.1f}ms "
            f"news={row['news_ms']:>6.1f}ms ({row['news_source']})  "
            f"sent={row['sent_ms']:>5.1f}ms  predict={row['predict_ms']:>5.1f}ms  "
            f"daily_rows={row['daily_rows']}"
        )

    print("=" * 72)
    crypto = [r for r in rows if "Crypto" in r["label"]]
    equity = [r for r in rows if r["label"] in ("NYSE", "NASDAQ")]
    commodity = [r for r in rows if r["label"] in ("CME", "ICE")]
    if crypto and equity:
        avg_crypto = sum(r["total_ms"] for r in crypto) / len(crypto)
        avg_equity = sum(r["total_ms"] for r in equity) / len(equity)
        print(f"Avg equity total:    {avg_equity:.1f} ms")
        print(f"Avg crypto total:    {avg_crypto:.1f} ms")
        if commodity:
            avg_comm = sum(r["total_ms"] for r in commodity) / len(commodity)
            print(f"Avg commodity total: {avg_comm:.1f} ms")
        slowest = max(rows, key=lambda r: r["total_ms"])
        print(f"Slowest: {slowest['label']} ({slowest['ticker']}) at {slowest['total_ms']:.1f} ms")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
