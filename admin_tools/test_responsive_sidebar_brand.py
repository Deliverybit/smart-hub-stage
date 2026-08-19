"""Sidebar brand ↔ dark mode ↔ first nav link spacing (mobile/tablet + desktop)."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import (  # noqa: E402
    DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER,
    RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER,
    SIDEBAR_NAV_COMPACT,
)


def test_brand_toggle_buffer_scoped_to_mobile_tablet() -> None:
    css = RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert "@media (max-width: 1366px)" in css
    assert ".sidebar-brand" in css
    assert 'div[data-testid="stCheckbox"]' in css


def test_brand_toggle_buffer_scoped_to_desktop() -> None:
    css = DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert "@media (min-width: 1367px)" in css
    assert 'html[data-scoop-desktop-layout="1"]' in css


def test_brand_toggle_buffer_increases_spacing() -> None:
    css = RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert "margin-bottom: 0.85rem !important" in css
    assert "margin-top: 0.25rem !important" in css


def test_brand_toggle_buffer_tightens_nav_gap() -> None:
    css = RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert "margin-bottom: 0.1rem !important" in css
    assert "gap: 0.2rem !important" in css
    assert ":has(hr) +" in css


def test_desktop_and_mobile_share_same_spacing_rules() -> None:
    shared = "margin-bottom: 0.85rem !important"
    assert shared in RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert shared in DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER


def test_compact_nav_base_unchanged() -> None:
    css = SIDEBAR_NAV_COMPACT
    assert "@media (max-width:" not in css
    assert "margin-bottom: 0.35rem !important" in css


def test_sidebar_brand_buffer_injected_on_every_page() -> None:
    js = (ROOT / "tooltip_scroll.py").read_text(encoding="utf-8")
    assert "def inject_desktop_sidebar_nav_market" in js
    assert "RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER" in js
    assert "DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER" in js
    start = js.index("def inject_desktop_sidebar_nav_market")
    end = js.index("\n\n", start)
    block = js[start:end]
    assert "scoop-responsive-sidebar-brand-toggle-buffer-css" in block
    assert "scoop-desktop-sidebar-brand-toggle-buffer-css" in block


def test_sidebar_brand_buffer_beats_page_css_specificity() -> None:
    css = DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER
    assert "html body .stApp [data-testid=\"stSidebar\"]" in css


if __name__ == "__main__":
    tests = [
        test_brand_toggle_buffer_scoped_to_mobile_tablet,
        test_brand_toggle_buffer_scoped_to_desktop,
        test_brand_toggle_buffer_increases_spacing,
        test_brand_toggle_buffer_tightens_nav_gap,
        test_desktop_and_mobile_share_same_spacing_rules,
        test_compact_nav_base_unchanged,
        test_sidebar_brand_buffer_injected_on_every_page,
        test_sidebar_brand_buffer_beats_page_css_specificity,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} sidebar brand spacing checks passed.")
