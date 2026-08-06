"""Shared helpers for Full Results table columns (Top 10 screener pages)."""

from __future__ import annotations

import html

from analyze_page import ANALYZE_PAGE_PATH


ANALYZE_COLUMN = "Analyze"

ANALYZE_COLUMN_TIP = (
    "Open a detailed Analyze dashboard for this symbol — price history, "
    "headline sentiment, and related scores."
)


def build_source_ticker_map(df) -> dict[str, str]:
    """Map display Ticker labels to API-ready symbols (e.g. BTC → BTC-USD)."""
    return {
        str(row["Ticker"]): str(row.get("_source_ticker") or row["Ticker"])
        for _, row in df.iterrows()
    }


def analyze_search_url(source_ticker: str) -> str:
    """Analyze page path (ticker travels via data-ticker; query params are stripped from HTML hrefs)."""
    return ANALYZE_PAGE_PATH


def analyze_link_html(source_ticker: str) -> str:
    """HTML anchor for the Analyze column cell."""
    sym = str(source_ticker).strip()
    url = analyze_search_url(sym)
    sym_esc = html.escape(sym, quote=True)
    url_esc = html.escape(url, quote=True)
    return (
        f'<a class="fr-analyze-link" href="{url_esc}" data-ticker="{sym_esc}" '
        f'target="_self" rel="noopener">Analyze</a>'
    )
