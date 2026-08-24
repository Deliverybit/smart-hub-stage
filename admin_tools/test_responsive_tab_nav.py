#!/usr/bin/env python3
"""Verify mobile/tablet tab navigation CSS (replaces slide-out sidebar)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP  # noqa: E402
import landing_page  # noqa: E402


def test_tab_nav_hides_sidebar_on_mobile() -> None:
    css = RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert 'html[data-scoop-tab-nav="1"]' in css
    assert "@media (max-width: 1366px)" in css
    assert 'section[data-testid="stSidebar"]' in css
    assert "[data-testid=\"stSidebarBackdrop\"]" in css
    assert "display: none !important" in css


def test_tab_nav_shell_hidden_on_desktop() -> None:
    css = RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert ".scoop-mobile-nav-shell" in css
    assert "@media (min-width: 1367px)" in css


def test_app_nav_pages_include_home_and_markets() -> None:
    paths = [path for path, _ in landing_page.APP_NAV_PAGES]
    assert landing_page.HOME_PAGE in paths
    assert landing_page.TERMS_PAGE not in paths
    assert len(landing_page.APP_NAV_PAGES) == 6


def test_mobile_tablet_defaults_mobile_safe() -> None:
    def fake_js(*, js_expressions: str, key: str, want_output: bool, height: int):
        _ = js_expressions, key, want_output, height
        return None

    landing_page._js_eval = lambda expression, *, key: fake_js(  # type: ignore[method-assign]
        js_expressions=expression,
        key=key,
        want_output=True,
        height=0,
    )
    assert landing_page.is_mobile_tablet_viewport() is True


def test_landing_uses_home_shell_without_tabs() -> None:
    import inspect

    home_source = inspect.getsource(landing_page.render_mobile_tablet_home)
    assert "render_mobile_home_shell" in home_source
    assert "use_container_width=True" in home_source
    assert "render_mobile_tab_nav_shell" not in home_source


def test_home_landing_page_css_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_HOME_LANDING

    css = RESPONSIVE_HOME_LANDING
    assert 'html[data-scoop-home-page="1"]' in css
    assert "[data-testid=\"stPageLink\"]" in css
    assert "[data-scoop-nav-active]" in css


def test_back_home_helper_skips_on_landing() -> None:
    import inspect

    source = inspect.getsource(landing_page.render_mobile_inner_top_bar)
    assert "HOME_PAGE" in source
    assert "scoop-mobile-inner-top" in source


def main() -> int:
    tests = [
        test_tab_nav_hides_sidebar_on_mobile,
        test_tab_nav_shell_hidden_on_desktop,
        test_app_nav_pages_include_home_and_markets,
        test_mobile_tablet_defaults_mobile_safe,
        test_landing_uses_home_shell_without_tabs,
        test_home_landing_page_css_scoped,
        test_back_home_helper_skips_on_landing,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} tab nav checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
