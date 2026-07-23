#!/usr/bin/env python3
"""Ensure desktop headlines popup is visible on hover."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:hover .tip-text,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text:hover {
            transition-delay: 0s !important;
        }"""

NEW = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:hover .tip-text,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text:hover {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            transition-delay: 0s !important;
        }"""


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        if OLD not in text:
            raise SystemExit(f"Expected hover block not found in {path.name}")
        path.write_text(text.replace(OLD, NEW, 1), encoding="utf-8")
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
