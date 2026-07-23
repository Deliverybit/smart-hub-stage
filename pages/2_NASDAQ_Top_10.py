"""
NASDAQ
Screens major NASDAQ-listed stocks for those trading at or near their
52-week / all-time low **and** whose recent headlines do NOT contain
signals of fraud, illegality, or imminent bankruptcy.
"""

import streamlit as st
import pandas as pd
from textblob import TextBlob
from datetime import datetime
from legal_consent_logger import ensure_timezone_cookie, log_terms_acceptance
from branding import logo_path_str, render_environment_banner
from market_data import MarketData
from app_config import get_screener_symbol_limit, SCREENER_CACHE_VERSION
from screener_headlines import enrich_headline_sentiment
from screener_page_data import load_screener_page_data
from screener_selection import (
    MAX_PAD_CAP_PCT,
    MARKET_MOOD_TIP,
    proximity_how_it_works,
    selection_status_message,
)
from tooltip_scroll import install_tooltip_scroll_handler
import html

# ── Page config ───────────────────────────────────────────────────────
st.set_page_config(
    page_title="NASDAQ",
    page_icon=logo_path_str(),
    layout="wide",
)
render_environment_banner(st)


@st.cache_resource
def get_market_data(_cache_version: int = SCREENER_CACHE_VERSION):
    return MarketData()

