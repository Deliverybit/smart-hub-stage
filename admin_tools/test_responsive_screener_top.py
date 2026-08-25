"""Mobile/tablet screener landing top spacing: compact gaps, bootstrap collapse."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import RESPONSIVE_SCREENER_TOP_COMPACT  # noqa: E402


def test_screener_top_compact_scoped_to_mobile_tablet() -> None:
    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css


def test_screener_top_compact_targets_active_flag() -> None:
    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert 'html[data-scoop-screener-active="1"]' in css
    assert "streamlit_js_eval" in css
    assert '[data-testid="stHtml"]' in css
    assert "gap: 0 !important" in css


def test_screener_top_compact_does_not_touch_desktop() -> None:
    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert 'html[data-scoop-desktop-layout="1"]' not in css


def test_screener_toggle_banner_gap_on_mobile_tablet() -> None:
    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert 'html[data-scoop-tab-nav="1"][data-scoop-screener-active="1"]' in css
    assert '[data-testid="stCheckbox"]' in css
    assert "font-size: 18px !important" in css
    assert "font-size: 14px !important" in css
    assert '[data-testid="stMarkdownContainer"]' in css
    assert "margin-top: 12px !important" in css
    assert "margin-bottom: 12px !important" in css
    assert ".scoop-banner-compact" in css


def test_screener_banner_cards_full_width_on_mobile_tablet() -> None:
    css = RESPONSIVE_SCREENER_TOP_COMPACT
    assert 'div[style*="max-width:50%"]' in css
    assert 'div[style*="max-width: 50%"]' in css
    assert "min-width: 0 !important" in css
    assert "flex: 1 1 100% !important" in css
    assert "@media (min-width: 1367px)" not in css


if __name__ == "__main__":
    tests = [
        test_screener_top_compact_scoped_to_mobile_tablet,
        test_screener_top_compact_targets_active_flag,
        test_screener_top_compact_does_not_touch_desktop,
        test_screener_toggle_banner_gap_on_mobile_tablet,
        test_screener_banner_cards_full_width_on_mobile_tablet,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} responsive screener top checks passed.")
