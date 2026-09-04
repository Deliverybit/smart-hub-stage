"""Mobile/tablet screener landing intro: compact copy and responsive CSS."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from screener_selection import (  # noqa: E402
    _SCREENER_LANDING_INTRO_CSS,
    _landing_markdown_html,
    proximity_how_it_works,
    proximity_how_it_works_compact,
    render_screener_landing_intro,
    screener_landing_summary,
    sentiment_negative_keyword_notice,
    sentiment_negative_keyword_notice_compact,
)


def test_compact_summary_shorter_than_full_for_all_markets() -> None:
    for market in ("NYSE", "NASDAQ", "CRYPTO", "CME", "ICE"):
        full = screener_landing_summary(market, 70, compact=False)
        compact = screener_landing_summary(market, 70, compact=True)
        assert len(compact) < len(full)
        assert "70" in compact


def test_compact_how_it_works_and_sentiment_are_shorter() -> None:
    how_full = proximity_how_it_works("stock")
    how_compact = proximity_how_it_works_compact("stock")
    sent_full = sentiment_negative_keyword_notice("stock")
    sent_compact = sentiment_negative_keyword_notice_compact("stock")
    assert len(how_compact) < len(how_full)
    assert len(sent_compact) < len(sent_full)
    assert "30%" in how_compact
    assert "red-flag" in sent_compact.lower()


def test_landing_css_shows_compact_on_desktop() -> None:
    css = _SCREENER_LANDING_INTRO_CSS
    assert ".scoop-landing-full { display: none; }" in css
    assert ".scoop-landing-compact { display: block; }" in css


def test_landing_css_mobile_tablet_adds_spacing() -> None:
    css = _SCREENER_LANDING_INTRO_CSS
    assert "@media (max-width: 1366px)" in css
    assert "margin-bottom: 0.8rem" in css
    assert "margin-bottom: 0.45rem" not in css
    assert ".scoop-screener-last-updated" in css
    assert 'html:not([data-scoop-screener-gated="1"]) .scoop-landing-info' in css


def test_landing_css_desktop_adds_spacing() -> None:
    css = _SCREENER_LANDING_INTRO_CSS
    assert "@media (min-width: 1367px)" in css
    assert "margin-bottom: 0.9rem" in css
    assert "margin-bottom: 1.1rem" in css


def test_landing_markdown_html_bolds_text() -> None:
    assert _landing_markdown_html("**70** stocks") == "<strong>70</strong> stocks"


class _MarkdownStub:
    calls: list[str] = []

    @classmethod
    def markdown(cls, body: str, *, unsafe_allow_html: bool) -> None:
        cls.calls.append(body)


def test_render_screener_landing_intro_includes_both_variants() -> None:
    _MarkdownStub.calls.clear()
    render_screener_landing_intro(
        _MarkdownStub,
        market="NYSE",
        universe_size=70,
        asset_label="stock",
        sentiment_profile="stock",
    )
    body = _MarkdownStub.calls[0]
    assert "scoop-landing-full" in body
    assert "scoop-landing-compact" in body
    assert "NYSE stocks near" in body
    assert "Screens" in body
    assert "How it works:" in body
    assert "Sentiment screening:" in body
    assert "Sentiment:" in body


def main() -> int:
    tests = [
        test_compact_summary_shorter_than_full_for_all_markets,
        test_compact_how_it_works_and_sentiment_are_shorter,
        test_landing_css_shows_compact_on_desktop,
        test_landing_css_mobile_tablet_adds_spacing,
        test_landing_css_desktop_adds_spacing,
        test_landing_markdown_html_bolds_text,
        test_render_screener_landing_intro_includes_both_variants,
    ]
    for fn in tests:
        fn()
        print(f"PASS {fn.__name__}")
    print(f"\nAll {len(tests)} screener landing intro checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
