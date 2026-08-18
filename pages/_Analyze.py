"""
Analyze deep-dive page (hidden from navigation).

Opened from Top 10 **Analyze** links with ?ticker=. Archived Search backup: archived/search_page.py
"""

from datetime import timedelta

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import html

from analyze_page import (
    analyze_screener_snapshot_key,
    capture_analyze_source_from_query,
    inherit_screener_terms_for_analyze,
    is_analyze_mode,
    query_param_ticker,
    render_analyze_back_button,
)
from asset_names import resolve_asset_display_name
from predictor import Predictor
from market_data import MarketData
from screener_headlines import get_cached_news_items, normalize_screener_ticker
from sentiment_engine import SentimentEngine
from legal_consent_logger import ensure_timezone_cookie, log_terms_acceptance, render_terms_gate, terms_accepted
from branding import logo_path_str, render_environment_banner
from theme_mode import (
    chart_axis_colors,
    chart_hoverlabel,
    chart_paper_bgcolor,
    chart_plot_bgcolor,
    chart_template,
    inject_dark_mode_styles,
    install_theme_support,
    is_dark_mode,
    render_dark_mode_toggle,
)
from tooltip_scroll import install_responsive_sidebar_handler, install_tooltip_scroll_handler, inject_desktop_analyze_top_compact

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
    tick_kw, title_kw = chart_axis_colors()
    hover = chart_hoverlabel()
    layout_bg = dict(
        paper_bgcolor=chart_paper_bgcolor(),
        plot_bgcolor=chart_plot_bgcolor(),
    )
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
            template=chart_template(),
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
                tickfont=dict(size=axis_tick, **tick_kw),
                title_font=dict(size=axis_title, **title_kw),
                showspikes=False,
                unifiedhovertitle=dict(text="%{x|%b %d, %Y}"),
            ),
            yaxis=dict(
                tickfont=dict(size=axis_tick, **tick_kw),
                title_font=dict(size=axis_title, **title_kw),
            ),
            hovermode="x unified",
            hoverdistance=200,
            spikedistance=-1,
            hoverlabel=hover,
            **layout_bg,
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
            template=chart_template(),
            height=500,
            margin=dict(l=60, r=20, t=margin_top, b=60),
            font=dict(size=20),
            xaxis=dict(
                tickfont=dict(size=axis_tick, **tick_kw),
                title_font=dict(size=axis_title, **title_kw),
                showspikes=False,
                unifiedhovertitle=dict(text="%{x|%b %d, %Y}"),
            ),
            yaxis=dict(
                tickfont=dict(size=axis_tick, **tick_kw),
                title_font=dict(size=axis_title, **title_kw),
            ),
            hovermode="x unified",
            hoverdistance=200,
            spikedistance=-1,
            hoverlabel=hover,
            **layout_bg,
        )
    return fig


# ── Page config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Analyze",
    page_icon=logo_path_str(),
    layout="wide",
    initial_sidebar_state="collapsed",
)
render_environment_banner(st)
install_theme_support()
install_responsive_sidebar_handler()
if is_analyze_mode():
    inject_desktop_analyze_top_compact()
capture_analyze_source_from_query()
inherit_screener_terms_for_analyze()

