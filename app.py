"""
app.py
Final Live Version: Market Prediction App
Run: python -m streamlit run app.py
"""

from datetime import timedelta

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import html

from predictor import Predictor
from market_data import MarketData
from sentiment_engine import SentimentEngine
from legal_consent_logger import ensure_timezone_cookie, log_terms_acceptance
from branding import logo_path_str, render_environment_banner

# Search price chart: axis tick/title sizes (px in Plotly). Mobile matches existing UI.
_SEARCH_CHART_AXIS_TICK_MOBILE = 26
_SEARCH_CHART_AXIS_TITLE_MOBILE = 28
_SEARCH_CHART_AXIS_TICK_DESKTOP = _SEARCH_CHART_AXIS_TICK_MOBILE + 4
_SEARCH_CHART_AXIS_TITLE_DESKTOP = _SEARCH_CHART_AXIS_TITLE_MOBILE + 4


def _probe_search_chart_viewport() -> None:
    """Read parent viewport width into session_state (sidebar only — avoids a tall iframe gap before the chart)."""
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        return
    w = streamlit_js_eval(
        js_expressions="window.parent.innerWidth",
        key="search_price_chart_viewport_w",
        want_output=True,
        height=0,
    )
    if w is not None:
        try:
            st.session_state["search_viewport_inner_w"] = int(float(w))
        except (TypeError, ValueError):
            pass


def _search_price_chart_axis_px() -> tuple[int, int]:
    """Axis label sizes for the Search price chart; larger on viewports wider than mobile CSS."""
    w = st.session_state.get("search_viewport_inner_w")
    if w is None:
        return _SEARCH_CHART_AXIS_TICK_MOBILE, _SEARCH_CHART_AXIS_TITLE_MOBILE
    if w <= 768:
        return _SEARCH_CHART_AXIS_TICK_MOBILE, _SEARCH_CHART_AXIS_TITLE_MOBILE
    return _SEARCH_CHART_AXIS_TICK_DESKTOP, _SEARCH_CHART_AXIS_TITLE_DESKTOP


def _search_price_chart_margin_top(has_compare: bool) -> int:
    """Plotly layout margin top: keep desktop padding; trim unused space on mobile (single chart had t=140 with no top legend)."""
    w = st.session_state.get("search_viewport_inner_w")
    if w is None or w > 768:
        return 140
    return 88 if has_compare else 28


def _format_search_price(value) -> str:
    """Currency display: cents above $1, up to 8 decimals below $1."""
    try:
        price = float(value)
    except (TypeError, ValueError):
        return "N/A"

    if abs(price) > 1:
        return f"${price:,.2f}"

    formatted = f"{price:,.8f}"
    whole, _, decimal = formatted.partition(".")
    decimal = decimal.rstrip("0")
    if len(decimal) < 2:
        decimal = decimal.ljust(2, "0")
    return f"${whole}.{decimal}"


def _build_search_price_figure(
    *,
    has_compare: bool,
    plot_df: pd.DataFrame,
    comp_df: pd.DataFrame | None,
    ticker: str,
    compare_ticker: str,
    axis_tick: int,
    axis_title: int,
    margin_top: int,
) -> go.Figure:
    tick_kw = dict(size=axis_tick, color="#111827")
    title_kw = dict(size=axis_title, color="#111827")
    if has_compare and comp_df is not None:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=plot_df["date_dt"],
                y=plot_df["pct"],
                name=ticker,
                line=dict(color="#4ade80", width=2),
                hovertemplate="Change: %{y:+.2f}%<extra></extra>",
            )
        )
        fig.add_trace(
            go.Scatter(
                x=comp_df["date_dt"],
                y=comp_df["pct"],
                name=compare_ticker,
                line=dict(color="#818cf8", width=2),
                hovertemplate="Change: %{y:+.2f}%<extra></extra>",
            )
        )
        fig.update_layout(
            yaxis_title="Change from start (%)",
            template="plotly_dark",
            height=500,
            margin=dict(l=60, r=20, t=margin_top, b=60),
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="left",
                x=0,
                font=dict(size=20),
            ),
            font=dict(size=20),
            xaxis=dict(
                tickfont=tick_kw,
                title_font=title_kw,
                showspikes=False,
                unifiedhovertitle=dict(text="%{x|%b %d, %Y}"),
            ),
            yaxis=dict(tickfont=tick_kw, title_font=title_kw),
            hovermode="x unified",
            hoverdistance=200,
            spikedistance=-1,
            hoverlabel=dict(
                bgcolor="#ffffff",
                bordercolor="#cbd5e1",
                font=dict(color="#111827", size=26),
                align="left",
                namelength=-1,
            ),
        )
    else:
        fig = go.Figure()
        fig.add_trace(
            go.Scatter(
                x=plot_df["date_dt"],
                y=plot_df["price"],
                customdata=plot_df["price"].apply(_format_search_price),
                name=ticker,
                line=dict(color="#4ade80", width=2),
                hovertemplate="Price: %{customdata}<extra></extra>",
            )
        )
        fig.update_layout(
            yaxis_title="Price (USD)",
            template="plotly_dark",
            height=500,
            margin=dict(l=60, r=20, t=margin_top, b=60),
            font=dict(size=20),
            xaxis=dict(
                tickfont=tick_kw,
                title_font=title_kw,
                showspikes=False,
                unifiedhovertitle=dict(text="%{x|%b %d, %Y}"),
            ),
            yaxis=dict(tickfont=tick_kw, title_font=title_kw),
            hovermode="x unified",
            hoverdistance=200,
            spikedistance=-1,
            hoverlabel=dict(
                bgcolor="#ffffff",
                bordercolor="#cbd5e1",
                font=dict(color="#111827", size=26),
                align="left",
                namelength=-1,
            ),
        )
    return fig


# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Search | Live",
    page_icon=logo_path_str(),
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_environment_banner(st)

# ── Global responsive styling ─────────────────────────────────────────
st.markdown(
    """
    <style>
    /* ===== DESKTOP / HIGH-RES ===== */
    html, body, [class*="css"] {
        font-size: 30px !important;
        line-height: 1.7 !important;
    }
    h1 { font-size: 5rem !important; font-weight: 800 !important; }
    h2 { font-size: 3.2rem !important; }
    h3 { font-size: 2.6rem !important; }
    h4 { font-size: 2.1rem !important; }
    p, li, span, div { font-size: 1.6rem !important; line-height: 1.75 !important; }
    .stMarkdown p { font-size: 1.6rem !important; }
    /* Metrics */
    [data-testid="stMetricValue"] > div { font-size: 4rem !important; font-weight: 700 !important; }
    [data-testid="stMetricLabel"] > div > div > p,
    [data-testid="stMetricLabel"] label { font-size: 1.7rem !important; }
    [data-testid="stMetricDelta"] > div { font-size: 1.5rem !important; }
    /* Alerts */
    .stAlert p, [data-testid="stAlert"] p { font-size: 1.6rem !important; }
    .stSuccess p, .stWarning p, .stInfo p { font-size: 1.6rem !important; }
    /* Slider */
    .stSlider label { font-size: 1.6rem !important; margin-bottom: 1rem !important; }
    .stSlider p { font-size: 1.5rem !important; }
    .stSlider [data-testid="stThumbValue"] { margin-bottom: 0.5rem !important; }
    /* Buttons */
    .stButton button, button[kind="primary"] {
        font-size: 1.7rem !important;
        padding: 1.1rem 2.2rem !important;
        min-height: 4rem !important;
    }
    /* Primary button — light blue */
    .stMainBlockContainer > div > div > .stButton button[kind="primary"],
    button[kind="primary"] {
        background-color: #60a5fa !important;
        border-color: #60a5fa !important;
        color: #fff !important;
    }
    button[kind="primary"]:hover {
        background-color: #93c5fd !important;
        border-color: #93c5fd !important;
    }
    /* Captions */
    .stCaption p, [data-testid="stCaptionContainer"] p { font-size: 1.4rem !important; }
    /* Subheaders inside columns */
    [data-testid="stHorizontalBlock"] h2,
    [data-testid="stHorizontalBlock"] h3 { font-size: 2.2rem !important; }
    /* st.table (HTML) */
    [data-testid="stTable"] th {
        font-size: 1.6rem !important; font-weight: 700 !important; padding: 14px 18px !important;
    }
    [data-testid="stTable"] td {
        font-size: 1.6rem !important; padding: 12px 18px !important;
    }

    /* Sidebar — larger text & inputs */
    [data-testid="stSidebar"] { min-width: 380px !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span { font-size: 1.5rem !important; }
    [data-testid="stSidebar"] h1 { font-size: 2.8rem !important; }
    .sidebar-brand {
        font-size: 60px !important;
        font-weight: 400 !important;
        color: #000000 !important;
        line-height: 1.05 !important;
        background: #ffffff !important;
        display: block !important;
        width: calc(100% + 2rem) !important;
        margin: 0.15rem -1rem 140px -1rem !important;
        padding: 0.7rem 1rem !important;
        box-sizing: border-box !important;
        white-space: nowrap !important;
    }
    .sidebar-brand-row {
        display: inline-flex !important;
        align-items: flex-end !important;
        gap: 10px !important;
    }
    .sidebar-brand-text {
        font-size: 60px !important;
        font-weight: 400 !important;
        color: #000000 !important;
        text-decoration: underline !important;
        text-underline-offset: 6px !important;
    }
    [data-testid="stSidebar"] .stButton button {
        font-size: 1.6rem !important;
        padding: 1.1rem 1.8rem !important;
        min-height: 3.8rem !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="input"] > div {
        min-height: 3.6rem !important;
        max-height: 3.6rem !important;
        align-items: center !important;
        overflow: hidden !important;
    }
    [data-testid="stSidebar"] div[data-baseweb="input"] input {
        font-size: 1.2rem !important;
        line-height: 1.2 !important;
        padding: 0.5rem 0.75rem !important;
        height: 2.4rem !important;
        white-space: nowrap !important;
        overflow: hidden !important;
        text-overflow: ellipsis !important;
    }
    [data-testid="stSidebar"] [data-testid="InputInstructions"] {
        display: none !important;
    }
    [data-testid="stSidebar"] [data-testid="stTextInput"] label p {
        font-size: 1.15rem !important;
        line-height: 1.2 !important;
        margin-bottom: 0.35rem !important;
    }
    .tip-wrap {
        position: relative;
        display: inline-block;
        border-bottom: 2px dotted #475569;
        cursor: help;
        font-weight: 700;
        color: #0f172a;
    }
    .tip-wrap .tip-text {
        visibility: hidden;
        opacity: 0;
        width: 420px;
        max-width: min(90vw, 420px);
        background: #111827;
        color: #e5e7eb;
        text-align: left;
        border-radius: 8px;
        border: 1px solid #374151;
        padding: 0.75rem 0.9rem;
        position: absolute;
        z-index: 9999;
        left: 0;
        top: auto;
        bottom: calc(100% + 12px);
        box-shadow: 0 8px 18px rgba(0, 0, 0, 0.35);
        line-height: 1.5;
        font-size: 1rem !important;
        font-weight: 500;
        transition: opacity 0.15s ease;
    }
    .tip-wrap:hover .tip-text {
        visibility: visible;
        opacity: 1;
    }
    [data-testid="stSidebar"] .stSlider label { font-size: 1.5rem !important; }
    [data-testid="stSidebar"] .stSlider p { font-size: 1.4rem !important; }
    [data-testid="stSidebar"] .stCaption p { font-size: 1.3rem !important; }
    [data-testid="stSidebar"] a { font-size: 1.5rem !important; }
    /* Hide auto-generated multipage nav so we can use custom labels */
    [data-testid="stSidebarNav"] { display: none !important; }
    div[data-testid="stCheckbox"] {
        background: #0f172a;
        border: 1px solid #334155;
        border-radius: 10px;
        padding: 0.5rem 0.8rem;
        margin-top: 0.35rem;
    }
    div[data-testid="stCheckbox"] label p {
        color: #e2e8f0 !important;
        font-weight: 700 !important;
    }
    /* Plotly chart axis labels are configured per-chart in layout */
    /* Search: 52-week low/high divider (compact on mobile via rules below) */
    hr.search-52w-range-divider {
        border: none;
        border-top: 1px solid rgba(148, 163, 184, 0.65);
        margin: 0.75rem 0;
    }
    @media (min-width: 769px) {
        /* Search Plotly hover: keep the date/price label clear of the cursor. */
        .js-plotly-plot .hoverlayer {
            transform: translate(20px, -20px) !important;
        }
    }
    /* ===== MOBILE ===== */
    @media (max-width: 768px) {
        /* Search: tighter gap between "Price Chart" title and Plotly block */
        h3.search-price-chart-heading {
            margin-bottom: 0.25rem !important;
        }
        /* 52-Week Range: tighten gap between low row (+ %) and high row (mobile only) */
        h3.search-52week-range-heading {
            margin-bottom: 0.35rem !important;
        }
        hr.search-52w-range-divider {
            margin: 0.1rem 0 !important;
        }
        [data-testid="stMarkdownContainer"]:has(hr.search-52w-range-divider) {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        [data-testid="element-container"]:has(
            + [data-testid="element-container"] hr.search-52w-range-divider
        ) {
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        [data-testid="element-container"]:has(hr.search-52w-range-divider)
            + [data-testid="element-container"] {
            margin-top: 0 !important;
            padding-top: 0.2rem !important;
        }
        /* Mobile-only spacing tune (Search page only; header/sidebar chrome matches NYSE 10 — default Streamlit) */
        .stApp { overflow-x: hidden !important; }
        /* Sentiment column: remove fixed-height whitespace on mobile */
        .mood-column { margin-top: 0 !important; }
        .mood-feed {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            margin-bottom: 0 !important;
            padding-bottom: 0.25rem !important;
        }
        /* Extra top padding so index banners clear Streamlit header / notch (0.75rem alone clipped the row on phones) */
        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 2.75rem) !important;
            padding-left: 0.85rem !important;
            padding-right: 0.85rem !important;
        }
        /* Reduce vertical whitespace between blocks */
        [data-testid="stVerticalBlock"] { gap: 0.75rem !important; }
        /* Title/headings default margins are large on mobile */
        h1, h2, h3, h4 { margin-top: 0.35rem !important; margin-bottom: 0.45rem !important; }

        /* Mobile-friendly type scale (desktop unaffected) */
        html, body, [class*="css"] { font-size: 18px !important; line-height: 1.55 !important; }
        h1 { font-size: clamp(1.85rem, 6.3vw, 2.55rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.48rem, 5.2vw, 2.05rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.32rem, 4.7vw, 1.78rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.2rem, 4.1vw, 1.55rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; line-height: 1.68 !important; }

        /* Alerts / info boxes */
        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; line-height: 1.68 !important; }

        /* Metrics */
        [data-testid="stMetricValue"] > div { font-size: clamp(1.95rem, 7.2vw, 2.8rem) !important; }
        [data-testid="stMetricLabel"] > div > div > p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; }
        [data-testid="stMetricDelta"] > div { font-size: clamp(1.04rem, 3.6vw, 1.22rem) !important; }

        /* Buttons + captions */
        .stButton button { font-size: clamp(1.08rem, 3.75vw, 1.24rem) !important; padding: 0.8rem 1.15rem !important; }
        .stCaption p { font-size: clamp(0.98rem, 3.4vw, 1.12rem) !important; }

        /* Sticky disclaimer: keep readable but not overwhelming */
        .disclaimer-footer {
            font-size: clamp(0.76rem, 2.9vw, 0.92rem) !important;
            line-height: 1.4 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.78rem, 3vw, 0.94rem) !important;
        }

        /* Tables: scale vertically on mobile (more row height) */
        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.6rem, 2.6vw, 0.9rem) !important;
            padding-bottom: clamp(0.6rem, 2.6vw, 0.9rem) !important;
            line-height: 1.5 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(0.95rem, 3.25vw, 1.08rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div { flex: 1 1 100% !important; min-width: 100% !important; }
        [data-testid="stSidebar"] { min-width: 280px !important; }

        /* Sidebar brand title (The Scoop 52): larger on mobile only */
        .sidebar-brand-text,
        [data-testid="stSidebar"] #scoop-title {
            font-size: clamp(2.6rem, 11vw, 3.8rem) !important;
            line-height: 1.05 !important;
        }

        /* Mobile: reduce gap under the Scoop 52 title */
        .sidebar-brand {
            margin: 0.15rem -1rem 1.1rem -1rem !important;
            padding: 0.55rem 1rem !important;
        }

        /* Sidebar page links: larger on mobile only */
        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.25rem, 4.6vw, 1.55rem) !important;
            line-height: 1.25 !important;
        }

        /* Mobile: center hover tooltips so no horizontal scrolling is needed */
        .tip-wrap .tip-text {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            width: min(420px, 92vw) !important;
            max-width: 92vw !important;
            margin: 0 !important;
        }
    }

    /* ===== TABLET ===== */
    @media (min-width: 769px) and (max-width: 1200px) {
        html, body, [class*="css"] { font-size: 26px !important; }
        h1 { font-size: 3.4rem !important; }
        [data-testid="stMetricValue"] > div { font-size: 3.2rem !important; }
        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div { flex: 1 1 48% !important; min-width: 48% !important; }
    }
    [data-testid="stSidebar"] #scoop-title {
        font-size: 60px !important;
        line-height: 1.05 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Cached resources (shared across reruns) ──────────────────────────
@st.cache_resource
def get_predictor():
    return Predictor()

@st.cache_resource
def get_market_data():
    return MarketData()

@st.cache_resource
def get_sentiment_engine():
    return SentimentEngine()

_SEARCH_ANALYSIS_TTL_SEC = 15 * 60


_SEARCH_ASSET_NAMES = {
    "BTC": "Bitcoin",
    "BTC-USD": "Bitcoin",
    "ETH": "Ethereum",
    "ETH-USD": "Ethereum",
    "DOGE": "Dogecoin",
    "DOGE-USD": "Dogecoin",
    "SOL": "Solana",
    "SOL-USD": "Solana",
    "ADA": "Cardano",
    "ADA-USD": "Cardano",
    "XRP": "XRP",
    "XRP-USD": "XRP",
    "BNB": "BNB",
    "BNB-USD": "BNB",
    "AVAX": "Avalanche",
    "AVAX-USD": "Avalanche",
    "LINK": "Chainlink",
    "LINK-USD": "Chainlink",
    "SAND": "The Sandbox",
    "SAND-USD": "The Sandbox",
    "MANA": "Decentraland",
    "MANA-USD": "Decentraland",
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "TSLA": "Tesla Inc.",
    "NVDA": "NVIDIA Corp.",
    "AMZN": "Amazon.com Inc.",
    "GOOGL": "Alphabet Inc.",
    "META": "Meta Platforms Inc.",
}


def _search_asset_display_name(ticker: str) -> str:
    """Return a readable label for the searched asset."""
    normalized = ticker.strip().upper()
    return _SEARCH_ASSET_NAMES.get(normalized, normalized)


@st.cache_data(
    ttl=_SEARCH_ANALYSIS_TTL_SEC,
    show_spinner="Loading headlines and sentiment (updates every 15 minutes)…",
)
def _cached_search_analysis_bundle(ticker: str, days, compare_ticker: str) -> dict | None:
    """
    News, sentiment, predictor, and aligned price history — refreshed on a fixed
    TTL so user interactions do not re-trigger headline/sentiment work.
    """
    market_eng = get_market_data()
    sentiment_eng = get_sentiment_engine()
    predictor_eng = get_predictor()
    news_items = market_eng.get_news_items(ticker)[:10]
    headlines = [item["title"] for item in news_items]
    history = market_eng.get_price_history(ticker, days)
    if not history:
        return None
    latest_price = market_eng.get_latest_price(ticker)
    sent_result = sentiment_eng.analyze_headlines(ticker, headlines)
    result = predictor_eng.predict(ticker, headlines)
    week52_low = market_eng.get_52_week_low(ticker)
    week52_high = market_eng.get_52_week_high(ticker)
    low_date, high_date = market_eng.get_52_week_low_high_dates(ticker)
    compare_history: list = []
    if compare_ticker and compare_ticker != ticker:
        compare_history = market_eng.get_price_history(compare_ticker, days)
    return {
        "news_items": news_items,
        "sent_result": sent_result,
        "result": result,
        "history": history,
        "compare_history": compare_history,
        "latest_price": latest_price,
        "week52_low": week52_low,
        "week52_high": week52_high,
        "low_date": low_date,
        "high_date": high_date,
    }


# ── Sidebar ──────────────────────────────────────────────────────────
st.sidebar.image(logo_path_str(), use_container_width=True)
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
      <div class="sidebar-brand-row">
        <span id="scoop-title" class="sidebar-brand-text" style="font-size:60px !important;line-height:1.05 !important;">The Scoop 52</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
st.sidebar.page_link("pages/1_NYSE_Top_10.py", label="📊 NYSE 10")
st.sidebar.page_link("pages/2_NASDAQ_Top_10.py", label="💹 NASDAQ 10")
st.sidebar.page_link("pages/3_Crypto_Top_10.py", label="🪙 Crypto 10")
st.sidebar.page_link("pages/4_New_Crypto_Top_10.py", label="🚀 New Crypto 10")
st.sidebar.page_link("pages/5_CME_Top_10.py", label="🌾 CME Commodities 10")
st.sidebar.page_link("pages/6_ICE_Top_10.py", label="🛢️ ICE Commodities 10")
st.sidebar.page_link("app.py", label="🔎 Search")
st.sidebar.markdown("---")

ticker_input = st.sidebar.text_input(
    "Enter Ticker",
    value="DOGE",
    placeholder="e.g. DOGE, BTC, TSLA",
)

compare_input = st.sidebar.text_input(
    "Compare Against (optional)",
    value="",
    placeholder="e.g. BTC, ETH, TSLA",
)

st.sidebar.caption("Crypto tickers auto-append -USD")

st.sidebar.markdown("---")

PERIOD_OPTIONS = {
    "7 days": 7,
    "30 days": 30,
    "90 days": 90,
    "180 days": 180,
    "1 year": 365,
    "2 years": 730,
    "5 years": 1825,
    "All Time": "max",
}

st.sidebar.page_link("pages/7_Terms_of_Service.py", label="📜 Terms of Service")


@st.fragment(run_every=timedelta(minutes=15))
def _render_search_dashboard(ticker: str, compare_ticker: str) -> None:
    """Renders search analysis; reruns on a timer so cached sentiment/news refresh without widget clicks."""
    days = PERIOD_OPTIONS[st.session_state["search_price_history_range"]]
    bundle = _cached_search_analysis_bundle(ticker, days, compare_ticker)
    if not bundle:
        st.error(f"Could not find data for {ticker}. Please check the ticker symbol.")
        st.stop()

    news_items = bundle["news_items"]
    sent_result = bundle["sent_result"]
    result = bundle["result"]
    history = bundle["history"]
    compare_history = bundle["compare_history"]
    latest_price = bundle["latest_price"]
    week52_low = bundle["week52_low"]
    week52_high = bundle["week52_high"]
    low_date = bundle["low_date"]
    high_date = bundle["high_date"]

    df = pd.DataFrame(history)

    sentiment_score = sent_result["score"]
    sentiment_label = sent_result["label"]
    last_price = latest_price if latest_price > 0 else df.iloc[-1]["price"]
    prev_price = df.iloc[-2]["price"] if len(df) >= 2 else last_price
    change_24h_pct = ((last_price - prev_price) / prev_price * 100) if prev_price else 0
    combined = result["combined_score"]
    direction = "BULLISH" if combined > 0 else "BEARISH"
    arrow = "⬆️" if combined > 0 else "⬇️"
    color = "#4ade80" if combined > 0 else "#f87171"
    bg = "#14532d" if combined > 0 else "#7f1d1d"

    asset_name = _search_asset_display_name(ticker)
    st.markdown(
        f"""
        <div style="
            border:1px solid #cbd5e1;
            border-left:6px solid #2563eb;
            border-radius:12px;
            padding:0.9rem 1.1rem;
            margin:0 0 1rem 0;
            background:#f8fafc;
        ">
            <div style="font-size:1rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">
                Selected Asset
            </div>
            <div style="font-size:2rem;line-height:1.25;font-weight:800;color:#0f172a;">
                {html.escape(asset_name)}
            </div>
            <div style="font-size:1.15rem;color:#475569;font-weight:700;margin-top:0.2rem;">
                Ticker: {html.escape(ticker)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Headline sentiment, news, and related scores use a snapshot refreshed at most every "
        f"{_SEARCH_ANALYSIS_TTL_SEC // 60} minutes (not on each click). Price range controls still update the chart window."
    )

    st.markdown(
        f"""
        <div style="background:{bg}; border: 3px solid {color}; border-radius:15px;
                    padding:1.5rem 2rem; text-align:center; margin-bottom:1.5rem;">
            <div style="display:flex; align-items:center; justify-content:center; gap:1.5rem; flex-wrap:wrap;">
                <span style="font-size:4rem;">{arrow}</span>
                <span style="font-size:3.2rem; font-weight:800; color:{color};">{direction}</span>
                <span style="color:#d1d5db; font-size:1.6rem;">
                    Score: {combined:+.4f} &middot; Market Mood: {sentiment_label.capitalize()}
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.metric(
        label="Live Price (USD)",
        value=_format_search_price(last_price),
        delta=f"{change_24h_pct:+.2f}% (24h)",
    )

    if last_price < 0.01:
        st.warning("⚠️ Low-Cap/Penny Asset Detected")

    col_chart, col_mood = st.columns([2, 1])

    with col_chart:
        st.markdown(
            '<h3 class="search-52week-range-heading">📊 52-Week Range</h3>',
            unsafe_allow_html=True,
        )
        has_low = week52_low and week52_low > 0
        has_high = week52_high and week52_high > 0

        if not has_low and not has_high:
            st.info("No 52-week range data available for this asset.")
        else:
            if has_low:
                low_dollar_diff = last_price - week52_low
                pct_above_low = (low_dollar_diff / week52_low) * 100

                if pct_above_low <= 10:
                    st.success("🔥 **BULLISH MARKET MOOD** — Price is near the 52-week low")

                low_c1, low_c2, _ = st.columns([1, 1, 1])
                with low_c1:
                    st.metric(label="52-Week Low", value=_format_search_price(week52_low))
                    st.caption(f"Hit on {low_date}" if low_date else "")
                with low_c2:
                    st.metric(
                        label="Above 52-Week Low",
                        value=_format_search_price(low_dollar_diff),
                        delta=f"{pct_above_low:+.1f}%",
                    )

            if has_low and has_high:
                st.markdown(
                    '<hr class="search-52w-range-divider" />',
                    unsafe_allow_html=True,
                )

            if has_high:
                high_dollar_diff = last_price - week52_high
                pct_below_high = ((week52_high - last_price) / week52_high) * 100

                if pct_below_high <= 0:
                    st.warning("🚀 **AT / ABOVE 52-WEEK HIGH** — Asset is at peak, watch for reversal")

                high_c1, high_c2, _ = st.columns([1, 1, 1])
                with high_c1:
                    st.metric(label="52-Week High", value=_format_search_price(week52_high))
                    st.caption(f"Hit on {high_date}" if high_date else "")
                with high_c2:
                    st.metric(
                        label="Below 52-Week High",
                        value=_format_search_price(abs(high_dollar_diff)),
                        delta=f"{high_dollar_diff / week52_high * 100:+.1f}%",
                    )

        st.select_slider(
            "📅 Price History Range",
            options=list(PERIOD_OPTIONS.keys()),
            key="search_price_history_range",
        )
        st.markdown(
            '<h3 class="search-price-chart-heading">📈 Price Chart</h3>',
            unsafe_allow_html=True,
        )
        has_compare = bool(compare_history)
        plot_df = df.copy()
        plot_df["date_dt"] = pd.to_datetime(plot_df["date"])
        comp_df: pd.DataFrame | None = None
        if has_compare:
            comp_df = pd.DataFrame(compare_history)
            comp_df["date_dt"] = pd.to_datetime(comp_df["date"])
            base_price = plot_df.iloc[0]["price"]
            plot_df["pct"] = ((plot_df["price"] - base_price) / base_price) * 100
            comp_base = comp_df.iloc[0]["price"]
            comp_df["pct"] = ((comp_df["price"] - comp_base) / comp_base) * 100

        ax_tick, ax_title = _search_price_chart_axis_px()
        margin_top = _search_price_chart_margin_top(has_compare)
        fig = _build_search_price_figure(
            has_compare=has_compare,
            plot_df=plot_df,
            comp_df=comp_df,
            ticker=ticker,
            compare_ticker=compare_ticker,
            axis_tick=ax_tick,
            axis_title=ax_title,
            margin_top=margin_top,
        )

        st.plotly_chart(fig, width="stretch")

        if has_compare:
            merged = pd.merge(
                df[["date", "change_pct"]].rename(columns={"change_pct": "main"}),
                comp_df[["date", "change_pct"]].rename(columns={"change_pct": "comp"}),
                on="date",
                how="inner",
            )
            if len(merged) >= 5:
                corr = merged["main"].corr(merged["comp"])
                strength = "High" if abs(corr) >= 0.7 else "Moderate" if abs(corr) >= 0.4 else "Low"
                if corr > 0:
                    st.info(
                        f"🔗 **{strength} positive correlation** (r = {corr:+.2f}) — they tend to move in the **same direction**."
                    )
                else:
                    st.info(
                        f"🔀 **{strength} negative correlation** (r = {corr:+.2f}) — they tend to move in **opposite directions**."
                    )
            else:
                st.caption("Not enough overlapping trading days to compute correlation.")

    with col_mood:
        st.markdown("<div class='mood-column' style='margin-top:-400px;'>", unsafe_allow_html=True)
        mood_color = {"bullish": "#22c55e", "bearish": "#ef4444", "neutral": "#f59e0b"}.get(
            sentiment_label, "#94a3b8"
        )
        st.markdown(
            f"""
            <div style="
                border:1px solid #334155;
                border-radius:10px;
                padding:0.8rem 1rem;
                margin-bottom:0.7rem;
                background:#0f172a08;
            ">
                <div style="display:flex;align-items:center;gap:0.6rem;font-weight:700;color:#0f172a;">
                    <span>Market Mood</span>
                    <span style="
                        display:inline-block;
                        width:0.9rem;
                        height:0.9rem;
                        border-radius:999px;
                        background:{mood_color};
                        box-shadow:0 0 0 2px {mood_color}33;
                    "></span>
                </div>
                <div style="margin-top:0.45rem;color:#334155;">
                    Current Mood: <b>{sentiment_label.capitalize()}</b> &nbsp;|&nbsp; Score: <b>{sentiment_score:+.4f}</b>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        headline_to_urls = {}
        for item in news_items:
            title = item.get("title", "")
            if title:
                headline_to_urls.setdefault(title, []).append(item.get("url", ""))

        rows_html = ""
        for headline, score in sent_result["headline_scores"][:10]:
            urls = headline_to_urls.get(headline, [])
            source_url = urls.pop(0) if urls else ""
            safe_headline = html.escape(str(headline))
            score_text = f"{float(score):+.3f}"
            source_cell = (
                f'<a href="{html.escape(source_url)}" target="_blank" rel="noopener noreferrer">Source</a>'
                if source_url
                else "N/A"
            )
            rows_html += (
                "<tr>"
                f"<td>{safe_headline}</td>"
                f"<td style='text-align:right;white-space:nowrap;'>{score_text}</td>"
                f"<td style='text-align:center;'>{source_cell}</td>"
                "</tr>"
            )

        table_html = (
            "<table style='width:100%;border-collapse:collapse;'>"
            "<thead><tr>"
            "<th style='text-align:left;padding:10px;border-bottom:1px solid #334155;'>Headline</th>"
            "<th style='text-align:right;padding:10px;border-bottom:1px solid #334155;'>Score</th>"
            "<th style='text-align:center;padding:10px;border-bottom:1px solid #334155;'>Source URL</th>"
            "</tr></thead>"
            f"<tbody>{rows_html}</tbody>"
            "</table>"
        )
        st.markdown(
            "<div class='mood-feed' style='height:1600px;overflow-y:auto;border:1px solid #334155;border-radius:10px;padding:0.25rem;margin-bottom:0;'>"
            f"{table_html}</div>",
            unsafe_allow_html=True,
        )
        st.markdown("</div>", unsafe_allow_html=True)


if "search_terms_accepted" not in st.session_state:
    st.session_state["search_terms_accepted"] = False
agreed = st.session_state["search_terms_accepted"]
ensure_timezone_cookie(st)
if agreed:
    log_terms_acceptance(st, consent_key="agree_terms_search")
if "search_price_history_range" not in st.session_state:
    st.session_state["search_price_history_range"] = "30 days"

ticker = ticker_input.strip().upper()
compare_ticker = compare_input.strip().upper()
_probe_search_chart_viewport()

# ── Exchange performance banners ──────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def _fetch_index(tkr: str):
    try:
        return get_market_data().get_daily_change(tkr)
    except Exception:
        return None, None

def _banner_card(label, price, chg, prefix="$"):
    if price is None:
        return ""
    c = "#22c55e" if chg >= 0 else "#ef4444"
    a = "▲" if chg >= 0 else "▼"
    return (
        f'<div style="flex:1;min-width:180px;background:linear-gradient(135deg,#1e293b,#0f172a);'
        f'border:1px solid #334155;border-left:4px solid {c};border-radius:12px;'
        f'padding:0.9rem 1.4rem;display:flex;align-items:center;gap:0.8rem;flex-wrap:wrap;">'
        f'<span style="font-size:1.1rem;color:#e2e8f0;font-weight:500;">{label}</span>'
        f'<span style="font-size:1.6rem;font-weight:700;color:#f1f5f9;">{prefix}{price:,.2f}</span>'
        f'<span style="font-size:1.1rem;font-weight:600;color:{c};background:{c}18;'
        f'padding:0.2rem 0.6rem;border-radius:6px;">{a} {chg:+.2f}%</span></div>'
    )

_nya_p, _nya_c = _fetch_index("^NYA")
_ixic_p, _ixic_c = _fetch_index("^IXIC")
_btc_p, _btc_c = _fetch_index("BTC-USD")
_eth_p, _eth_c = _fetch_index("ETH-USD")
_cl_p, _cl_c = _fetch_index("CL=F")
_gc_p, _gc_c = _fetch_index("GC=F")

_all_cards = (
    _banner_card("NYSE (^NYA)", _nya_p, _nya_c)
    + _banner_card("NASDAQ (^IXIC)", _ixic_p, _ixic_c)
    + _banner_card("BTC", _btc_p, _btc_c)
    + _banner_card("ETH", _eth_p, _eth_c)
    + _banner_card("WTI Crude", _cl_p, _cl_c)
    + _banner_card("Gold", _gc_p, _gc_c)
)
if _all_cards:
    st.markdown(
        f'<div style="display:flex;gap:0.8rem;flex-wrap:wrap;margin-bottom:1.2rem;">{_all_cards}</div>',
        unsafe_allow_html=True,
    )

# ── Main area ────────────────────────────────────────────────────────
st.title(f"{ticker} Dashboard")

if not agreed:
    st.warning("Please agree to the **Disclaimer & Terms of Service** to enable analysis.")
    agreed = st.checkbox(
        "I have read and agree to the [Disclaimer & Terms of Service](/Terms_of_Service)",
        key="agree_terms_search",
    )
    if agreed:
        st.session_state["search_terms_accepted"] = True
        log_terms_acceptance(st, consent_key="agree_terms_search")

if ticker and agreed:
    _render_search_dashboard(ticker, compare_ticker)
else:
    st.markdown(
        "<div style='text-align:center; padding:3rem 0; color:#9ca3af;'>"
        "<p style='font-size:4rem; margin:0.5rem 0;'>☝️</p>"
        "<p style='font-size:2rem;'>Use the sidebar to enter a ticker to view analysis.</p>"
        "</div>",
        unsafe_allow_html=True,
    )

# ── Sticky disclaimer footer ─────────────────────────────────────────
st.markdown(
    """
    <style>
    .disclaimer-footer {
        position: fixed; bottom: 0; left: var(--footer-sidebar-width); width: calc(100% - var(--footer-sidebar-width));
        background: #020617; border-top: 1px solid #334155;
        padding: 0.6rem 1rem;
        box-sizing: border-box; z-index: 10000;
        font-size: clamp(0.78rem, 0.72rem + 0.15vw, 0.9rem) !important; color: #e2e8f0;
        text-align: center; line-height: 1.45; white-space: normal;
        transition: left 0.25s ease, width 0.25s ease, font-size 0.25s ease;
    }
    .disclaimer-footer a { color: #93c5fd; text-decoration: underline; font-weight: 600; }
    .stMainBlockContainer { padding-bottom: 9rem !important; }
    :root { --footer-sidebar-width: 360px; }
    @media (max-width: 1400px) { :root { --footer-sidebar-width: 330px; } }
    @media (max-width: 1200px) { :root { --footer-sidebar-width: 300px; } }
    @media (max-width: 992px)  { :root { --footer-sidebar-width: 270px; } }
    @media (max-width: 768px) {
        :root { --footer-sidebar-width: 0px; }
        .disclaimer-footer {
            position: static !important;
            left: 0 !important;
            width: 100% !important;
            /* Mobile: keep footer compact so it doesn't block form controls */
            padding: 0.35rem 0.55rem !important;
            font-size: 0.64rem !important;
            line-height: 1.25 !important;
        }
        .disclaimer-footer strong,
        .disclaimer-footer a {
            font-size: inherit !important;
        }
        .stMainBlockContainer { padding-bottom: 2rem !important; }
    }
    </style>
    <div class="disclaimer-footer">
        <strong>⚠️ ALGORITHMIC RESEARCH ONLY – NOT FINANCIAL ADVICE</strong>
        This tool provides automated sentiment analysis and 'Market Mood' scores based on third-party news data.
        It is intended for <strong>informational and educational purposes only</strong> and does not constitute investment advice.
        Market data is provided 'as-is' and may be delayed or inaccurate.
        <strong>Trading involves significant risk of loss.</strong>
        <a href="/Terms_of_Service" target="_self">Terms of Service</a> ·
        Past performance is not indicative of future results.
    </div>
    """,
    unsafe_allow_html=True,
)