# ── Global responsive styling (shared with app.py) ────────────────────
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

    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@800;900&family=Montserrat:wght@800;900&display=swap');

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
    [data-testid="stTable"] table { width: 100% !important; }
    [data-testid="stTable"] th {
        font-size: 1.6rem !important; font-weight: 700 !important; padding: 14px 18px !important;
    }
    [data-testid="stTable"] td {
        font-size: 1.6rem !important; padding: 12px 18px !important;
    }
    /* Custom HTML results table & markdown tables */
    .stMarkdown table { width: 100% !important; border-collapse: collapse !important; }
    .stMarkdown table th {
        font-size: 1.6rem !important; font-weight: 700 !important;
        padding: 14px 18px !important; text-align: left !important;
        border-bottom: 2px solid #444 !important;
    }
    .stMarkdown table td {
        font-size: 1.6rem !important; padding: 12px 18px !important;
        border-bottom: 1px solid #333 !important;
    }
    .stMarkdown table tr:hover { background: rgba(255,255,255,0.04) !important; }

    /* Custom tooltip — appears ABOVE the element, interactive */
    .tip-wrap {
        position: relative !important;
        cursor: help !important;
        border-bottom: 1px dashed #888 !important;
    }
    .tip-wrap .tip-text {
        visibility: hidden !important;
        opacity: 0 !important;
        position: absolute !important;
        bottom: calc(100% + 12px) !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        min-width: 360px !important;
        max-width: 700px !important;
        background: #1e1e2f !important;
        color: #e2e8f0 !important;
        border: 1px solid #555 !important;
        border-radius: 8px !important;
        padding: 16px 20px !important;
        font-size: 0.95rem !important;
        line-height: 1.5 !important;
        font-weight: 400 !important;
        white-space: normal !important;
        z-index: 9999 !important;
        box-shadow: 0 4px 16px rgba(0,0,0,0.45) !important;
        pointer-events: auto !important;
        transition: opacity 0.15s ease-in-out, visibility 0.15s ease-in-out !important;
        overflow-y: visible !important;
        max-height: none !important;
    }
    .tip-wrap .tip-text::before {
        content: "" !important;
        position: absolute !important;
        bottom: -14px !important;
        left: 0 !important;
        width: 100% !important;
        height: 14px !important;
    }
    .tip-wrap .tip-text::after {
        content: "" !important;
        position: absolute !important;
        top: 100% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        border-width: 8px !important;
        border-style: solid !important;
        border-color: #1e1e2f transparent transparent transparent !important;
    }
    .tip-wrap:hover .tip-text,
    .tip-wrap .tip-text:hover {
        visibility: visible !important;
        opacity: 1 !important;
    }
    .tip-wrap .tip-text a {
        color: #60a5fa !important;
        text-decoration: underline !important;
        font-weight: 500 !important;
    }
    .tip-wrap .tip-text a:hover {
        color: #93c5fd !important;
    }

    @media (min-width: 1367px) {
        /* Full Results: keep header tooltips above the hovered heading so rows stay readable */
        .full-results-table thead .tip-wrap .tip-text {
            bottom: calc(100% + 12px) !important;
            top: auto !important;
        }
        .full-results-table thead .tip-wrap .tip-text::before {
            bottom: -14px !important;
            top: auto !important;
        }
        .full-results-table thead .tip-wrap .tip-text::after {
            top: 100% !important;
            bottom: auto !important;
            border-color: #1e1e2f transparent transparent transparent !important;
        }
        @supports (position-anchor: auto) {
            .full-results-table thead .tip-wrap .tip-text {
                position: fixed !important;
                left: anchor(center) !important;
                top: anchor(top) !important;
                bottom: auto !important;
                transform: translate(-50%, calc(-100% - 12px)) !important;
                max-width: min(700px, calc(100vw - 2rem)) !important;
            }
        }
        /* Body-row tooltips appear near the hovered text, upper-right of the trigger. */
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text {
            display: block !important;
            position: absolute !important;
            left: calc(100% + 12px) !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 8px) !important;
            transform: none !important;
            width: max-content !important;
            min-width: 260px !important;
            max-width: min(360px, calc(100vw - 2rem)) !important;
            max-height: min(45vh, 22rem) !important;
            overflow-y: auto !important;
            pointer-events: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text::before {
            display: block !important;
            content: "" !important;
            position: absolute !important;
            left: -14px !important;
            right: auto !important;
            top: 0 !important;
            bottom: 0 !important;
            width: 14px !important;
            height: 100% !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text::after {
            display: block !important;
            top: auto !important;
            bottom: 10px !important;
            left: -16px !important;
            transform: none !important;
            border-color: transparent #1e1e2f transparent transparent !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap:not(.headlines-tip) .tip-text:hover {
            visibility: hidden !important;
            opacity: 0 !important;
        }
    }

    /* Desktop/webview only: Headlines — narrow wrap + beside trigger (anchor) / right-edge fallback; mobile unchanged */
    @media (min-width: 1367px) {
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip {
            display: inline-block !important;
            padding: 0.2rem 0.45rem !important;
            margin: -0.1rem -0.25rem !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            transform: none !important;
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-pop-w) !important;
            min-width: var(--hl-pop-w) !important;
            max-width: var(--hl-pop-w) !important;
            height: auto !important;
            min-height: 0 !important;
            max-height: var(--hl-pop-h) !important;
            overflow: hidden !important;
            white-space: normal !important;
            text-align: left !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            z-index: 100020 !important;
            color: #ffffff !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            transition: opacity 0.25s ease-in-out 0.18s, visibility 0s linear 0.9s !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:hover .tip-text,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text:hover {
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 8px !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            transition-delay: 0s !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #111827 !important;
            -webkit-overflow-scrolling: touch !important;
            padding: 0.65rem 1rem 0.85rem 1rem !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 10px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border: 2px solid #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
            display: block !important;
            flex: 0 0 auto !important;
            position: static !important;
            margin: 0 !important;
            padding: 1.45rem 1rem 0.85rem 1rem !important;
            background: #1e1e2f !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            border-bottom: 1px solid #334155 !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::before,
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::after {
            display: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.45rem !important;
            padding-top: 0 !important;
            min-width: 0 !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.45rem 0.25rem !important;
            border-bottom: 1px solid rgba(148, 163, 184, 0.35) !important;
            line-height: 1.5 !important;
            font-size: 1.05rem !important;
            color: #ffffff !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line:last-child {
            border-bottom: none !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }
        .full-results-wrap:has(.tip-wrap.headlines-tip:hover) {
            overflow: visible !important;
        }
    }

    /* Sidebar — larger text & inputs */
    
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div { font-size: 1.5rem !important; }
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
    [data-testid="stSidebar"] input {
        font-size: 1.5rem !important;
        padding: 0.9rem 1.1rem !important;
        min-height: 3.4rem !important;
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

    /* Full Results (custom HTML table): wide content scrolls inside wrapper */
    .full-results-wrap {
        overflow-x: auto !important;
        -webkit-overflow-scrolling: touch !important;
        margin: 0.25rem 0 0.75rem 0 !important;
        max-width: 100% !important;
    }
    .full-results-wrap .full-results-table {
        display: table !important;
        width: max(100%, max-content) !important;
        border-collapse: collapse !important;
        table-layout: auto !important;
    }
    /* Mobile card layout adds a left-hand label; hide it on desktop tables */
    .full-results-wrap .full-results-table .fr-label {
        display: none !important;
    }
    .full-results-mobile-legend {
        display: none !important;
    }
    /* ===== MOBILE ===== */
    @media (max-width: 768px) {
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

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; line-height: 1.68 !important; }

        [data-testid="stMetricValue"] > div { font-size: clamp(1.95rem, 7.2vw, 2.8rem) !important; }
        [data-testid="stMetricLabel"] > div > div > p { font-size: clamp(1.08rem, 3.75vw, 1.28rem) !important; }
        [data-testid="stMetricDelta"] > div { font-size: clamp(1.04rem, 3.6vw, 1.22rem) !important; }

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

        /* Mobile: center hover tooltips so no horizontal scrolling is needed */
        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: 92vw !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
        }

        /* Full Results (mobile cards): show the per-cell heading/label on mobile only */
        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
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
            margin: 0.15rem -1rem 1.1rem -1rem !important;
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

        /* Top Picks (mobile only): make each pick read as a single card. */
        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 0.9rem 0.95rem 1rem 0.95rem !important;
            margin: 0 0 1rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.75rem 0.85rem 0.65rem 0.85rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.15rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 1.9rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.1rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.15rem 0 !important;
            padding: 0.6rem 0.85rem 0.85rem 0.85rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.15rem !important;
            line-height: 1.55 !important;
        }

        /* Full Results — column tips panel (optional) */
        .stMarkdown .full-results-mobile-legend {
            display: block !important;
            margin: 0 0 1rem 0 !important;
            padding: 0.65rem 0.75rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(0.9rem, 0.5rem + 2.2vw, 1rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.65rem !important;
            padding-bottom: 0.65rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.35rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.45 !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
        }

        /* Full Results — mobile: one vertical card per row (desktop: unchanged table) */
        .stMarkdown .full-results-wrap {
            margin-left: -0.5rem !important;
            margin-right: -0.5rem !important;
            width: calc(100% + 1rem) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 0.2rem max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.15rem 0 !important;
            padding: 0.65rem 0.85rem 0.75rem 0.85rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.35rem 0.65rem !important;
            align-items: start !important;
            padding: 0.48rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(0.95rem, 0.52rem + 2.4vw, 1.08rem) !important;
            line-height: 1.4 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        /* Tooltips — mobile: appear above the touched text; page scroll hides sticky hover */
        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(18rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(18rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }
        /* Headlines: tap count toggles checkbox; card overlay at top of row (same as tablet). */
        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: absolute !important;
            left: 0 !important;
            right: 0 !important;
            top: 0 !important;
            bottom: auto !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
            height: auto !important;
            max-height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            text-align: left !important;
            color: #ffffff !important;
            padding: 0.45rem 0.6rem !important;
            font-size: calc(0.82rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.15 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: scroll !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.28rem 0.35rem 0.35rem 0.55rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.28rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.32rem 0.38rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.28 !important;
            font-size: calc(0.72rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.72rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }
    }

    /* ===== TABLET (769px–1366px) — mobile card layout; mobile/desktop unchanged ===== */
    @media (min-width: 769px) and (max-width: 1366px) {

        :root {
            --scoop-sidebar-width: clamp(16rem, 42vw, 28rem);
            --footer-sidebar-width: 0px;
        }

        .stApp {
            overflow-x: hidden !important;
        }

        /* Main content uses full viewport width (sidebar overlays when open). */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div {
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
            max-width: min(92vw, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-105%) !important;
            transition: transform 0.28s ease !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
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
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stExpandSidebarButton"],
        [data-testid="collapsedControl"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 1000006 !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] {
            display: flex !important;
            color: #31333f !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 0.5rem !important;
            background: #ffffff !important;
            box-shadow: 0 1px 6px rgba(15, 23, 42, 0.12) !important;
        }
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stExpandSidebarButton"],
        [data-testid="stExpandSidebarButton"] button,
        [data-testid="collapsedControl"] button {
            min-width: 2.75rem !important;
            min-height: 2.75rem !important;
            color: #31333f !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarHeader"] {
            position: relative !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            position: absolute !important;
            top: 0.35rem !important;
            right: 0.35rem !important;
            left: auto !important;
            z-index: 1000007 !important;
            background: rgba(255, 255, 255, 0.95) !important;
            border-radius: 0.5rem !important;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.18) !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] button {
            color: #31333f !important;
        }
        .scoop-responsive-sidebar-close {
            position: fixed !important;
            z-index: 10000010 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 2.85rem !important;
            height: 2.85rem !important;
            padding: 0 !important;
            margin: 0 !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 0.55rem !important;
            background: #ffffff !important;
            color: #0f172a !important;
            font-size: 1.45rem !important;
            font-weight: 800 !important;
            line-height: 1 !important;
            box-shadow: 0 3px 14px rgba(15, 23, 42, 0.24) !important;
            cursor: pointer !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
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
            margin: 0.15rem -1rem 1.1rem -1rem !important;
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
            padding-left: 1.1rem !important;
            padding-right: 1.1rem !important;
            padding-bottom: 2.5rem !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }

        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
            font-size: clamp(1.1rem, 2.4vw, 1.32rem) !important;
        }

        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.72rem, 1.8vw, 1rem) !important;
            padding-bottom: clamp(0.72rem, 1.8vw, 1rem) !important;
            line-height: 1.55 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(1.08rem, 2.4vw, 1.28rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 1rem 1.05rem 1.1rem 1.05rem !important;
            margin: 0 0 1.15rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.85rem 0.95rem 0.75rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.35rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 2.35rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.25rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.2rem 0 !important;
            padding: 0.7rem 0.95rem 0.95rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.3rem !important;
            line-height: 1.58 !important;
        }

        .stMarkdown .full-results-mobile-legend {
            display: block !important;
            margin: 0 0 1.1rem 0 !important;
            padding: 0.8rem 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.72rem !important;
            padding-bottom: 0.72rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.4rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.5 !important;
            font-size: clamp(1.02rem, 2.1vw, 1.18rem) !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
            font-size: clamp(1.08rem, 2.25vw, 1.24rem) !important;
        }

        .stMarkdown .full-results-wrap {
            margin-left: -0.5rem !important;
            margin-right: -0.5rem !important;
            width: calc(100% + 1rem) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 0.2rem max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.2rem 0 !important;
            padding: 0.85rem 1rem 0.95rem 1rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.45rem 0.75rem !important;
            align-items: start !important;
            padding: 0.58rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(1.12rem, 2.5vw, 1.38rem) !important;
            line-height: 1.5 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(22rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(22rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 0.95rem 1.05rem !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
        }

        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
            font-size: clamp(1.08rem, 2.3vw, 1.28rem) !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 100001 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: 0 !important;
            background: rgba(15, 23, 42, 0.12) !important;
            cursor: default !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
            display: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
            position: relative !important;
            z-index: 100003 !important;
            overflow: visible !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
            position: static !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            width: var(--hl-fixed-width, 40vw) !important;
            min-width: 0 !important;
            max-width: var(--hl-fixed-width, 40vw) !important;
            height: auto !important;
            max-height: var(--hl-fixed-max-height, calc(100dvh - 1.5rem)) !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            flex-shrink: 0 !important;
            display: block !important;
            visibility: visible !important;
            position: relative !important;
            z-index: 2 !important;
            text-align: left !important;
            color: #ffffff !important;
            padding: 0.55rem 0.75rem !important;
            font-size: calc(1rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.2 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.35rem 0.45rem 0.45rem 0.65rem !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 8px !important;
            -webkit-appearance: none !important;
            display: block !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #1e293b !important;
            border-radius: 4px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border-radius: 4px !important;
            min-height: 28px !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.35rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.42rem 0.48rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.35 !important;
            font-size: calc(0.95rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.95rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }

    }
    /* Hard override so sidebar brand stays exactly 60px */
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
    </style>
    """,
    unsafe_allow_html=True,
)
install_tooltip_scroll_handler()

# ── Custom sidebar navigation ─────────────────────────────────────────
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
st.sidebar.page_link("pages/1_NYSE_Top_10.py", label="📊 NYSE 10")
st.sidebar.page_link("pages/2_NASDAQ_Top_10.py", label="💹 NASDAQ 10")
st.sidebar.page_link("pages/3_Crypto_Top_10.py", label="🪙 Crypto 10")
st.sidebar.page_link("pages/5_CME_Top_10.py", label="🌾 CME Commodities 10")
st.sidebar.page_link("pages/6_ICE_Top_10.py", label="🛢️ ICE Commodities 10")
st.sidebar.page_link("app.py", label="🔎 Search")
st.sidebar.markdown("---")
st.sidebar.page_link("pages/7_Terms_of_Service.py", label="📜 Terms of Service")
agreed = st.session_state.get("agree_terms_nasdaq", False)
ensure_timezone_cookie(st)
if agreed:
    log_terms_acceptance(st, consent_key="agree_terms_nasdaq")

# ── Constants ─────────────────────────────────────────────────────────
# A broad universe of well-known NASDAQ-listed stocks across sectors.
COMPANY_NAMES = {
    # Big Tech / Mega-cap
    "AAPL": "Apple Inc.",
    "MSFT": "Microsoft Corp.",
    "AMZN": "Amazon.com Inc.",
    "GOOGL": "Alphabet Inc. (Class A)",
    "GOOG": "Alphabet Inc. (Class C)",
    "META": "Meta Platforms Inc.",
    "NVDA": "NVIDIA Corp.",
    "TSLA": "Tesla Inc.",
    "AVGO": "Broadcom Inc.",
    "ADBE": "Adobe Inc.",
    # Semiconductors
    "AMD": "Advanced Micro Devices",
    "INTC": "Intel Corp.",
    "QCOM": "Qualcomm Inc.",
    "TXN": "Texas Instruments",
    "MU": "Micron Technology",
    "MRVL": "Marvell Technology",
    "LRCX": "Lam Research Corp.",
    "KLAC": "KLA Corp.",
    "AMAT": "Applied Materials",
    "ON": "ON Semiconductor",
    # Software / Cloud
    "CRM": "Salesforce Inc.",
    "ORCL": "Oracle Corporation",
    "NOW": "ServiceNow Inc.",
    "INTU": "Intuit Inc.",
    "PANW": "Palo Alto Networks",
    "CRWD": "CrowdStrike Holdings",
    "SNPS": "Synopsys Inc.",
    "CDNS": "Cadence Design Systems",
    "WDAY": "Workday Inc.",
    "ZS": "Zscaler Inc.",
    "DDOG": "Datadog Inc.",
    "FTNT": "Fortinet Inc.",
    "TEAM": "Atlassian Corp.",
    "TTD": "The Trade Desk Inc.",
    "HUBS": "HubSpot Inc.",
    "NET": "Cloudflare Inc.",
    "MDB": "MongoDB Inc.",
    "SNOW": "Snowflake Inc.",
    "OKTA": "Okta Inc.",
    "ZM": "Zoom Video Communications",
    "DOCU": "DocuSign Inc.",
    "U": "Unity Software Inc.",
    # Internet / E-Commerce
    "NFLX": "Netflix Inc.",
    "BKNG": "Booking Holdings",
    "ABNB": "Airbnb Inc.",
    "MELI": "MercadoLibre Inc.",
    "PYPL": "PayPal Holdings",
    "XYZ": "Block Inc.",
    "COIN": "Coinbase Global",
    "ROKU": "Roku Inc.",
    "PINS": "Pinterest Inc.",
    "SNAP": "Snap Inc.",
    "LYFT": "Lyft Inc.",
    "DASH": "DoorDash Inc.",
    "HOOD": "Robinhood Markets",
    # Biotech / Pharma
    "AMGN": "Amgen Inc.",
    "GILD": "Gilead Sciences",
    "VRTX": "Vertex Pharmaceuticals",
    "REGN": "Regeneron Pharmaceuticals",
    "MRNA": "Moderna Inc.",
    "BIIB": "Biogen Inc.",
    "ILMN": "Illumina Inc.",
    "DXCM": "DexCom Inc.",
    "IDXX": "IDEXX Laboratories",
    "ISRG": "Intuitive Surgical",
    # Telecom / Media
    "CMCSA": "Comcast Corp.",
    "TMUS": "T-Mobile US",
    "CHTR": "Charter Communications",
    "WBD": "Warner Bros. Discovery",
    "EA": "Electronic Arts",
    "TTWO": "Take-Two Interactive",
    # Consumer / Food / Beverage
    "COST": "Costco Wholesale",
    "PEP": "PepsiCo Inc.",
    "SBUX": "Starbucks Corp.",
    "MNST": "Monster Beverage Corp.",
    "KDP": "Keurig Dr Pepper",
    "MDLZ": "Mondelez International",
    "KHC": "The Kraft Heinz Co.",
    # EV / Auto
    "RIVN": "Rivian Automotive",
    "LCID": "Lucid Group",
    # Fintech / Financial
    "AFRM": "Affirm Holdings",
    "SOFI": "SoFi Technologies",
    "UPST": "Upstart Holdings",
}

NASDAQ_UNIVERSE = list(COMPANY_NAMES.keys())

COMPANY_SUMMARIES = {
    "AAPL": "Consumer electronics and software giant; maker of iPhone, Mac, iPad, and Apple services.",
    "MSFT": "Enterprise software leader in cloud (Azure), Office 365, Windows, and gaming (Xbox).",
    "AMZN": "Global e-commerce and cloud computing leader via Amazon Web Services (AWS).",
    "GOOGL": "Parent of Google; dominates search, advertising, YouTube, and cloud services.",
    "GOOG": "Alphabet Class C shares; same business as GOOGL without voting rights.",
    "META": "Social media conglomerate operating Facebook, Instagram, WhatsApp, and Reality Labs.",
    "NVDA": "Leading designer of GPUs for gaming, data centers, and AI/ML workloads.",
    "TSLA": "Electric vehicle manufacturer and clean energy company; also in AI and robotics.",
    "AVGO": "Semiconductor company supplying networking, broadband, and storage chips.",
    "ADBE": "Creative and marketing software leader with Photoshop, Illustrator, and Experience Cloud.",
    "AMD": "Designs CPUs and GPUs for PCs, data centers, and gaming consoles.",
    "INTC": "Legacy chipmaker producing CPUs for PCs and servers; investing in foundry services.",
    "QCOM": "Leading mobile chipmaker supplying processors and modems for smartphones.",
    "TXN": "Analog and embedded semiconductor company serving industrial and automotive markets.",
    "MU": "Major manufacturer of DRAM and NAND flash memory chips.",
    "MRVL": "Semiconductor company focused on data infrastructure for cloud and 5G.",
    "LRCX": "Manufactures wafer fabrication equipment for the semiconductor industry.",
    "KLAC": "Makes process control and yield management systems for chip manufacturing.",
    "AMAT": "Largest supplier of semiconductor manufacturing equipment worldwide.",
    "ON": "Semiconductor company focused on automotive, industrial, and IoT power solutions.",
    "CRM": "Cloud-based CRM platform and enterprise software company.",
    "ORCL": "Enterprise software giant specializing in cloud infrastructure and databases.",
    "NOW": "Cloud platform for IT service management and enterprise digital workflows.",
    "INTU": "Financial software maker of TurboTax, QuickBooks, and Credit Karma.",
    "PANW": "Leading cybersecurity company offering next-gen firewalls and cloud security.",
    "CRWD": "Cloud-native endpoint security and threat intelligence platform.",
    "SNPS": "Electronic design automation tools for semiconductor chip design.",
    "CDNS": "EDA software and IP for designing integrated circuits and SoCs.",
    "WDAY": "Cloud-based enterprise software for human resources and financial management.",
    "ZS": "Cloud security company providing zero-trust internet access for enterprises.",
    "DDOG": "Cloud monitoring and analytics platform for infrastructure and applications.",
    "FTNT": "Cybersecurity company providing firewalls, endpoint, and network security.",
    "TEAM": "Maker of Jira, Confluence, and Trello for team collaboration and project management.",
    "TTD": "Demand-side platform for programmatic digital advertising.",
    "HUBS": "Inbound marketing, sales, and CRM platform for growing businesses.",
    "NET": "Cloud platform providing CDN, DDoS protection, and internet security services.",
    "MDB": "Developer data platform built around the MongoDB NoSQL database.",
    "SNOW": "Cloud-based data warehousing and analytics platform.",
    "OKTA": "Identity and access management platform for enterprises.",
    "ZM": "Video conferencing and collaboration platform for businesses and consumers.",
    "DOCU": "E-signature and contract lifecycle management platform.",
    "U": "Real-time 3D development platform for gaming, AR/VR, and simulations.",
    "NFLX": "World's largest streaming entertainment service with original content.",
    "BKNG": "Online travel agency operating Booking.com, Priceline, and Kayak.",
    "ABNB": "Online marketplace for short-term vacation rentals and travel experiences.",
    "MELI": "Largest e-commerce and fintech platform in Latin America.",
    "PYPL": "Digital payments platform enabling online money transfers and commerce.",
    "XYZ": "Financial services and digital payments company (Cash App, Square POS).",
    "COIN": "Largest U.S. cryptocurrency exchange platform.",
    "ROKU": "Streaming platform and smart TV operating system maker.",
    "PINS": "Visual discovery and bookmarking platform for ideas and inspiration.",
    "SNAP": "Social media company operating Snapchat, Spectacles, and AR tools.",
    "LYFT": "Ride-sharing and transportation network company in the U.S. and Canada.",
    "DASH": "On-demand food delivery and local commerce platform.",
    "HOOD": "Commission-free stock, crypto, and options trading platform.",
    "AMGN": "Biotech company developing therapies for oncology, cardiovascular, and inflammation.",
    "GILD": "Biopharmaceutical company focused on antivirals (HIV, hepatitis) and oncology.",
    "VRTX": "Biotech company leading in cystic fibrosis treatments and gene editing.",
    "REGN": "Biotech known for Dupixent (eczema/asthma) and Eylea (eye disease).",
    "MRNA": "Biotech pioneer in mRNA vaccines and therapeutics.",
    "BIIB": "Neuroscience-focused biotech developing treatments for Alzheimer's and MS.",
    "ILMN": "Genomics company manufacturing DNA sequencing and array-based technologies.",
    "DXCM": "Maker of continuous glucose monitoring systems for diabetes management.",
    "IDXX": "Veterinary diagnostics and software company serving animal health.",
    "ISRG": "Maker of the da Vinci robotic surgical system for minimally invasive surgery.",
    "CMCSA": "Media conglomerate operating Comcast Cable, NBCUniversal, and Sky.",
    "TMUS": "Major U.S. wireless carrier known for aggressive pricing and 5G network.",
    "CHTR": "Second-largest cable operator in the U.S. under the Spectrum brand.",
    "WBD": "Media company operating Warner Bros. studios, HBO, CNN, and Discovery networks.",
    "EA": "Major video game publisher of FIFA/EA Sports, Madden, Apex Legends, and The Sims.",
    "TTWO": "Video game publisher behind Grand Theft Auto, NBA 2K, and Red Dead Redemption.",
    "COST": "Membership-based warehouse club offering bulk goods at discount prices.",
    "PEP": "Global food and beverage company with brands like Pepsi, Lay's, Gatorade, Quaker.",
    "SBUX": "World's largest coffeehouse chain with global café and retail operations.",
    "MNST": "Energy drink company behind Monster Energy, Reign, and Bang brands.",
    "KDP": "Beverage company with Dr Pepper, Snapple, Keurig coffee systems, and more.",
    "MDLZ": "Global snack company with Oreo, Cadbury, Toblerone, and Ritz brands.",
    "KHC": "Food company with Kraft, Heinz, Oscar Mayer, and Philadelphia brands.",
    "RIVN": "Electric vehicle startup making the R1T pickup truck and R1S SUV.",
    "LCID": "Luxury EV manufacturer producing the Lucid Air sedan.",
    "AFRM": "Buy-now-pay-later fintech offering installment payment plans at checkout.",
    "SOFI": "Digital personal finance company offering loans, investing, and banking.",
    "UPST": "AI-powered lending platform that partners with banks for personal loans.",
}

# Keywords that disqualify a stock
DISQUALIFY_KEYWORDS = [
    "fraud", "illegal", "lawsuit", "bankrupt", "bankruptcy", "indicted",
    "indictment", "criminal", "sec charges", "securities fraud",
    "going out of business", "shutting down", "closing all",
    "delisted", "ponzi", "embezzlement", "money laundering",
    "accounting scandal", "class action", "fda rejection",
]

SCREENER_SYMBOL_LIMIT = get_screener_symbol_limit()


# ── Helper functions ──────────────────────────────────────────────────
def screen_stock(ticker: str) -> dict | None:
    """Return screening data for one ticker, or None on failure."""
    try:
        import math
        market_data = get_market_data()
        snapshot = market_data.get_market_snapshot(ticker)
        if not snapshot:
            return None
        current_price = snapshot["current_price"]
        year_low = snapshot["year_low"]
        year_high = snapshot["year_high"]

        if (current_price is None or year_low is None or year_high is None
                or (isinstance(year_low, float) and math.isnan(year_low))
                or (isinstance(year_high, float) and math.isnan(year_high))
                or (isinstance(current_price, float) and math.isnan(current_price))
                or year_low <= 0):
            return None

        pct_above_low = ((current_price - year_low) / year_low) * 100

        # Keep screener calls price-first so Alpha Vantage rate limits do not
        # block the whole Top 10 table. Detailed headline analysis remains on Search.
        news = []
        headlines = []
        headline_links = []
        for item in news:
            title = item.get("title", "")
            url = item.get("url", "")
            if title:
                headlines.append(title)
                headline_links.append(url)

        lower_headlines = " ".join(headlines).lower()
        for kw in DISQUALIFY_KEYWORDS:
            if kw in lower_headlines:
                return None

        polarity = 0.0
        if headlines:
            for hl in headlines:
                polarity += TextBlob(hl).sentiment.polarity
            polarity /= len(headlines)

        if polarity < -0.35:
            return None

        if pct_above_low < 0:
            signal = "BELOW LOW"
        elif pct_above_low <= 2:
            signal = "AT LOW"
        else:
            signal = "NEAR LOW"

        return {
            "Ticker": ticker,
            "_source_ticker": ticker,
            "Company": COMPANY_NAMES.get(ticker, ticker),
            "Price": current_price,
            "52W Low": year_low,
            "52W High": year_high,
            "% Above Low": round(pct_above_low, 2),
            "Headline Sentiment": round(polarity, 3),
            "Headlines": len(headlines),
            "Market Mood": signal,
            "_headline_texts": headlines,
            "_headline_urls": headline_links,
        }
    except Exception:
        return None


# ── Exchange performance banner ───────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)
def _fetch_index(ticker: str):
    """Return (price, daily_change_pct) for an index ticker."""
    try:
        return get_market_data().get_daily_change(ticker)
    except Exception:
        return None, None

idx_price, idx_chg = _fetch_index("^IXIC")
if idx_price is not None:
    chg_color = "#22c55e" if idx_chg >= 0 else "#ef4444"
    arrow = "▲" if idx_chg >= 0 else "▼"
    st.markdown(
        f'''<div style="
            max-width: 50%;
            background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
            border: 1px solid #334155;
            border-left: 4px solid {chg_color};
            border-radius: 12px;
            padding: 1.2rem 1.8rem;
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 1.5rem;
            flex-wrap: wrap;
        ">
            <span style="font-size:1.4rem;color:#e2e8f0;font-weight:500;">NASDAQ Composite (^IXIC) — Today</span>
            <span style="font-size:2.2rem;font-weight:700;color:#f1f5f9;">{idx_price:,.2f}</span>
            <span style="font-size:1.4rem;font-weight:600;color:{chg_color};
                background:{chg_color}18;padding:0.3rem 0.8rem;border-radius:6px;">
                {arrow} {idx_chg:+.2f}%
            </span>
        </div>''',
        unsafe_allow_html=True,
    )

# ── UI ────────────────────────────────────────────────────────────────
st.title("💹 NASDAQ")
st.markdown(
    "Screens **{}** major NASDAQ-listed stocks for those trading **at or near "
    "their 52-week low** using Alpha Vantage daily market data. "
    "Headline sentiment is fetched for the final displayed rows.".format(len(NASDAQ_UNIVERSE))
)

st.markdown("---")

st.info(proximity_how_it_works("stock"))

@st.cache_data(ttl=900, show_spinner="Refreshing NASDAQ data…")
def _run_screen(_cache_version: int = SCREENER_CACHE_VERSION):
    results = []
    scan_universe = NASDAQ_UNIVERSE[:SCREENER_SYMBOL_LIMIT]
    for tkr in scan_universe:
        row = screen_stock(tkr)
        if row is not None:
            results.append(row)
    return results, datetime.now().strftime("%b %d, %Y  %I:%M %p")

if not agreed:
    st.warning("Please agree to the **Disclaimer & Terms of Service** to view results.")
    agreed = st.checkbox(
        "I agree to the [Disclaimer & Terms](/Terms_of_Service)",
        key="agree_terms_nasdaq",
    )
    if agreed:
        log_terms_acceptance(st, consent_key="agree_terms_nasdaq")
else:
    loaded = load_screener_page_data(
        "NASDAQ",
        universe_size=len(NASDAQ_UNIVERSE),
        asset_noun="stocks",
        run_live=_run_screen,
    )
    all_results = loaded.all_results
    results = loaded.display_results
    last_updated = loaded.last_updated
    scanned_count = loaded.scanned_count
    selection = loaded.selection

    st.markdown(
        f'<div style="text-align:right;color:#64748b;font-size:1.1rem;margin-bottom:0.5rem;">'
        f'Last updated: <b>{last_updated}</b>  ·  Auto-refreshes every 15 min</div>',
        unsafe_allow_html=True,
    )

    if not all_results:
        st.warning(
            "No stock data is available right now. Alpha Vantage may be rate-limiting "
            "requests; wait a minute and refresh."
        )
        if st.button("Clear cache and refresh", key="refresh_nasdaq"):
            st.cache_data.clear()
            st.rerun()
    elif not results:
        st.warning(
            f"No stocks are within **{MAX_PAD_CAP_PCT}%** of their 52-week low right now."
        )
        if st.button("Clear cache and refresh", key="refresh_nasdaq"):
            st.cache_data.clear()
            st.rerun()
    else:
        df = pd.DataFrame(results)
        df = df.sort_values("% Above Low", ascending=True).reset_index(drop=True)
        if not loaded.headlines_enriched:
            df = enrich_headline_sentiment(df, get_market_data())
        df["Headlines"] = df["Headlines"].clip(upper=10)
        df["_headline_texts"] = df["_headline_texts"].apply(lambda items: items[:10])
        df["_headline_urls"] = df["_headline_urls"].apply(lambda items: items[:10])
        df.index = df.index + 1

        level, status_msg = selection_status_message(
            selection,
            asset_noun=loaded.asset_noun,
            scanned_count=scanned_count,
            universe_size=len(NASDAQ_UNIVERSE),
        )
        getattr(st, level)(status_msg)

        # ── Metrics row for top 3 ─────────────────────────────────────
        st.markdown("### 🏆 Top Picks")
        top_cols = st.columns(min(3, len(df)))
        for idx, col in enumerate(top_cols):
            if idx >= len(df):
                break
            row = df.iloc[idx]
            with col:
                delta_txt = f"{row['% Above Low']:+.1f}% above 52W low"
                st.metric(
                    label=f"#{idx + 1}  {row['Ticker']}",
                    value=f"${row['Price']:,.2f}",
                    delta=delta_txt,
                    delta_color="normal",
                )
                tip = COMPANY_SUMMARIES.get(row["Ticker"], "")
                if row["Market Mood"] == "BELOW LOW":
                    badge = "🚨 BELOW 52W LOW — New Floor"
                elif row["Market Mood"] == "AT LOW":
                    badge = "🔥 AT 52W LOW"
                else:
                    badge = "📉 NEAR 52W LOW"
                st.markdown(
                    f'<div style="font-size:1.5rem;line-height:1.8;">'
                    f'<span class="tip-wrap" style="font-weight:700;">'
                    f'{row["Company"]}'
                    f'<span class="tip-text">{tip}</span></span><br>'
                    f'52W Low: <b style="color:#22c55e;">${row["52W Low"]:,.2f}</b> · '
                    f'52W High: <b>${row["52W High"]:,.2f}</b><br>'
                    f'Sentiment: <b>{row["Headline Sentiment"]:+.3f}</b><br>'
                    f'<b>{badge}</b>'
                    f'</div>',
                    unsafe_allow_html=True,
                )

        # ── Full table (HTML with hover tooltips) ─────────────────────
        st.markdown("### 📋 Full Results")

        headline_map = {}
        for _, r in df.iterrows():
            texts = r.get("_headline_texts", [])
            urls = r.get("_headline_urls", [])
            headline_map[r["Ticker"]] = list(zip(texts, urls))

        display_df = df.drop(columns=["_source_ticker", "_headline_texts", "_headline_urls"], errors="ignore").copy()
        display_df["Price"] = display_df["Price"].apply(lambda x: f"${x:,.2f}")
        display_df["52W Low"] = display_df["52W Low"].apply(lambda x: f"${x:,.2f}")
        display_df["52W High"] = display_df["52W High"].apply(lambda x: f"${x:,.2f}")
        display_df["% Above Low"] = display_df["% Above Low"].apply(lambda x: f"{x:.2f}%")
        display_df["Headline Sentiment"] = display_df["Headline Sentiment"].apply(lambda x: f"{x:+.3f}")

        COLUMN_TIPS = {
            "Headline Sentiment": "Average polarity score of recent news headlines (TextBlob). Ranges from -1.0 (very negative) to +1.0 (very positive). Stocks below -0.35 are automatically disqualified.",
            "Headlines": "Number of recent news headlines found for this stock. More headlines give a more reliable sentiment reading.",
            "Market Mood": MARKET_MOOD_TIP,
            "% Above Low": "How far the current price is above the 52-week low, expressed as a percentage. Lower is closer to the floor.",
        }

        def _tip(text, tooltip, anchor_id: str = ""):
            anchor_style = f' style="anchor-name: {anchor_id};"' if anchor_id else ""
            tip_style = f' style="position-anchor: {anchor_id};"' if anchor_id else ""
            return (
                f'<span class="tip-wrap"{anchor_style}>{text}'
                f'<span class="tip-text"{tip_style}>{tooltip}</span></span>'
            )

        def _headlines_tip(count_display, hl_pairs: list, row_idx: int) -> str:
            aid = f"--hl-r{int(row_idx)}"
            rows_inner = []
            for title, url in hl_pairs:
                stitle = html.escape(str(title))
                if url:
                    surl = html.escape(str(url), quote=True)
                    rows_inner.append(
                        f'<div class="hl-tip-line"><a href="{surl}" target="_blank" '
                        f'rel="noopener noreferrer">{stitle}</a></div>'
                    )
                else:
                    rows_inner.append(f'<div class="hl-tip-line">{stitle}</div>')
            list_html = "".join(rows_inner)
            cb_id = f"hl-cb-r{int(row_idx)}"
            return (
                f'<span class="tip-wrap headlines-tip" style="anchor-name: {aid};">'
                f'<input type="checkbox" id="{cb_id}" class="hl-tip-cb" aria-hidden="true">'
                f'<label class="hl-tip-count" for="{cb_id}">'
                f"{html.escape(str(count_display))}</label>"
                f'<label class="hl-tip-backdrop" for="{cb_id}" aria-hidden="true">'
                f"<span>&nbsp;</span></label>"
                f'<span class="tip-text" style="position-anchor: {aid};">'
                f'<span class="hl-tip-heading">Headlines</span>'
                f'<div class="headlines-tip-scroll">'
                f'<div class="headlines-tip-list">{list_html}</div>'
                f"</div>"
                f"</span></span>"
            )

        def _attr_html(s):
            return (
                str(s)
                .replace("&", "&amp;")
                .replace('"', "&quot;")
                .replace("<", "&lt;")
            )

        def _td(col_label: str, inner_html: str, label_tip: str = "") -> str:
            label_html = _attr_html(col_label)
            if label_tip:
                label_html = _tip(_attr_html(col_label), html.escape(label_tip))
            return (
                f'<td data-label="{_attr_html(col_label)}">'
                f'<span class="fr-label">{label_html}</span>'
                f'<span class="fr-val">{inner_html}</span></td>'
            )

        def _build_html_table(dataframe):
            cols = list(dataframe.columns)
            rows_html = ""
            header_cells = '<th>#</th>'
            for idx_col, c in enumerate(cols):
                tip = COLUMN_TIPS.get(c, "")
                if tip:
                    header_cells += f'<th>{_tip(c, tip, f"--frh-{idx_col}")}</th>'
                else:
                    header_cells += f"<th>{c}</th>"
            for idx_row, (i, r) in enumerate(dataframe.iterrows()):
                cells = _td("#", str(i))
                for c in cols:
                    val = r[c]
                    if c == "Company":
                        tip = COMPANY_SUMMARIES.get(r["Ticker"], "")
                        cells += (
                            _td(c, _tip(val, tip), COLUMN_TIPS.get(c, "")) if tip else _td(c, str(val), COLUMN_TIPS.get(c, ""))
                        )
                    elif c == "Headlines":
                        hl_pairs = headline_map.get(r["Ticker"], [])
                        if hl_pairs:
                            cells += _td(c, _headlines_tip(val, hl_pairs, idx_row), COLUMN_TIPS.get(c, ""))
                        else:
                            cells += _td(c, str(val), COLUMN_TIPS.get(c, ""))
                    else:
                        cells += _td(c, str(val), COLUMN_TIPS.get(c, ""))
                rows_html += f"<tr>{cells}</tr>"
            return (
                f'<div class="full-results-wrap">'
                f'<table class="full-results-table"><thead><tr>{header_cells}</tr></thead>'
                f"<tbody>{rows_html}</tbody></table></div>"
            )

        _fr_legend_rows = "".join(
            f"<div class='fr-mobile-tip-row'><strong>{html.escape(c)}</strong>"
            f"<p>{html.escape(t)}</p></div>"
            for c, t in COLUMN_TIPS.items()
        )
        st.markdown(
            f'<div class="full-results-mobile-legend">{_fr_legend_rows}</div>',
            unsafe_allow_html=True,
        )
        st.markdown(_build_html_table(display_df), unsafe_allow_html=True)

        # ── Explanation card ──────────────────────────────────────────
        st.markdown("---")
        st.markdown(
            """
            #### 🧠 Why these assets were selected

            | Criterion | Check |
            |-----------|-------|
            | **Near 52-week low** | Price is within 30% of the lowest price in the past year (15% preferred) |
            | **No scandal headlines** | Recent news contains no keywords related to fraud, lawsuits, bankruptcy, or delisting |
            | **Headline context** | Detailed headline sentiment is available on the Search page |

            > **Disclaimer:** This is an automated screen — not financial advice.
            > Always do your own due diligence before investing.
            """
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
