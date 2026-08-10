#!/usr/bin/env python3
"""Verify Analyze back navigation marks parent session storage on mobile/tablet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import analyze_page  # noqa: E402


def test_mark_analyze_return_uses_parent_session_storage() -> None:
    js = analyze_page._mark_analyze_return_js()
    assert "window.parent" in js
    assert "scoop-return-from-analyze" in js
    assert "scoop-landing-seen" in js
    assert "__scoopClearResponsiveExpandTimers" in js


def main() -> int:
    tests = [test_mark_analyze_return_uses_parent_session_storage]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} analyze return checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
