#!/usr/bin/env python3
"""Verify mobile/tablet back navigation is wired on every page."""

from __future__ import annotations

import inspect
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import landing_page  # noqa: E402

SCREENER_PAGES = (
    "pages/1_NYSE_Top_10.py",
    "pages/2_NASDAQ_Top_10.py",
    "pages/3_Crypto_Top_10.py",
    "pages/5_CME_Top_10.py",
    "pages/6_ICE_Top_10.py",
)

INNER_PAGES = SCREENER_PAGES + ("pages/7_Terms_of_Service.py", "pages/_Analyze.py")


def test_back_link_helper_renders_for_inner_pages() -> None:
    source = inspect.getsource(landing_page.render_mobile_back_home_bar)
    assert "← Back to Home" in source
    assert "HOME_PAGE" in source
    assert "scoop-mobile-back-home-bar" in source


def test_all_inner_pages_use_responsive_navigation() -> None:
    for rel in INNER_PAGES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        assert "render_responsive_navigation" in text, rel
        assert f'current_page="{rel}"' in text, rel


def test_landing_skips_back_link() -> None:
    home_source = inspect.getsource(landing_page.render_mobile_tablet_home)
    assert "render_mobile_back_home_bar" not in home_source
    assert "HOME_NAV_MARKETS" in home_source


def test_analyze_has_market_back_button() -> None:
    text = (ROOT / "pages/_Analyze.py").read_text(encoding="utf-8")
    assert "render_analyze_back_button" in text
    assert "_analyze_mode" in text


def test_back_link_hidden_on_desktop_via_tab_nav() -> None:
    from admin_tools.tablet_mobile_layout_css import MOBILE_BACK_HOME_BAR, RESPONSIVE_TAB_NAV_BOOTSTRAP

    css = RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert ".scoop-mobile-back-home" in css
    assert ".scoop-mobile-back-home-bar" in css
    assert MOBILE_BACK_HOME_BAR in css
    assert "@media (min-width: 1367px)" in MOBILE_BACK_HOME_BAR
    assert 'html[data-scoop-tab-nav="1"]' in css


def test_back_bar_renders_independently_of_viewport_probe() -> None:
    source = inspect.getsource(landing_page.render_responsive_navigation)
    assert "render_mobile_back_home_bar" in source
    back_block = source.split("is_mobile_tablet_viewport()")[0]
    assert "render_mobile_back_home_bar" in back_block


def test_desktop_skips_mobile_inner_top_bar() -> None:
    source = inspect.getsource(landing_page.render_responsive_navigation)
    assert "render_mobile_inner_top_bar" in source
    assert "is_mobile_tablet_viewport()" in source
    assert "render_desktop_sidebar_nav()" in source
    mobile_block = source.split("render_desktop_sidebar_nav()")[0]
    assert "render_mobile_inner_top_bar" in mobile_block


def test_inner_top_bar_uses_compact_row() -> None:
    source = inspect.getsource(landing_page.render_mobile_inner_top_bar)
    assert "scoop-mobile-inner-top" in source
    assert "scoop-mobile-inner-top-toggle" in source
    assert "← Back to Home" not in source
    assert "scoop-mobile-back-home-spacer" not in source


def main() -> int:
    tests = [
        test_back_link_helper_renders_for_inner_pages,
        test_all_inner_pages_use_responsive_navigation,
        test_landing_skips_back_link,
        test_analyze_has_market_back_button,
        test_back_link_hidden_on_desktop_via_tab_nav,
        test_back_bar_renders_independently_of_viewport_probe,
        test_desktop_skips_mobile_inner_top_bar,
        test_inner_top_bar_uses_compact_row,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} mobile back navigation wiring checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
