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


def test_tab_nav_hides_sidebar_controls_on_mobile() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_SIDEBAR_BOOTSTRAP,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
    )

    css = RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert "html[data-scoop-tab-nav=\"1\"] [data-testid=\"stExpandSidebarButton\"]" in css
    assert "html[data-scoop-tab-nav=\"1\"] [data-testid=\"collapsedControl\"]" in css
    assert "left: -9999px !important" in css
    assert 'html:not([data-scoop-tab-nav="1"])' in RESPONSIVE_SIDEBAR_BOOTSTRAP


def test_shared_mobile_tablet_toggle_in_tab_nav_bootstrap() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        MOBILE_TABLET_TOGGLE_STYLE,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _MOBILE_TAB_TOGGLE_WRAP,
    )

    assert MOBILE_TABLET_TOGGLE_STYLE in RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert 'html[data-scoop-tab-nav="1"][data-scoop-home-page="1"]' in RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert _MOBILE_TAB_TOGGLE_WRAP.split(",")[0].strip() in RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert ".scoop-mobile-inner-top-toggle" in RESPONSIVE_TAB_NAV_BOOTSTRAP


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


def test_landing_uses_sidebar_style_home() -> None:
    import inspect

    home_source = inspect.getsource(landing_page.render_mobile_tablet_home)
    assert "sidebar-brand" in home_source
    assert "sidebar-brand-text" in home_source
    assert "scoop-mobile-inner-top-toggle" in home_source
    assert "Dark mode" in home_source
    assert 'st.markdown("---")' in home_source
    assert "SCOOP_52_DESCRIPTION" in home_source
    assert "HOME_NAV_MARKETS" in home_source
    assert "Welcome to The Scoop 52" not in home_source
    assert "scoop-mobile-home-title" not in home_source
    assert "use_container_width=True" in home_source
    assert "render_mobile_tab_nav_shell" not in home_source


def test_home_landing_page_css_scoped() -> None:
    from admin_tools.tablet_mobile_layout_css import (
        RESPONSIVE_HOME_LANDING,
        RESPONSIVE_TAB_NAV_BOOTSTRAP,
        _DESKTOP_MARKET_NAV_GAP,
        _HOME_LOGO_MAX,
        _HOME_MARKET_NAV_GAP_SPACER_RULES,
        _HOME_MARKET_NAV_LIGHT_RULES,
        _MOBILE_TAB_TOGGLE_WRAP,
        _mirror_sidebar_nav_css_for_home,
    )

    css = RESPONSIVE_HOME_LANDING
    bootstrap = RESPONSIVE_TAB_NAV_BOOTSTRAP
    assert 'html[data-scoop-home-page="1"]' in css
    assert ".sidebar-brand-text" in css
    assert "--scoop-home-side-padding: 20px" in css
    assert _HOME_LOGO_MAX in css
    assert "background: #ffffff !important" in css
    assert "clamp(300px, 38vw, 420px)" in css
    assert "clamp(2rem, 10vw, 3.75rem)" in css
    assert "background: transparent !important" in bootstrap
    assert "display: none !important" in bootstrap
    assert "html[data-scoop-home-page=\"1\"]" in bootstrap
    assert "border-radius: 999px !important" in bootstrap
    assert "width: fit-content !important" in bootstrap
    assert "clamp(0.78rem, 2.2vw, 0.88rem)" in bootstrap
    assert "background: #0f172a !important" in bootstrap
    assert "border: 1px solid #334155 !important" in bootstrap
    assert "color: #e2e8f0 !important" in bootstrap
    assert "scoop-mobile-inner-top-toggle" in bootstrap
    assert 'div[data-testid="stToggle"]' in bootstrap
    assert "_MOBILE_TABLET_DARK_MODE_PILL_LAYOUT_FINAL" not in bootstrap
    assert "margin-left: auto !important" in bootstrap
    assert "margin-top: 12px !important" in css
    assert "padding-left: var(--scoop-home-side-padding, 20px)" in css
    assert "#111827" in css
    assert "#f0f2f6" in css
    assert _DESKTOP_MARKET_NAV_GAP in css
    assert _HOME_MARKET_NAV_GAP_SPACER_RULES.strip() in css
    assert 'a[href*="Top_10"]' in css
    assert _HOME_MARKET_NAV_LIGHT_RULES.strip() in css
    assert 'html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"]' in _HOME_MARKET_NAV_LIGHT_RULES
    assert "html:not([data-scoop-theme=\"dark\"]) html[data-scoop-home-page=\"1\"]" not in _HOME_MARKET_NAV_LIGHT_RULES
    assert "Terms_of_Service" in css


def test_back_home_helper_skips_on_landing() -> None:
    import inspect

    source = inspect.getsource(landing_page.render_mobile_back_home_bar)
    assert "HOME_PAGE" in source
    assert "scoop-mobile-back-home-bar" in source


def main() -> int:
    tests = [
        test_shared_mobile_tablet_toggle_in_tab_nav_bootstrap,
        test_tab_nav_hides_sidebar_on_mobile,
        test_tab_nav_hides_sidebar_controls_on_mobile,
        test_tab_nav_shell_hidden_on_desktop,
        test_app_nav_pages_include_home_and_markets,
        test_mobile_tablet_defaults_mobile_safe,
        test_landing_uses_sidebar_style_home,
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
