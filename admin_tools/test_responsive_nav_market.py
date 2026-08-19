#!/usr/bin/env python3
"""Verify mobile/tablet slide-out nav containers and active highlight."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import DESKTOP_SIDEBAR_NAV_MARKET  # noqa: E402


def _responsive_block(css: str) -> str:
    start = css.index("@media (max-width: 1366px)")
    return css[start:]


def test_responsive_nav_scoped_to_mobile_tablet() -> None:
    block = _responsive_block(DESKTOP_SIDEBAR_NAV_MARKET)
    assert "@media (max-width: 1366px)" in block
    assert 'a[href$="_Top_10"]' not in block


def test_responsive_nav_has_containers_light_and_dark() -> None:
    block = _responsive_block(DESKTOP_SIDEBAR_NAV_MARKET)
    assert 'html:not([data-scoop-theme="dark"])' in block
    assert 'html[data-scoop-theme="dark"]' in block
    assert "border: 1px solid #cbd5e1 !important" in block
    assert "border: 1px solid #404040 !important" in block


def test_responsive_nav_active_highlight_both_themes() -> None:
    block = _responsive_block(DESKTOP_SIDEBAR_NAV_MARKET)
    assert "[data-scoop-nav-active]" in block
    assert "background: #dbeafe !important" in block
    assert "background: #333333 !important" in block
    assert "border-color: #60a5fa !important" in block


def test_responsive_nav_styles_all_page_links() -> None:
    block = _responsive_block(DESKTOP_SIDEBAR_NAV_MARKET)
    assert '[data-testid="stPageLink"]' in block
    assert "margin-top: 10px !important" in block


def test_desktop_block_still_targets_top_10_only() -> None:
    css = DESKTOP_SIDEBAR_NAV_MARKET
    desktop_start = css.index("@media (min-width: 1367px)")
    desktop_end = css.index("@media (max-width: 1366px)")
    desktop = css[desktop_start:desktop_end]
    assert 'a[href$="_Top_10"]' in desktop


def main() -> int:
    tests = [
        test_responsive_nav_scoped_to_mobile_tablet,
        test_responsive_nav_has_containers_light_and_dark,
        test_responsive_nav_active_highlight_both_themes,
        test_responsive_nav_styles_all_page_links,
        test_desktop_block_still_targets_top_10_only,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} responsive nav market checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
