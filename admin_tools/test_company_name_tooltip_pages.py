#!/usr/bin/env python3
"""Ensure screener pages no longer embed legacy below-card company tooltip CSS."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def test_pages_removed_legacy_company_below_tooltip_css() -> None:
    malformed = (
        'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip), '
        ".full-results-wrap .full-results-table tbody td[data-label=\"Name\"] "
        ".fr-val .tip-wrap:not(.headlines-tip) .tip-text"
    )
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        assert "scoop-name-tip-active" not in text, path.name
        assert "margin-top: 12px !important" not in text, path.name
        assert malformed not in text, path.name


def main() -> int:
    test_pages_removed_legacy_company_below_tooltip_css()
    print("PASS test_pages_removed_legacy_company_below_tooltip_css")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
