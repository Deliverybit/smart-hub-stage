"""Desktop Analyze top spacing: compact padding, js_eval collapse, hr hide."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import DESKTOP_ANALYZE_TOP_COMPACT  # noqa: E402


def test_analyze_top_compact_scoped_to_desktop() -> None:
    css = DESKTOP_ANALYZE_TOP_COMPACT
    assert "@media (min-width: 1367px)" in css
    assert 'html[data-scoop-desktop-layout="1"][data-scoop-analyze-active="1"]' in css


def test_analyze_top_compact_targets_active_flag() -> None:
    css = DESKTOP_ANALYZE_TOP_COMPACT
    assert 'html[data-scoop-analyze-active="1"]' in css
    assert "streamlit_js_eval" in css
    assert "hr:not(.search-52w-range-divider)" in css


def test_analyze_top_compact_does_not_touch_mobile() -> None:
    css = DESKTOP_ANALYZE_TOP_COMPACT
    assert "@media (max-width:" not in css


if __name__ == "__main__":
    tests = [
        test_analyze_top_compact_scoped_to_desktop,
        test_analyze_top_compact_targets_active_flag,
        test_analyze_top_compact_does_not_touch_mobile,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} analyze desktop top checks passed.")
