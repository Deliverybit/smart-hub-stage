#!/usr/bin/env python3
"""
Pre-launch smoke tests — run before starting Streamlit locally.

Usage (from repo root):
    python admin_tools/smoke_test.py
    python admin_tools/smoke_test.py --quick   # skip screener universe scan
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from screener_engine import SCREENER_DEFINITIONS  # noqa: E402
from screener_snapshots import fetch_snapshot, snapshot_is_fresh  # noqa: E402


def _run_script(relative_path: str, *extra_args: str) -> tuple[str, int]:
    script = ROOT / relative_path
    cmd = [sys.executable, str(script), *extra_args]
    result = subprocess.run(cmd, cwd=ROOT, check=False)
    return relative_path, result.returncode


def _check_snapshots() -> tuple[str, int]:
    label = "Screener snapshots (DB freshness)"
    missing = []
    stale = []
    empty = []

    for defn in SCREENER_DEFINITIONS:
        payload = fetch_snapshot(defn.key)
        if payload is None:
            missing.append(defn.key)
            continue
        display = payload.get("display_results") or []
        if len(display) < 1:
            empty.append(defn.key)
        if not snapshot_is_fresh(payload):
            stale.append(defn.key)

    problems = []
    if missing:
        problems.append(f"missing: {', '.join(missing)}")
    if empty:
        problems.append(f"empty display_results: {', '.join(empty)}")
    if stale:
        problems.append(f"stale: {', '.join(stale)}")

    if problems:
        print(f"[FAIL] {label}")
        for line in problems:
            print(f"  {line}")
        print("  Hint: python admin_tools/screener_worker.py")
        return label, 1

    print(f"[PASS] {label} — {len(SCREENER_DEFINITIONS)} screeners fresh")
    return label, 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Pre-launch smoke tests for Smart Hub Stage.")
    parser.add_argument(
        "--quick",
        action="store_true",
        help="Skip validate_screeners --quick (faster; DB + Search + rate-limit only)",
    )
    args = parser.parse_args()

    steps: list[tuple[str, int]] = []

    print("Pre-launch smoke tests")
    print("=" * 60)

    label, code = _run_script("admin_tools/test_rate_limit_recovery.py")
    steps.append((label, code))

    label, code = _run_script("admin_tools/test_search.py")
    steps.append((label, code))

    label, code = _check_snapshots()
    steps.append((label, code))

    if not args.quick:
        label, code = _run_script("admin_tools/validate_screeners.py", "--quick")
        steps.append((label, code))

    print("=" * 60)
    passed = sum(1 for _, code in steps if code == 0)
    for label, code in steps:
        print(f"[{'PASS' if code == 0 else 'FAIL'}] {label}")

    ok = all(code == 0 for _, code in steps)
    print(f"Summary: {passed}/{len(steps)} passed — {'READY TO LAUNCH' if ok else 'FIX FAILURES FIRST'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
