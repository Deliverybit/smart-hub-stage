#!/usr/bin/env python3
"""Verify desktop market nav containers do not affect mobile/tablet sidebars."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.dark_mode_css import DARK_MODE_CSS  # noqa: E402
from admin_tools.tablet_mobile_layout_css import DESKTOP_SIDEBAR_NAV_MARKET  # noqa: E402


def test_market_nav_css_scoped_to_desktop() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    assert "@media (min-width: 1367px)" in css
    assert 'html[data-scoop-desktop-layout="1"]' in css
    assert "@media (max-width: 1366px)" in css
    assert "background: transparent !important" in css


def test_dark_mode_css_does_not_style_market_nav_globally() -> None:
    assert 'stPageLink"]:has(a[href$="_Top_10"])' not in DARK_MODE_CSS


def test_light_rules_skip_dark_theme() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    assert 'html:not([data-scoop-theme="dark"])' in css
    assert "background: #000000 !important" in css


def test_dark_active_nav_has_desktop_grey_state() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    assert "[data-scoop-nav-active]" in css
    assert "background: #333333 !important" in css


def test_dark_layout_selector_uses_combined_html_attributes() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    assert 'html[data-scoop-theme="dark"]' in css


def test_desktop_market_nav_fixed_gap() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    assert "margin-top: 12px !important" in css
    assert 'a[href$="_Top_10"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]' in css
    assert '[data-testid="stSidebar"] [data-testid="stVerticalBlock"]' in css


def main() -> int:
    tests = [
        test_market_nav_css_scoped_to_desktop,
        test_dark_mode_css_does_not_style_market_nav_globally,
        test_light_rules_skip_dark_theme,
        test_dark_active_nav_has_desktop_grey_state,
        test_dark_layout_selector_uses_combined_html_attributes,
        test_desktop_market_nav_fixed_gap,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} desktop nav market checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
