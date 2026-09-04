"""Desktop Headlines popup must show link list without moving the panel."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from tooltip_scroll import _DESKTOP_HEADLINES_CSS


def test_desktop_headlines_css_is_desktop_only() -> None:
    css = _DESKTOP_HEADLINES_CSS
    assert "@media (min-width: 1367px)" in css
    assert "@media (max-width:" not in css


def test_desktop_open_headlines_keep_fixed_slot() -> None:
    css = _DESKTOP_HEADLINES_CSS
    assert "top: var(--hl-fixed-top, -10000px)" in css
    assert "left: var(--hl-fixed-left, -10000px)" in css
    assert "left: var(--hl-fixed-left) !important;" not in css
    assert "min-width: 280px" in css
    assert "position: fixed !important" in css


def test_desktop_open_headlines_show_links() -> None:
    css = _DESKTOP_HEADLINES_CSS
    assert "min-height: 4.5rem !important" in css
    assert "flex: 1 1 auto !important" in css
    assert ".hl-tip-line a" in css
    assert "color: #93c5fd !important" in css
    assert ":not(.hl-tip-desktop-open):not(:has(.hl-tip-cb:checked))" in css


if __name__ == "__main__":
    test_desktop_headlines_css_is_desktop_only()
    test_desktop_open_headlines_keep_fixed_slot()
    test_desktop_open_headlines_show_links()
    print("ok")
