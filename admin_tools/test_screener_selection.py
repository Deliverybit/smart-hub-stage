"""Tests for screener proximity selection."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from screener_selection import (  # noqa: E402
    INTERNAL_THRESHOLD_PCT,
    MAX_PAD_CAP_PCT,
    TARGET_COUNT,
    select_proximity_results,
)


def _row(ticker: str, pct: float) -> dict:
    return {"Ticker": ticker, "% Above Low": pct}


def test_all_strict_when_enough_within_15():
    rows = [_row(f"T{i}", float(i)) for i in range(1, 12)]
    selection = select_proximity_results(rows)
    assert selection.mode == "all_strict"
    assert len(selection.results) == TARGET_COUNT
    assert all(r["% Above Low"] <= INTERNAL_THRESHOLD_PCT for r in selection.results)


def test_pads_to_ten_from_30_cap():
    rows = [_row("A", 5), _row("B", 12), _row("C", 18), _row("D", 25), _row("E", 29)]
    selection = select_proximity_results(rows)
    assert selection.mode == "padded"
    assert len(selection.results) == 5
    assert selection.strict_count == 2
    assert selection.padded_count == 3


def test_excludes_rows_above_30():
    rows = [_row("A", 10), _row("B", 35), _row("C", 40)]
    selection = select_proximity_results(rows)
    assert len(selection.results) == 1
    assert selection.results[0]["Ticker"] == "A"
    assert all(r["% Above Low"] <= MAX_PAD_CAP_PCT for r in selection.results)


def test_empty_when_everything_above_30():
    rows = [_row("A", 31), _row("B", 50)]
    selection = select_proximity_results(rows)
    assert selection.mode == "empty"
    assert selection.results == []


def main() -> int:
    test_all_strict_when_enough_within_15()
    test_pads_to_ten_from_30_cap()
    test_excludes_rows_above_30()
    test_empty_when_everything_above_30()
    print("screener_selection tests: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
