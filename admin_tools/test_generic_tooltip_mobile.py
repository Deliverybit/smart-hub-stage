#!/usr/bin/env python3
"""Verify mobile/tablet generic tooltips mirror desktop CSS hover behavior."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import (  # noqa: E402
    IPAD_MINI_POPUP_CLAMP_CSS,
    NAME_VALUE_TOOLTIP_PAGE_SNIPPET,
    RESPONSIVE_GENERIC_TOOLTIP_LAYOUT,
    RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS,
)
from tooltip_scroll import (  # noqa: E402
    GENERIC_TOOLTIP_CSS_VERSION,
    TOOLTIP_SCRIPT_VERSION,
    _DESKTOP_TOOLTIP_TYPE_CSS,
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


def test_name_value_tooltips_use_standard_popup_layout() -> None:
    css = RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
    assert ".fr-val .tip-wrap:not(.headlines-tip) .tip-text" in css
    assert "position: relative !important" in css
    assert "bottom: calc(100% + 12px)" in css
    assert "margin-top: 12px !important" not in css
    assert "position: static !important" not in css
    assert ":focus-within" in css
    # Company tips inherit generic fr-val rules — no duplicate name-only popup block.
    assert css.count('td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip),') == 0


def test_name_tooltip_override_css_and_page_snippet() -> None:
    css = RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    assert "scoop-name-tip-active" not in css
    assert "margin-top: 12px !important" not in css
    assert "@media (max-width: 768px)" in css
    assert "@media (max-width: 375px)" in css
    assert "@media (min-width: 376px) and (max-width: 768px)" in css
    assert "@media (min-width: 769px) and (max-width: 1366px)" in css
    assert "position: fixed !important" in css
    assert "--scoop-mobile-tip-top" in css
    assert "translateX(-50%)" in css
    assert ".tip-wrap:not(.headlines-tip) .tip-text" in css
    assert "background: #1e1e2f !important" in css
    assert "scoop-mobile-tip-open" in css
    assert ".scoop-mobile-tip-open .tip-text" in css
    assert NAME_VALUE_TOOLTIP_PAGE_SNIPPET == ""


def test_tablet_tooltip_layout_unchanged() -> None:
    css = RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
    assert "position: absolute !important" in css
    assert "bottom: calc(100% + 12px)" in css
    assert "position: fixed !important" not in css


def test_tablet_generic_tips_use_ipad_mini_fixed_popup() -> None:
    css = RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    tablet_start = css.index("@media (min-width: 769px) and (max-width: 1366px)")
    phone_start = css.index("@media (max-width: 768px)")
    tablet = css[tablet_start:]
    phone = css[phone_start:tablet_start]
    assert "position: fixed !important" in tablet
    assert "--scoop-mobile-tip-top" in tablet
    assert "scoop-mobile-tip-open" in tablet
    assert "translateX(-50%)" in tablet
    assert "background: #1e1e2f !important" in tablet
    assert phone_start < tablet_start
    assert "position: fixed !important" in phone


def test_name_value_tip_selectors_include_tip_text_for_each_label() -> None:
    from admin_tools.tablet_mobile_layout_css import _name_value_tip_selectors

    scoped = _name_value_tip_selectors(
        'body .stApp [data-testid="stAppViewContainer"] .stMarkdown', " .tip-text"
    )
    assert scoped.count(".tip-text") == 3
    assert 'td[data-label="Company"]' in scoped
    assert 'td[data-label="Name"]' in scoped
    assert 'td[data-label="Commodity"]' in scoped
    assert (
        'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip), '
        'body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap'
        not in scoped
    )


def test_mobile_tooltip_js_clears_legacy_fixed_positioning() -> None:
    js = _GENERIC_TOOLTIP_DESKTOP_HOVER_RESET_JS
    assert "__scoopGenericTooltipBindVersion === 7" in js or "VERSION = 7" in js
    assert "positionNameTipInViewport" not in js
    assert "bindNameValueTips" not in js
    assert "removeProperty" in js
    assert "generic-tip-open" in js
    assert "handleGenericTooltipOver" not in js


def test_dark_name_value_underline_beats_page_css() -> None:
    from admin_tools.dark_mode_css import DARK_MODE_CSS
    from admin_tools.tablet_mobile_layout_css import DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS

    assert DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS.strip() in DARK_MODE_CSS
    assert 'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip)' in DARK_MODE_CSS
    assert "border-bottom: 2px dashed #ffffff !important" in DARK_MODE_CSS
    assert '[data-testid="stAppViewContainer"]' in DARK_MODE_CSS
    assert "@media (max-width: 1366px)" in DARK_MODE_CSS


def test_mobile_generic_tip_positioning_js() -> None:
    js = _TOOLTIP_SCROLL_JS
    assert "MOBILE_GENERIC_TIP_MAX = 768" in js
    assert "TABLET_GENERIC_TIP_MIN = 769" in js
    assert "isTabletGenericTipViewport" in js
    assert "isTapGenericTipViewport" in js
    assert "bindTabletGenericTips" in js
    assert "openTabletGenericTip" in js
    assert "IPHONE_SE_MAX = 375" in js
    assert "isOtherMobileViewport" in js
    assert "positionMobileGenericTip" in js
    assert "applyIphoneSEHorizontalCenter" in js
    assert "applyOtherMobileHorizontalCenter" in js
    assert "--scoop-mobile-tip-top" in js
    assert "bindMobileGenericTips" in js
    assert "scoop-mobile-tip-open" in js
    assert "closeAllMobileGenericTips" in js
    assert "openMobileGenericTip" in js
    assert "__scoopMobileGenericTipBindVersion === 7" in js
    assert "__scoopTabletGenericTipBindVersion === 1" in js
    assert 'addEventListener("pointerenter"' not in js


def test_tablet_generic_tip_reliability_css() -> None:
    css = RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS
    tablet_start = css.index("@media (min-width: 769px) and (max-width: 1366px)")
    tablet = css[tablet_start:]
    assert "html.scoop-tooltip-scrolling" in tablet
    assert "scoop-mobile-tip-open" in tablet
    assert "html body .stApp [data-testid=\"stAppViewContainer\"] .stMarkdown" in tablet
    assert ":not(.scoop-mobile-tip-open):hover .tip-text" in tablet


def test_ipad_mini_popup_clamp_css() -> None:
    css = IPAD_MINI_POPUP_CLAMP_CSS
    assert "@media (min-width: 744px) and (max-width: 768px)" in css
    assert "scoop-mobile-tip-open" in css
    assert "hl-tip-cb:checked" in css
    assert "overflow-y: auto !important" in css
    assert "100dvh" in css
    assert "769px" not in css
    assert "transform: none !important" not in css
    assert "html.scoop-tooltip-scrolling" not in css
    assert "--hl-fixed-top, 90px" in css
    assert "90px - 30px" in css
    assert "min(20rem, calc(100vw - 1.5rem))" in css


def test_ipad_mini_popup_clamp_js() -> None:
    js = _TOOLTIP_SCROLL_JS
    assert "clampIpadMiniGenericTipInViewport" in js
    assert "centerIpadMiniGenericTipInViewport" not in js
    assert "getIpadMiniHeadlinesSlot" in js
    assert "getIpadMiniHeadlinesSlot()" in js
    assert "IPAD_MINI_HEADLINES_TOP = 90" in js
    assert "IPAD_MINI_HEADLINES_BOTTOM = 30" in js
    assert "IPAD_MINI_HEADLINES_MAX_WIDTH" in js
    assert "getTabletNarrowCenteredHeadlinesSlot" not in js
    assert "isTabletNarrowCenteredHeadlinesViewport" not in js
    assert "cardRect" not in js.split("getIpadMiniHeadlinesSlot")[1].split("const clampIpadMiniGenericTipInViewport")[0]
    assert "isIpadMiniViewport()" in js
    assert "__scoopMobileGenericTipBindVersion === 7" in js


def test_version_bumps_for_asset_refresh() -> None:
    assert GENERIC_TOOLTIP_CSS_VERSION >= 27
    assert TOOLTIP_SCRIPT_VERSION >= 41


def test_ipad_mini_headlines_use_tablet_pro_popup() -> None:
    assert "@media (max-width: 743px)" in _MOBILE_HEADLINES_CSS
    assert "744px" in _IPAD_MINI_HEADLINES_CSS
    assert "768px" in _IPAD_MINI_HEADLINES_CSS
    assert _TABLET_HEADLINES_POPUP_RULES.strip() in _IPAD_MINI_HEADLINES_CSS
    assert "position: fixed !important" in _IPAD_MINI_HEADLINES_CSS
    assert "isIpadMiniViewport()" in _TOOLTIP_SCROLL_JS
    assert "isResponsiveHeadlinesViewport() || isIpadMiniViewport()" in _TOOLTIP_SCROLL_JS


def test_desktop_tooltip_type_css_larger_fonts() -> None:
    css = _DESKTOP_TOOLTIP_TYPE_CSS
    assert "@media (min-width: 1367px)" in css
    assert "font-size: 1.25rem !important" in css
    assert "font-size: 1.65rem !important" in css
    assert "min-width: 24rem !important" in css
    assert "scoop-desktop-tooltip-type-css" not in css
    assert "max-width: 1366px" not in css


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
        test_name_value_tooltips_use_standard_popup_layout,
        test_name_tooltip_override_css_and_page_snippet,
        test_tablet_tooltip_layout_unchanged,
        test_tablet_generic_tips_use_ipad_mini_fixed_popup,
        test_tablet_generic_tip_reliability_css,
        test_name_value_tip_selectors_include_tip_text_for_each_label,
        test_mobile_generic_tip_positioning_js,
        test_dark_name_value_underline_beats_page_css,
        test_mobile_tooltip_js_clears_legacy_fixed_positioning,
        test_ipad_mini_headlines_use_tablet_pro_popup,
        test_ipad_mini_popup_clamp_css,
        test_ipad_mini_popup_clamp_js,
        test_desktop_tooltip_type_css_larger_fonts,
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
