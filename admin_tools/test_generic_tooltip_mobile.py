#!/usr/bin/env python3
"""Verify mobile/tablet generic tooltips mirror desktop CSS hover behavior."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import (  # noqa: E402
    NAME_VALUE_TOOLTIP_PAGE_MARKER,
    NAME_VALUE_TOOLTIP_PAGE_SNIPPET,
    RESPONSIVE_GENERIC_TOOLTIP_LAYOUT,
    RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS,
)
from tooltip_scroll import (  # noqa: E402
    GENERIC_TOOLTIP_CSS_VERSION,
    TOOLTIP_SCRIPT_VERSION,
    _GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS,
    _IPAD_MINI_HEADLINES_CSS,
    _MOBILE_HEADLINES_CSS,
    _MOBILE_PHONE_HEADLINES_FIXED_CSS,
    _TABLET_HEADLINES_POPUP_RULES,
    _TOOLTIP_SCROLL_JS,
)


def test_mobile_tooltip_css_uses_desktop_hover_layout() -> None:
    css = RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
    assert "position: absolute !important" in css
    assert "bottom: calc(100% + 12px)" in css
    assert "position: fixed !important" not in css
    assert "generic-tip-open" not in css
    assert ":hover .tip-text" in css
    assert ":active .tip-text" in css
    assert ".tip-text::before" in css
    assert "display: block !important" in css


def test_name_value_tooltips_open_below_on_mobile_tablet() -> None:
    css = RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
    assert 'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip)' in css
    assert 'td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip)' in css
    assert "top: 100% !important" in css
    assert "left: 0 !important" in css
    assert "right: 0 !important" in css
    assert "position: static !important" in css
    assert ":focus-within" in css


def test_name_tooltip_override_css_and_page_snippet() -> None:
    assert "scoop-name-tip-active" in RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    assert "left: 0 !important" in RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    assert NAME_VALUE_TOOLTIP_PAGE_MARKER in NAME_VALUE_TOOLTIP_PAGE_SNIPPET
    assert 'td[data-label="Company"]' in NAME_VALUE_TOOLTIP_PAGE_SNIPPET


def test_mobile_tooltip_js_clears_legacy_fixed_positioning() -> None:
    js = _GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS
    assert "__scoopGenericTooltipBindVersion === 6" in js or "VERSION = 6" in js
    assert "positionNameTipInViewport" in js
    assert "bindNameValueTips" in js
    assert "scoop-name-tip-active" in js
    assert "removeProperty" in js
    assert "generic-tip-open" in js
    assert "handleGenericTooltipOver" not in js


def test_version_bumps_for_asset_refresh() -> None:
    assert GENERIC_TOOLTIP_CSS_VERSION >= 7
    assert TOOLTIP_SCRIPT_VERSION >= 12


def test_ipad_mini_headlines_use_tablet_pro_popup() -> None:
    assert "@media (max-width: 743px)" in _MOBILE_HEADLINES_CSS
    assert "744px" in _IPAD_MINI_HEADLINES_CSS
    assert "768px" in _IPAD_MINI_HEADLINES_CSS
    assert _TABLET_HEADLINES_POPUP_RULES.strip() in _IPAD_MINI_HEADLINES_CSS
    assert "position: fixed !important" in _IPAD_MINI_HEADLINES_CSS
    assert "isIpadMiniViewport()" in _TOOLTIP_SCROLL_JS
    assert "isResponsiveHeadlinesViewport() || isIpadMiniViewport()" in _TOOLTIP_SCROLL_JS


def test_phone_mobile_headlines_top_panel() -> None:
    css = _MOBILE_PHONE_HEADLINES_FIXED_CSS
    js = _TOOLTIP_SCROLL_JS
    assert "@media (max-width: 743px)" in css
    assert "position: fixed !important" in css
    assert ".hl-tip-heading" in css
    assert "position: relative !important" in css
    assert "margin-top: 0 !important" in css
    assert "MOBILE_HEADLINES_CARD_WIDTH_INSET" in js
    assert "getPhoneMobileHeadlinesSlot(wrap)" in js
    assert "cardRect.width - MOBILE_HEADLINES_CARD_WIDTH_INSET" in js
    assert "syncPhoneMobileHeadlinesHeadingInset" not in js
    assert "const MOBILE_MAX = 743" in js


def main() -> int:
    tests = [
        test_mobile_tooltip_css_uses_desktop_hover_layout,
        test_name_value_tooltips_open_below_on_mobile_tablet,
        test_name_tooltip_override_css_and_page_snippet,
        test_mobile_tooltip_js_clears_legacy_fixed_positioning,
        test_ipad_mini_headlines_use_tablet_pro_popup,
        test_phone_mobile_headlines_top_panel,
        test_version_bumps_for_asset_refresh,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} generic tooltip mobile checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
