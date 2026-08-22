#!/usr/bin/env python3
"""Verify Analyze column: mobile/tablet tooltip (no link), desktop link unchanged."""

from __future__ import annotations

import html
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import (  # noqa: E402
    PHONE_ANALYZE_MOBILE_TIP_CSS,
    TABLET_ANALYZE_LINK_CSS,
    TABLET_SCREENER_MOBILE_LAYOUT,
)
from screener_table import ANALYZE_COLUMN_TIP, analyze_link_html  # noqa: E402
from tooltip_scroll import _inject_responsive_bootstrap_css  # noqa: E402


def test_analyze_html_has_desktop_link_and_mobile_tip() -> None:
    out = analyze_link_html("NKE")
    assert 'class="fr-analyze-cell"' in out
    assert 'class="fr-analyze-link"' in out
    assert 'href="Analyze?ticker=NKE"' in out
    assert 'data-ticker="NKE"' in out
    assert 'class="tip-wrap fr-analyze-mobile-tip"' in out
    assert 'style="display:none"' in out
    assert html.escape(ANALYZE_COLUMN_TIP) in out


def test_mobile_css_hides_link_shows_tip() -> None:
    css = PHONE_ANALYZE_MOBILE_TIP_CSS
    assert "@media (max-width: 743px)" in css
    assert ".fr-analyze-cell .fr-analyze-link" in css
    assert "display: none !important" in css
    assert ".fr-analyze-cell .fr-analyze-mobile-tip" in css
    assert "display: inline-block !important" in css
    assert "text-decoration: none !important" in css
    layout = TABLET_SCREENER_MOBILE_LAYOUT
    assert re.search(r"\.fr-analyze-link:hover\s*\{[^}]*underline", layout) is None


def test_desktop_css_does_not_hide_analyze_link() -> None:
    from admin_tools.tablet_mobile_layout_css import DESKTOP_SIDEBAR_LAYOUT

    assert "fr-analyze-link" not in DESKTOP_SIDEBAR_LAYOUT
    assert "fr-analyze-mobile-tip" not in DESKTOP_SIDEBAR_LAYOUT


def test_tablet_analyze_link_css() -> None:
    css = TABLET_ANALYZE_LINK_CSS
    assert "@media (min-width: 744px) and (max-width: 1366px)" in css
    assert 'td[data-label="Analyze"]' in css
    assert "border-radius: 10px !important" in css
    assert "border: 1px solid #e5e7eb !important" in css
    assert "text-decoration: underline !important" in css
    assert "color: #2563eb !important" in css
    assert "justify-content: space-between !important" in css
    assert "order: 1 !important" in css
    assert "order: 2 !important" in css
    assert "a.fr-analyze-link" in css
    assert ".fr-analyze-mobile-tip" in css
    assert "display: inline-block !important" in css
    assert "border-bottom: 1px dashed #888 !important" in css
    assert "display: none !important" not in css.split(".fr-analyze-mobile-tip")[1].split("a.fr-analyze-link")[0]


def test_ipad_mini_analyze_uses_tablet_link() -> None:
    css = TABLET_ANALYZE_LINK_CSS
    assert "744px" in css
    assert "1366px" in css
    assert ".fr-analyze-mobile-tip" in css
    assert "a.fr-analyze-link" in css


def test_analyze_click_js_skips_mobile_tablet() -> None:
    js = _inject_responsive_bootstrap_css()
    assert "innerWidth || 0) < 1367" in js
    assert "fr-analyze-link" in js


def test_tablet_analyze_injected_from_tooltip_handler() -> None:
    import inspect

    from tooltip_scroll import install_tooltip_scroll_handler

    source = inspect.getsource(install_tooltip_scroll_handler)
    assert "_inject_tablet_analyze_link_css" in source


def test_all_screener_pages_install_tooltip_handler() -> None:
    pages_dir = ROOT / "pages"
    for path in sorted(pages_dir.glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        assert "install_tooltip_scroll_handler()" in text, f"{path.name} missing handler"
        assert "analyze_link_html" in text, f"{path.name} missing analyze column"


def test_tablet_analyze_css_beats_page_tablet_rules() -> None:
    css = TABLET_ANALYZE_LINK_CSS
    page_rule = (
        ".stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-link"
    )
    injected_rule = (
        'html body .stApp [data-testid="stAppViewContainer"] .stMarkdown'
        " .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link"
    )
    assert page_rule not in css
    assert injected_rule in css
    assert "display: inline !important" in css
    assert ".fr-analyze-mobile-tip" in css and "order: 1 !important" in css
    assert "a.fr-analyze-link" in css and "order: 2 !important" in css
    assert "margin-left: auto !important" in css


def test_tablet_analyze_media_query_covers_all_tablet_viewports() -> None:
    css = TABLET_ANALYZE_LINK_CSS
    assert "@media (min-width: 744px) and (max-width: 1366px)" in css
    phone_css = PHONE_ANALYZE_MOBILE_TIP_CSS
    assert "@media (max-width: 743px)" in phone_css
    assert "order:" not in phone_css
    assert "color: #2563eb" not in phone_css


def main() -> int:
    tests = [
        test_analyze_html_has_desktop_link_and_mobile_tip,
        test_mobile_css_hides_link_shows_tip,
        test_desktop_css_does_not_hide_analyze_link,
        test_tablet_analyze_link_css,
        test_ipad_mini_analyze_uses_tablet_link,
        test_tablet_analyze_injected_from_tooltip_handler,
        test_all_screener_pages_install_tooltip_handler,
        test_tablet_analyze_css_beats_page_tablet_rules,
        test_tablet_analyze_media_query_covers_all_tablet_viewports,
        test_analyze_click_js_skips_mobile_tablet,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} Analyze mobile/tablet checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
