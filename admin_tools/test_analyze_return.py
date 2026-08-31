#!/usr/bin/env python3
"""Verify Analyze back navigation marks parent session storage on mobile/tablet."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import analyze_page  # noqa: E402


def test_mark_analyze_return_uses_parent_session_storage() -> None:
    js = analyze_page._mark_analyze_return_js()
    assert "window.parent" in js
    assert "scoop-return-from-analyze" in js
    assert "scoop-landing-seen" in js
    assert "__scoopClearResponsiveExpandTimers" in js


def test_analyze_back_link_marks_return_query() -> None:
    from legal_consent_logger import ANALYZE_RETURN_QUERY_KEY

    href = f"{analyze_page.analyze_back_href('pages/1_NYSE_Top_10.py')}?{ANALYZE_RETURN_QUERY_KEY}=1"
    assert href.endswith(f"?{ANALYZE_RETURN_QUERY_KEY}=1")
    assert "/NYSE_Top_10" in href


def test_normalize_screener_path_accepts_cloud_style_paths() -> None:
    assert analyze_page._normalize_screener_path("/NASDAQ_Top_10") == "/NASDAQ_Top_10"
    assert analyze_page._normalize_screener_path("~/+/NASDAQ_Top_10") == "/NASDAQ_Top_10"
    assert analyze_page._normalize_screener_path("/foo/ICE_Top_10?x=1") == "/ICE_Top_10"
    assert analyze_page._normalize_screener_path("crypto_top_10") == "/Crypto_Top_10"


def test_analyze_back_labels_name_markets_explicitly() -> None:
    labels = {label for _page, label in analyze_page.SCREENER_RETURN_PAGES.values()}
    assert labels == {
        "NYSE Top 10",
        "NASDAQ Top 10",
        "Crypto Top 10",
        "CME Top 10",
        "ICE Top 10",
    }
    assert analyze_page.SCREENER_RETURN_PAGES["/NASDAQ_Top_10"][1] == "NASDAQ Top 10"


def test_analyze_link_includes_ticker_query() -> None:
    from screener_table import analyze_link_html, analyze_search_url

    url = analyze_search_url("BTC-USD", from_path="/Crypto_Top_10")
    assert url.startswith("Analyze?ticker=")
    assert "BTC-USD" in url
    assert "from=%2FCrypto_Top_10" in url or "from=/Crypto_Top_10" in url
    html = analyze_link_html("DOGE-USD", from_path="/NASDAQ_Top_10")
    assert 'data-ticker="DOGE-USD"' in html
    assert "ticker=DOGE-USD" in html
    assert "from=" in html
    assert "NASDAQ_Top_10" in html
    assert 'class="fr-analyze-link"' in html
    assert 'class="tip-wrap fr-analyze-mobile-tip"' in html


def test_analyze_click_js_handles_mobile_targets() -> None:
    from tooltip_scroll import _inject_responsive_bootstrap_css

    js = _inject_responsive_bootstrap_css()
    assert "nodeType" in js
    assert 'td[data-label="Analyze"]' in js
    assert 'new URL("Analyze"' in js
    assert "appDoc.querySelector" in js
    assert "scoop-analyze-from" in js
    assert "NASDAQ_Top_10" in js


def main() -> int:
    tests = [
        test_mark_analyze_return_uses_parent_session_storage,
        test_analyze_back_link_marks_return_query,
        test_normalize_screener_path_accepts_cloud_style_paths,
        test_analyze_back_labels_name_markets_explicitly,
        test_analyze_link_includes_ticker_query,
        test_analyze_click_js_handles_mobile_targets,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} analyze return checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
