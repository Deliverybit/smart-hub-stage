"""Mobile/tablet Analyze top spacing: compact gaps, js_eval collapse, hr hide."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from admin_tools.tablet_mobile_layout_css import RESPONSIVE_ANALYZE_TOP_COMPACT  # noqa: E402


def test_analyze_top_compact_scoped_to_mobile_tablet() -> None:
    css = RESPONSIVE_ANALYZE_TOP_COMPACT
    assert "@media (max-width: 1366px)" in css
    assert "@media (min-width: 1367px)" not in css


def test_analyze_top_compact_targets_active_flag() -> None:
    css = RESPONSIVE_ANALYZE_TOP_COMPACT
    assert 'html[data-scoop-analyze-active="1"]' in css
    assert "streamlit_js_eval" in css
    assert "hr:not(.search-52w-range-divider)" in css
    assert '[data-testid="stHtml"]' in css
    assert "gap: 0 !important" in css


def test_analyze_top_compact_hides_hr_only_containers() -> None:
    css = RESPONSIVE_ANALYZE_TOP_COMPACT
    assert 'stMarkdownContainer"] hr:not(.search-52w-range-divider))' in css


def test_analyze_top_compact_does_not_touch_desktop() -> None:
    css = RESPONSIVE_ANALYZE_TOP_COMPACT
    assert 'html[data-scoop-desktop-layout="1"]' not in css


if __name__ == "__main__":
    tests = [
        test_analyze_top_compact_scoped_to_mobile_tablet,
        test_analyze_top_compact_targets_active_flag,
        test_analyze_top_compact_hides_hr_only_containers,
        test_analyze_top_compact_does_not_touch_desktop,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} responsive analyze top checks passed.")
