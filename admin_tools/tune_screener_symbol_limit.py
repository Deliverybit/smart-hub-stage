#!/usr/bin/env python3
"""
Step 6 — Tune SCREENER_SYMBOL_LIMIT using universe coverage + scan timing.

Benchmarks the current limit once (warm cache), then projects performance for
candidate limits without repeated Alpha Vantage cold scans.

Usage:
    python admin_tools/tune_screener_symbol_limit.py
    python admin_tools/tune_screener_symbol_limit.py --apply-staging
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.validate_screeners import (  # noqa: E402
    SCREENER_PAGES,
    load_universe,
    screen_ticker,
)
from app_config import get_screener_symbol_limit  # noqa: E402
from market_data import MarketData  # noqa: E402

SECRETS_PATH = ROOT / ".streamlit" / "secrets.toml"
CANDIDATE_LIMITS = (50, 83, 100, 500, 1000)


def _benchmark_current(market_data: MarketData, limit: int) -> list[dict]:
    rows = []
    for screener in SCREENER_PAGES:
        universe = load_universe(screener["path"], screener["universe_expr"], screener["deps"])
        scan = universe[:limit]
        started = time.perf_counter()
        candidates = 0
        for ticker in scan:
            if screen_ticker(market_data, ticker):
                candidates += 1
        elapsed = time.perf_counter() - started
        rows.append(
            {
                "name": screener["name"],
                "universe_size": len(universe),
                "scanned": len(scan),
                "coverage_pct": round((len(scan) / len(universe)) * 100, 1) if universe else 0.0,
                "candidates": candidates,
                "elapsed_sec": round(elapsed, 1),
                "sec_per_symbol": round(elapsed / len(scan), 2) if scan else 0.0,
            }
        )
    return rows


def _project_limit(rows: list[dict], limit: int) -> dict:
    screeners = []
    for row in rows:
        scanned = min(limit, row["universe_size"])
        coverage = round((scanned / row["universe_size"]) * 100, 1) if row["universe_size"] else 0.0
        projected = round(row["sec_per_symbol"] * scanned, 1)
        screeners.append(
            {
                "name": row["name"],
                "universe_size": row["universe_size"],
                "scanned": scanned,
                "coverage_pct": coverage,
                "projected_sec": projected,
            }
        )
    return {
        "limit": limit,
        "total_projected_sec": round(sum(item["projected_sec"] for item in screeners), 1),
        "min_coverage_pct": min(item["coverage_pct"] for item in screeners),
        "screeners": screeners,
    }


def _recommend_limit(projections: list[dict], max_universe: int, target_sec: float) -> int:
    full = [item for item in projections if item["min_coverage_pct"] >= 100.0]
    if not full:
        return max_universe
    under_target = [item for item in full if item["total_projected_sec"] <= target_sec]
    if under_target:
        return min(item["limit"] for item in under_target)
    return max_universe


def _update_secrets_limit(limit: int) -> bool:
    if not SECRETS_PATH.is_file():
        return False
    text = SECRETS_PATH.read_text(encoding="utf-8")
    if "SCREENER_SYMBOL_LIMIT" in text:
        lines = []
        for line in text.splitlines():
            if line.strip().startswith("SCREENER_SYMBOL_LIMIT"):
                lines.append(f"SCREENER_SYMBOL_LIMIT = {limit}")
            else:
                lines.append(line)
        SECRETS_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    else:
        SECRETS_PATH.write_text(text.rstrip() + f"\nSCREENER_SYMBOL_LIMIT = {limit}\n", encoding="utf-8")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description="Tune SCREENER_SYMBOL_LIMIT for staging.")
    parser.add_argument(
        "--target-sec",
        type=float,
        default=180.0,
        help="Target cold-scan budget (all screeners combined).",
    )
    parser.add_argument(
        "--apply-staging",
        action="store_true",
        help="Write recommended limit to .streamlit/secrets.toml if present.",
    )
    args = parser.parse_args()

    configured = get_screener_symbol_limit()
    print("Step 6 — SCREENER_SYMBOL_LIMIT tuning")
    print(f"Configured limit: {configured}")
    print("Running one live benchmark at configured limit (uses AV cache within run)...")
    print("-" * 72)

    market_data = MarketData()
    current_rows = _benchmark_current(market_data, configured)
    max_universe = max(row["universe_size"] for row in current_rows)

    for row in current_rows:
        print(
            f"{row['name']:<12} universe={row['universe_size']:<3} "
            f"scanned={row['scanned']:<3} coverage={row['coverage_pct']:>5}% "
            f"time={row['elapsed_sec']:>5}s ({row['sec_per_symbol']}s/symbol)"
        )

    projections = [_project_limit(current_rows, limit) for limit in CANDIDATE_LIMITS]
    recommended = _recommend_limit(projections, max_universe, args.target_sec)

    print("-" * 72)
    print(f"{'Limit':>6}  {'ProjectedTotal(s)':>18}  {'MinCoverage%':>14}")
    for item in projections:
        print(
            f"{item['limit']:>6}  {item['total_projected_sec']:>18.1f}  {item['min_coverage_pct']:>14.1f}"
        )

    print("-" * 72)
    print(f"Largest universe: {max_universe} symbols")
    print(f"Recommended SCREENER_SYMBOL_LIMIT: {recommended}")

    if recommended >= max_universe:
        print("Full coverage preserved for all current screeners.")
    if configured >= max_universe:
        print(
            f"Current value ({configured}) already scans full universes; "
            f"no reduction needed unless you add larger symbol lists later."
        )

    if recommended == 100 and configured == 1000:
        print("Optional: set SCREENER_SYMBOL_LIMIT = 100 for clarity (same coverage today).")

    report = {
        "step": 6,
        "configured_limit": configured,
        "recommended_limit": recommended,
        "max_universe": max_universe,
        "target_sec": args.target_sec,
        "current_benchmark": current_rows,
        "projections": projections,
    }
    report_path = ROOT / "docs" / "screener-symbol-limit-tuning.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(f"Report saved: {report_path}")

    if args.apply_staging:
        if _update_secrets_limit(recommended):
            os.environ["SCREENER_SYMBOL_LIMIT"] = str(recommended)
            print(f"Updated {SECRETS_PATH} -> SCREENER_SYMBOL_LIMIT = {recommended}")
        else:
            print(f"No {SECRETS_PATH} found; set SCREENER_SYMBOL_LIMIT = {recommended} manually.")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
