#!/usr/bin/env python3
"""
Step 9 — Verify Alpha Vantage rate-limit retry and recovery in market_data.

Uses mocks to simulate AV throttle responses without hammering the live API.

Usage:
    python admin_tools/test_rate_limit_recovery.py
"""

from __future__ import annotations

import sys
import time
from pathlib import Path
from unittest.mock import MagicMock, patch

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from market_data import MarketData  # noqa: E402


def _ok_quote_response() -> dict:
    return {
        "Global Quote": {
            "05. price": "100.50",
        }
    }


def _rate_limit_response() -> dict:
    return {
        "Note": "Thank you for using Alpha Vantage! Our standard API call frequency is 5 calls per minute.",
    }


def test_retries_then_recovers() -> bool:
    """Simulate rate-limit Note twice, then a successful response."""
    md = MarketData()
    md.api_key = "test-key"
    responses = [
        MagicMock(status_code=200, ok=True, json=lambda: _rate_limit_response()),
        MagicMock(status_code=200, ok=True, json=lambda: _rate_limit_response()),
        MagicMock(status_code=200, ok=True, json=lambda: _ok_quote_response()),
    ]

    with patch.object(md.session, "get", side_effect=responses) as get_mock:
        with patch("market_data.time.sleep") as sleep_mock:
            data = md._request(function="GLOBAL_QUOTE", symbol="AAPL")

    recovered = data.get("Global Quote", {}).get("05. price") == "100.50"
    retried = get_mock.call_count == 3
    slept = sleep_mock.call_count == 2
    return recovered and retried and slept


def test_exhausted_retries_returns_empty() -> bool:
    """After max attempts, _request returns {} without raising."""
    md = MarketData()
    md.api_key = "test-key"
    throttle = MagicMock(status_code=200, ok=True, json=lambda: _rate_limit_response())

    with patch.object(md.session, "get", return_value=throttle) as get_mock:
        with patch("market_data.time.sleep"):
            data = md._request(function="GLOBAL_QUOTE", symbol="AAPL")

    return data == {} and get_mock.call_count == 4


def test_network_error_retries() -> bool:
    """Transient network errors trigger retry before success."""
    import requests

    md = MarketData()
    md.api_key = "test-key"
    ok = MagicMock(status_code=200, ok=True, json=lambda: _ok_quote_response())

    with patch.object(
        md.session,
        "get",
        side_effect=[requests.Timeout("timeout"), ok],
    ) as get_mock:
        with patch("market_data.time.sleep"):
            data = md._request(function="GLOBAL_QUOTE", symbol="AAPL")

    return data.get("Global Quote") and get_mock.call_count == 2


def test_get_latest_price_survives_empty_response() -> bool:
    """Public API returns 0.0 instead of crashing when all retries fail."""
    md = MarketData()
    with patch.object(md, "_request", return_value={}):
        with patch.object(md, "_daily_history_frame", return_value=__import__("pandas").DataFrame()):
            price = md.get_latest_price("AAPL")
    return price == 0.0


def test_live_recovery_smoke() -> bool:
    """One live AV call succeeds (sanity check API key + connectivity)."""
    md = MarketData()
    started = time.perf_counter()
    price = md.get_latest_price("AAPL")
    elapsed = time.perf_counter() - started
    return bool(price) and price > 0 and elapsed < 30


def main() -> int:
    checks = [
        ("Retries then recovers (mock)", test_retries_then_recovers()),
        ("Exhausted retries return empty (mock)", test_exhausted_retries_returns_empty()),
        ("Network error retries (mock)", test_network_error_retries()),
        ("get_latest_price survives empty (mock)", test_get_latest_price_survives_empty_response()),
        ("Live AAPL quote smoke", test_live_recovery_smoke()),
    ]

    print("Step 9 — Rate-limit recovery test")
    print("-" * 60)
    for label, ok in checks:
        print(f"[{'PASS' if ok else 'FAIL'}] {label}")

    passed = all(ok for _, ok in checks)
    print("-" * 60)
    print(f"Overall: {'PASS' if passed else 'FAIL'}")
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