# ── Global responsive styling ─────────────────────────────────────────
st.markdown(
    """
    <style>
    :root {
        --scoop-sidebar-width: clamp(12rem, 20vw, 36rem);
    }
    /* Sidebar: rem-based width scales with browser zoom; no label clipping */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        min-width: var(--scoop-sidebar-width) !important;
        width: var(--scoop-sidebar-width) !important;
        max-width: min(92vw, 36rem) !important;
        overflow-x: visible !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a,
    [data-testid="stSidebar"] [data-testid="stPageLink"] span,
    [data-testid="stSidebar"] [data-testid="stPageLink"] p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] .stCaption p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }

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
        margin: 0.15rem -1rem 0.35rem -1rem !important;
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
        .mood-column {
            margin-top: -400px;
        }
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
        :root { --scoop-sidebar-width: clamp(20rem, 92vw, 36rem); }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: 92vw !important;
            overflow-x: visible !important;
        }

        /* Sidebar brand title (The Scoop 52): larger on mobile only */
        .sidebar-brand-text,
        [data-testid="stSidebar"] #scoop-title {
            font-size: clamp(2.6rem, 11vw, 3.8rem) !important;
            line-height: 1.05 !important;
        }

        /* Mobile: reduce gap under the Scoop 52 title */
        .sidebar-brand {
            margin: 0.15rem -1rem 0.35rem -1rem !important;
            padding: 0.55rem 1rem !important;
        }

        /* Sidebar page links: larger on mobile only */
        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.15rem, 4.2vw, 1.45rem) !important;
            line-height: 1.25 !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
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

    /* ===== Phone mobile (≤743px) — overlay sidebar full off-screen retract; tablet/desktop unchanged ===== */
    @media (max-width: 743px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }

    }

    /* ===== iPad Mini portrait (744px–768px) — overlay sidebar; phones/tablet/desktop unchanged ===== */
    @media (min-width: 744px) and (max-width: 768px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }

    }


    /* ===== TABLET (769px–1366px) — mobile card layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
            --scoop-tablet-gutter: clamp(0.85rem, 2.5vw, 1.1rem);
            --scoop-sidebar-arrow-size: 32px;
            --scoop-sidebar-arrow-top: 14px;
            --scoop-sidebar-arrow-left: 12px;
        }

        html, body {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
            overflow-x: hidden !important;
        }

        .stApp {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }

        /* Main content uses full viewport width (sidebar overlays when open). */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Slide-out sidebar overlays the page (mobile-style). */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100%) !important;
            transition: transform 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            top: auto !important;
            left: auto !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            transform: none !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }
        /* Plain Streamlit arrows (Surface Pro 7 / Duo style) — no boxed chrome. */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            z-index: 1000006 !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            font-size: clamp(1.1rem, 2.2vw, 1.32rem) !important;
        }

        .sidebar-brand-text,
        [data-testid="stSidebar"] #scoop-title {
            font-size: clamp(2.4rem, 5.5vw, 3.25rem) !important;
            line-height: 1.05 !important;
        }
        .sidebar-brand {
            margin: 0.15rem -1rem 0.35rem -1rem !important;
            padding: 0.65rem 1rem !important;
            white-space: normal !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.15rem, 2.2vw, 1.42rem) !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }


        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }


        .stApp { overflow-x: hidden !important; }

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

        h3.search-price-chart-heading { margin-bottom: 0.25rem !important; }
        h3.search-52week-range-heading { margin-bottom: 0.35rem !important; }
        hr.search-52w-range-divider { margin: 0.1rem 0 !important; }

        .mood-column { margin-top: 0 !important; }
        .mood-feed {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            margin-bottom: 0 !important;
            padding-bottom: 0.25rem !important;
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            line-height: 1.62 !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .tip-wrap .tip-text {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

    }

    /* ===== Surface Duo only — full slide-in, mobile-style arrows ===== */
    @media (width: 540px),
           ((width: 720px) and (max-height: 541px)),
           ((min-width: 1110px) and (max-width: 1118px) and (max-height: 741px)) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }

    }

    @media (min-width: 1367px) {

        :root {
            --footer-sidebar-width: clamp(12rem, 20vw, 36rem);
        }

        /* Desktop: sidebar always visible — no slide-out overlay. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: relative !important;
            transform: none !important;
            translate: none !important;
            transition: none !important;
            pointer-events: auto !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            box-shadow: none !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            margin-left: 0 !important;
            left: auto !important;
            top: auto !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            height: auto !important;
            min-height: auto !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: none !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"]) [data-testid="stAppViewContainer"]::before {
            display: none !important;
            content: none !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: auto !important;
            max-width: none !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div {
            width: auto !important;
            max-width: none !important;
        }
        [data-testid="stSidebar"] #scoop-title {
            font-size: 60px !important;
            line-height: 1.05 !important;
        }
    }

    /* ===== iPad 14 Pro Max only — full slide-in retract ===== */
    @media (min-width: 1028px) and (max-width: 1036px) and (min-height: 1370px) {

        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(calc(-100vw - 4px)) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]),
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(calc(-100vw - 4px)) !important;
            visibility: hidden !important;
            pointer-events: none !important;
            opacity: 0 !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            visibility: visible !important;
            opacity: 1 !important;
        }

    }
    @media (min-width: 1370px) and (max-width: 1382px) and (max-height: 1040px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
            --scoop-tablet-gutter: clamp(0.85rem, 2.5vw, 1.1rem);
            --scoop-sidebar-arrow-size: 32px;
            --scoop-sidebar-arrow-top: 14px;
            --scoop-sidebar-arrow-left: 12px;
        }

        html, body {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
            overflow-x: hidden !important;
        }

        .stApp {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }

        /* Main content uses full viewport width (sidebar overlays when open). */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Slide-out sidebar overlays the page (mobile-style). */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100%) !important;
            transition: transform 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            top: auto !important;
            left: auto !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            transform: none !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }
        /* Plain Streamlit arrows (Surface Pro 7 / Duo style) — no boxed chrome. */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            z-index: 1000006 !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            font-size: clamp(1.1rem, 2.2vw, 1.32rem) !important;
        }

        .sidebar-brand-text,
        [data-testid="stSidebar"] #scoop-title {
            font-size: clamp(2.4rem, 5.5vw, 3.25rem) !important;
            line-height: 1.05 !important;
        }
        .sidebar-brand {
            margin: 0.15rem -1rem 0.35rem -1rem !important;
            padding: 0.65rem 1rem !important;
            white-space: normal !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.15rem, 2.2vw, 1.42rem) !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }


        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }


        /* Beat desktop (1367px) split-sidebar rules — same specificity, later cascade. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            margin-left: 0 !important;
            display: block !important;
            opacity: 1 !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
            z-index: 999999 !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
            z-index: 1000010 !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 1000009 !important;
            cursor: pointer !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"] {
            display: flex !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }

    }


    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (folded) ===== */
    @media (min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),
           (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }


        .stApp { overflow-x: hidden !important; }

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

        h3.search-price-chart-heading { margin-bottom: 0.25rem !important; }
        h3.search-52week-range-heading { margin-bottom: 0.35rem !important; }
        hr.search-52w-range-divider { margin: 0.1rem 0 !important; }

        .mood-column { margin-top: 0 !important; }
        .mood-feed {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            margin-bottom: 0 !important;
            padding-bottom: 0.25rem !important;
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            line-height: 1.62 !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .tip-wrap .tip-text {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

    }
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (unfolded) ===== */
    @media (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),
           (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),
           (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px) {

        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }


        .stApp { overflow-x: hidden !important; }

        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

        h3.search-price-chart-heading { margin-bottom: 0.25rem !important; }
        h3.search-52week-range-heading { margin-bottom: 0.35rem !important; }
        hr.search-52w-range-divider { margin: 0.1rem 0 !important; }

        .mood-column { margin-top: 0 !important; }
        .mood-feed {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            margin-bottom: 0 !important;
            padding-bottom: 0.25rem !important;
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            line-height: 1.62 !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .tip-wrap .tip-text {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }


        /* Beat desktop (1367px) split-sidebar rules — same specificity, later cascade. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            margin-left: 0 !important;
            display: block !important;
            opacity: 1 !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
            z-index: 999999 !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
            z-index: 1000010 !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 1000009 !important;
            cursor: pointer !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"] {
            display: flex !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }

    }

    @media (min-width: 1367px) {
        .sidebar-brand {
            width: 100% !important;
            margin: 0.15rem 0 0.35rem 0 !important;
            white-space: normal !important;
        }
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


@st.cache_data(
    ttl=_SEARCH_ANALYSIS_TTL_SEC,
    show_spinner="Loading analysis…",
)
def _cached_analyze_bundle(ticker: str, days, screener_key: str | None) -> dict | None:
    """
    One cached Analyze payload — single price API pass, snapshot headlines when
    available, and no redundant predictor price fetches.
    """
    sym = normalize_screener_ticker(ticker)
    market_eng = get_market_data()
    sentiment_eng = get_sentiment_engine()
    predictor_eng = get_predictor()

    price = market_eng.get_analyze_price_bundle(sym, days)
    if not price:
        return None

    news_items = get_cached_news_items(sym, screener_key=screener_key or None)
    headlines = [item["title"] for item in news_items]
    sent_result = sentiment_eng.analyze_headlines(sym, headlines)

    history = price["history"]
    latest_price = price["latest_price"]
    if len(history) >= 2:
        prev_price = history[-2]["price"]
        price_change_pct = (latest_price - prev_price) / prev_price if prev_price else 0
    else:
        price_change_pct = 0

    result = predictor_eng.predict(
        sym,
        headlines,
        market_data=market_eng,
        latest_price=latest_price,
        price_change_pct=price_change_pct,
        sentiment_score=sent_result["score"],
    )

    return {
        "news_items": news_items,
        "sent_result": sent_result,
        "result": result,
        "history": history,
        "latest_price": latest_price,
        "week52_low": price["week52_low"],
        "week52_high": price["week52_high"],
        "low_date": price["low_date"],
        "high_date": price["high_date"],
    }


# ── Sidebar ──────────────────────────────────────────────────────────
st.sidebar.image(logo_path_str(), use_container_width=True)
st.sidebar.markdown(
    """
    <div class="sidebar-brand">
      <div class="sidebar-brand-row">
        <span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">The Scoop 52</span>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
render_dark_mode_toggle()
st.sidebar.markdown("---")
st.sidebar.page_link("pages/1_NYSE_Top_10.py", label="📊 NYSE 10")
st.sidebar.page_link("pages/2_NASDAQ_Top_10.py", label="💹 NASDAQ 10")
st.sidebar.page_link("pages/3_Crypto_Top_10.py", label="🪙 Crypto 10")
st.sidebar.page_link("pages/5_CME_Top_10.py", label="🌾 CME Commodities 10")
st.sidebar.page_link("pages/6_ICE_Top_10.py", label="🛢️ ICE Commodities 10")
st.sidebar.markdown("---")

_analyze_mode = is_analyze_mode()
_analyze_ticker = query_param_ticker()
if _analyze_mode:
    st.session_state["search_terms_accepted"] = True

if _analyze_mode:
    st.sidebar.markdown(f"**Analyzing:** `{_analyze_ticker}`")
    ticker = _analyze_ticker
else:
    if "sidebar_ticker" not in st.session_state:
        st.session_state["sidebar_ticker"] = "DOGE"
    st.sidebar.text_input(
        "Enter Ticker",
        key="sidebar_ticker",
        placeholder="e.g. DOGE, BTC, TSLA",
    )
    ticker = st.session_state["sidebar_ticker"].strip().upper()

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
def _render_search_dashboard(ticker: str) -> None:
    """Renders analyze deep-dive; reruns on a timer so cached sentiment/news refresh without widget clicks."""
    is_dark_mode()
    days = PERIOD_OPTIONS[st.session_state["search_price_history_range"]]
    screener_key = analyze_screener_snapshot_key()
    bundle = _cached_analyze_bundle(ticker, days, screener_key)
    if not bundle:
        st.error(f"Could not find data for {ticker}. Please check the ticker symbol.")
        st.stop()

    news_items = bundle["news_items"]
    sent_result = bundle["sent_result"]
    result = bundle["result"]
    history = bundle["history"]
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

    asset_name = resolve_asset_display_name(ticker)
    st.markdown(
        f"""
        <div class="scoop-selected-asset-card" style="
            border:1px solid #cbd5e1;
            border-left:6px solid #2563eb;
            border-radius:12px;
            padding:0.9rem 1.1rem;
            margin:0 0 1rem 0;
            background:#f8fafc;
        ">
            <div class="scoop-muted" style="font-size:1rem;color:#64748b;font-weight:700;text-transform:uppercase;letter-spacing:0.04em;">
                Selected Asset
            </div>
            <div class="scoop-title-text" style="font-size:2rem;line-height:1.25;font-weight:800;color:#0f172a;">
                {html.escape(asset_name)}
            </div>
            <div class="scoop-subtitle-text" style="font-size:1.15rem;color:#475569;font-weight:700;margin-top:0.2rem;">
                Ticker: {html.escape(ticker)}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption(
        f"Headlines and sentiment reuse the same cached data as the Top 10 screeners (refreshed at most every "
        f"{_SEARCH_ANALYSIS_TTL_SEC // 60} minutes). Changing the price range only updates the chart."
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
        has_compare = False
        plot_df = df.copy()
        plot_df["date_dt"] = pd.to_datetime(plot_df["date"])
        comp_df = None

        ax_tick, ax_title = _search_price_chart_axis_px()
        margin_top = _search_price_chart_margin_top(has_compare)
        fig = _build_search_price_figure(
            has_compare=has_compare,
            plot_df=plot_df,
            comp_df=comp_df,
            ticker=ticker,
            compare_ticker="",
            axis_tick=ax_tick,
            axis_title=ax_title,
            margin_top=margin_top,
        )

        st.plotly_chart(fig, width="stretch")

    with col_mood:
        st.markdown("<div class='mood-column'>", unsafe_allow_html=True)
        mood_color = {"bullish": "#22c55e", "bearish": "#ef4444", "neutral": "#f59e0b"}.get(
            sentiment_label, "#94a3b8"
        )
        st.markdown(
            f"""
            <div class="scoop-mood-summary" style="
                border:1px solid #334155;
                border-radius:10px;
                padding:0.8rem 1rem;
                margin-bottom:0.7rem;
                background:#0f172a08;
            ">
                <div class="scoop-mood-label" style="display:flex;align-items:center;gap:0.6rem;font-weight:700;color:#0f172a;">
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
                <div class="scoop-mood-detail" style="margin-top:0.45rem;color:#334155;">
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
if _analyze_mode:
    st.session_state["search_terms_accepted"] = True
agreed = terms_accepted(st, "search_terms_accepted")
ensure_timezone_cookie(st)
if "search_price_history_range" not in st.session_state:
    st.session_state["search_price_history_range"] = "30 days"

ticker = ticker.strip().upper()
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

if not _analyze_mode:
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
if _analyze_mode:
    render_analyze_back_button()
st.title(f"{ticker} — Analyze" if _analyze_mode else f"{ticker} Dashboard")

if not _analyze_mode and not render_terms_gate(
    st,
    "agree_terms_search",
    "I have read and agree to the [Disclaimer & Terms of Service](/Terms_of_Service)",
    accepted_key="search_terms_accepted",
    warning_text="Please agree to the **Disclaimer & Terms of Service** to enable analysis.",
):
    pass
elif agreed:
    log_terms_acceptance(st, consent_key="agree_terms_search")

if ticker and (agreed or _analyze_mode):
    _render_search_dashboard(ticker)
elif not _analyze_mode:
    st.markdown(
        "<div style='text-align:center; padding:3rem 0; color:#9ca3af;'>"
        "<p style='font-size:4rem; margin:0.5rem 0;'>☝️</p>"
        "<p style='font-size:2rem;'>Click <strong>Analyze</strong> on a Top 10 row, "
        "or agree to the terms to view analysis.</p>"
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
    :root { --footer-sidebar-width: clamp(12rem, 20vw, 36rem); }
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
    @media (min-width: 769px) and (max-width: 1366px) {
        .disclaimer-footer {
            position: static !important;
            left: 0 !important;
            width: 100% !important;
            margin-top: 1.25rem !important;
            padding: 0.5rem 0.75rem !important;
            font-size: clamp(0.76rem, 1.8vw, 0.92rem) !important;
            line-height: 1.35 !important;
        }
        .disclaimer-footer strong,
        .disclaimer-footer a {
            font-size: inherit !important;
        }
        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"] {
            padding-bottom: 2.5rem !important;
        }
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

inject_dark_mode_styles()
install_tooltip_scroll_handler()