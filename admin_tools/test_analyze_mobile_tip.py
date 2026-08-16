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

from admin_tools.tablet_mobile_layout_css import TABLET_SCREENER_MOBILE_LAYOUT  # noqa: E402
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
    css = TABLET_SCREENER_MOBILE_LAYOUT
    assert ".fr-analyze-cell .fr-analyze-link" in css
    assert "display: none !important" in css
    assert ".fr-analyze-cell .fr-analyze-mobile-tip" in css
    assert "display: inline-block !important" in css
    assert "text-decoration: none !important" in css
    # Old mobile hyperlink styling should be gone.
    assert re.search(r"\.fr-analyze-link:hover\s*\{[^}]*underline", css) is None


def test_desktop_css_does_not_hide_analyze_link() -> None:
    from admin_tools.tablet_mobile_layout_css import DESKTOP_SIDEBAR_LAYOUT

    assert "fr-analyze-link" not in DESKTOP_SIDEBAR_LAYOUT
    assert "fr-analyze-mobile-tip" not in DESKTOP_SIDEBAR_LAYOUT


def test_analyze_click_js_skips_mobile_tablet() -> None:
    js = _inject_responsive_bootstrap_css()
    assert "innerWidth || 0) < 1367" in js
    assert "fr-analyze-link" in js


def main() -> int:
    tests = [
        test_analyze_html_has_desktop_link_and_mobile_tip,
        test_mobile_css_hides_link_shows_tip,
        test_desktop_css_does_not_hide_analyze_link,
        test_analyze_click_js_skips_mobile_tablet,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} Analyze mobile/tablet checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
