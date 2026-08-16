"""Shared helpers for Full Results table columns (Top 10 screener pages)."""

from __future__ import annotations

import html
from urllib.parse import quote

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
    """Relative Analyze URL with ticker (works on Cloud ~/+/ paths if click JS is skipped)."""
    sym = str(source_ticker).strip()
    return f"Analyze?ticker={quote(sym, safe='')}"


def analyze_link_html(source_ticker: str) -> str:
    """HTML for the Analyze column cell (desktop link + mobile/tablet tooltip)."""
    sym = str(source_ticker).strip()
    url = analyze_search_url(sym)
    sym_esc = html.escape(sym, quote=True)
    url_esc = html.escape(url, quote=True)
    tip_esc = html.escape(ANALYZE_COLUMN_TIP)
    link = (
        f'<a class="fr-analyze-link" href="{url_esc}" data-ticker="{sym_esc}" '
        f'target="_self" rel="noopener">Analyze</a>'
    )
    mobile_tip = (
        f'<span class="tip-wrap fr-analyze-mobile-tip" style="display:none">Analyze'
        f'<span class="tip-text">{tip_esc}</span></span>'
    )
    return f'<span class="fr-analyze-cell">{link}{mobile_tip}</span>'
