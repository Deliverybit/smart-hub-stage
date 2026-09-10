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


def analyze_search_url(source_ticker: str, *, from_path: str = "") -> str:
    """Relative Analyze URL with ticker (works on Cloud ~/+/ paths if click JS is skipped)."""
    sym = str(source_ticker).strip()
    url = f"Analyze?ticker={quote(sym, safe='')}"
    source = str(from_path or "").strip()
    if source:
        if not source.startswith("/"):
            source = f"/{source}"
        url = f"{url}&from={quote(source, safe='')}"
    return url


def analyze_link_html(source_ticker: str, *, from_path: str = "") -> str:
    """HTML for the Analyze column cell (desktop link + mobile/tablet tooltip)."""
    sym = str(source_ticker).strip()
    url = analyze_search_url(sym, from_path=from_path)
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


def render_full_results_heading(st_module, compact_title: str) -> None:
    """Show the market Top 10 title in place of Full Results."""
    title = html.escape(str(compact_title).strip() or "Top 10")
    st_module.markdown(
        f"""
        <style>
        .scoop-fr-heading-wrap {{
            padding-top: 24px !important;
            padding-bottom: 24px !important;
            box-sizing: border-box !important;
        }}
        .scoop-full-results-heading {{
            margin-top: 24px !important;
            margin-bottom: 24px !important;
        }}
        .scoop-fr-heading-wrap .scoop-full-results-heading {{
            margin-top: 0 !important;
            margin-bottom: 0 !important;
        }}
        .scoop-fr-heading-spacer {{
            display: none !important;
            height: 0 !important;
        }}
        [data-testid="stElementContainer"]:has(.scoop-full-results-heading),
        [data-testid="element-container"]:has(.scoop-full-results-heading) {{
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }}
        @media (max-width: 1366px) {{
            .scoop-full-results-heading,
            .scoop-full-results-heading .scoop-fr-title-box {{
                font-weight: 800 !important;
            }}
            html[data-scoop-theme="dark"] .scoop-full-results-heading {{
                background: transparent !important;
                border: none !important;
                padding: 0 !important;
            }}
            html[data-scoop-theme="dark"] body .stApp .scoop-full-results-heading .scoop-fr-title-box {{
                display: inline-block !important;
                border: 2px solid #ffffff !important;
                border-radius: 10px !important;
                padding: 0.2em 0.55em !important;
                background: #ffffff !important;
                color: #0f172a !important;
                box-sizing: border-box !important;
                font-weight: 800 !important;
            }}
        }}
        @media (min-width: 1367px) {{
            .scoop-fr-heading-wrap {{
                padding-top: 40px !important;
                padding-bottom: 0 !important;
            }}
            .scoop-full-results-heading {{
                margin-top: 40px !important;
                margin-bottom: 0 !important;
            }}
            .scoop-fr-heading-wrap .scoop-full-results-heading {{
                margin-top: 0 !important;
                margin-bottom: 0 !important;
            }}
            .scoop-fr-heading-spacer {{
                display: block !important;
                height: 40px !important;
                width: 100% !important;
            }}
        }}
        .scoop-full-results-heading .scoop-fr-title-box {{
            font-size: inherit !important;
            line-height: inherit !important;
        }}
        html:not([data-scoop-theme="dark"]) .scoop-full-results-heading {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        html:not([data-scoop-theme="dark"]) body .stApp .scoop-full-results-heading .scoop-fr-title-box {{
            display: inline-block !important;
            border: 2px solid #22c55e !important;
            border-radius: 10px !important;
            padding: 0.2em 0.55em !important;
            background: #f0fdf4 !important;
            box-sizing: border-box !important;
        }}
        html[data-scoop-theme="dark"] .scoop-full-results-heading {{
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }}
        html[data-scoop-theme="dark"] body .stApp .scoop-full-results-heading .scoop-fr-title-box {{
            display: inline-block !important;
            border: 2px solid #ffffff !important;
            border-radius: 10px !important;
            padding: 0.2em 0.55em !important;
            background: #ffffff !important;
            color: #0f172a !important;
            box-sizing: border-box !important;
        }}
        </style>
        <div class="scoop-fr-heading-wrap"><h3 class="scoop-full-results-heading"><span class="scoop-fr-title-box">📋 {title}</span></h3><div class="scoop-fr-heading-spacer" aria-hidden="true"></div></div>
        """,
        unsafe_allow_html=True,
    )
