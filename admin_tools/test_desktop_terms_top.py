"""Desktop Terms page top spacing: compact padding, bootstrap collapse."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import (  # noqa: E402
    DESKTOP_TERMS_TOP_COMPACT,
    RESPONSIVE_TERMS_TOP_COMPACT,
)


def test_desktop_terms_top_compact_scoped_to_desktop() -> None:
    css = DESKTOP_TERMS_TOP_COMPACT
    assert "@media (min-width: 1367px)" in css
    assert 'html[data-scoop-desktop-layout="1"][data-scoop-terms-active="1"]' in css


def test_desktop_terms_top_compact_targets_active_flag() -> None:
    css = DESKTOP_TERMS_TOP_COMPACT
    assert 'html[data-scoop-terms-active="1"]' in css
    assert "padding-top: 12px !important" in css
    assert "gap: 0 !important" in css
    assert "streamlit_js_eval" in css


def test_desktop_terms_top_compact_does_not_touch_mobile() -> None:
    css = DESKTOP_TERMS_TOP_COMPACT
    assert "@media (max-width:" not in css


def test_responsive_and_desktop_terms_rules_are_separate() -> None:
    assert "@media (max-width: 1366px)" in RESPONSIVE_TERMS_TOP_COMPACT
    assert "padding-top: 12px !important" not in RESPONSIVE_TERMS_TOP_COMPACT


def test_terms_page_included_in_desktop_header_padding_sync() -> None:
    js = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "const termsActive = /Terms_of_Service/i.test(appWin.location.pathname || \"\");" in js
    assert "analyzeActive || screenerActive || termsActive" in js


if __name__ == "__main__":
    tests = [
        test_desktop_terms_top_compact_scoped_to_desktop,
        test_desktop_terms_top_compact_targets_active_flag,
        test_desktop_terms_top_compact_does_not_touch_mobile,
        test_responsive_and_desktop_terms_rules_are_separate,
        test_terms_page_included_in_desktop_header_padding_sync,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} desktop terms top checks passed.")
