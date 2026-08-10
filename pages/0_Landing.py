"""
Mobile/tablet landing page — shown on first visit to `/` (width <= 1366px).

Desktop users are redirected to NYSE Top 10.
"""

import streamlit as st

from branding import logo_path_str, render_environment_banner
from landing_page import (
    DEFAULT_SCREENER_PAGE,
    inject_landing_seen_on_nav,
    redirect_if_desktop_on_landing,
)
from theme_mode import (
    inject_dark_mode_styles,
    install_theme_support,
    render_dark_mode_toggle,
)
from tooltip_scroll import install_responsive_sidebar_handler

st.set_page_config(
    page_title="The Scoop 52",
    page_icon=logo_path_str(),
    layout="wide",
    initial_sidebar_state="expanded",
)
render_environment_banner(st)
install_theme_support()
redirect_if_desktop_on_landing()
install_responsive_sidebar_handler()

st.markdown(
    """
    <style>
    [data-testid="stSidebarNav"] { display: none !important; }

    .landing-hero {
        text-align: center;
        padding: 1.25rem 0 1.75rem 0;
    }
    .landing-hero img {
        width: min(9rem, 42vw);
        margin: 0 auto 0.75rem auto;
        display: block;
    }
    .landing-hero h1 {
        font-size: clamp(2rem, 7vw, 3.4rem) !important;
        margin-bottom: 0.35rem !important;
    }
    .landing-hero p {
        font-size: clamp(1rem, 3.6vw, 1.35rem) !important;
        color: #475569;
        max-width: 40rem;
        margin: 0 auto;
        line-height: 1.55 !important;
    }

    .landing-grid {
        display: grid;
        grid-template-columns: 1fr;
        gap: 0.85rem;
        max-width: 42rem;
        margin: 0 auto;
    }
    .landing-card {
        border: 1px solid #cbd5e1;
        border-radius: 14px;
        padding: 1rem 1.1rem;
        background: #f8fafc;
    }
    .landing-card h3 {
        margin: 0 0 0.35rem 0 !important;
        font-size: clamp(1.15rem, 4vw, 1.45rem) !important;
    }
    .landing-card p {
        margin: 0 !important;
        color: #64748b;
        font-size: clamp(0.92rem, 3.2vw, 1.05rem) !important;
        line-height: 1.45 !important;
    }

    @media (min-width: 744px) and (max-width: 1366px) {
        .landing-grid {
            grid-template-columns: 1fr 1fr;
            max-width: 52rem;
        }
    }

    @media (min-width: 1367px) {
        .landing-hero, .landing-grid { display: none !important; }
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar (shared navigation) ───────────────────────────────────────
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
st.sidebar.page_link("pages/7_Terms_of_Service.py", label="📜 Terms of Service")

# ── Landing content (mobile/tablet) ───────────────────────────────────
_, hero_col, _ = st.columns([1, 2, 1])
with hero_col:
    st.image(logo_path_str(), width=140)
st.markdown(
    """
    <div class="landing-hero">
        <h1>The Scoop 52</h1>
        <p>
            Curated Top&nbsp;10 screeners for major markets — highlighting names
            at or near their 52-week lows with headline sentiment and market mood.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("### Choose a market")
st.markdown(
    """
    <div class="landing-grid">
        <div class="landing-card">
            <h3>📊 NYSE 10</h3>
            <p>Major NYSE-listed stocks near their 52-week lows.</p>
        </div>
        <div class="landing-card">
            <h3>💹 NASDAQ 10</h3>
            <p>Leading NASDAQ names trading near yearly lows.</p>
        </div>
        <div class="landing-card">
            <h3>🪙 Crypto 10</h3>
            <p>Top digital assets approaching their 52-week lows.</p>
        </div>
        <div class="landing-card">
            <h3>🌾 CME Commodities 10</h3>
            <p>Agricultural and soft commodities on CME.</p>
        </div>
        <div class="landing-card">
            <h3>🛢️ ICE Commodities 10</h3>
            <p>Energy and metals contracts on ICE.</p>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("")
col1, col2 = st.columns(2)
with col1:
    st.page_link("pages/1_NYSE_Top_10.py", label="📊 NYSE 10", use_container_width=True)
    st.page_link("pages/3_Crypto_Top_10.py", label="🪙 Crypto 10", use_container_width=True)
    st.page_link("pages/6_ICE_Top_10.py", label="🛢️ ICE Commodities 10", use_container_width=True)
with col2:
    st.page_link("pages/2_NASDAQ_Top_10.py", label="💹 NASDAQ 10", use_container_width=True)
    st.page_link("pages/5_CME_Top_10.py", label="🌾 CME Commodities 10", use_container_width=True)

if st.button("Start with NYSE 10 →", type="primary", use_container_width=True):
    st.switch_page(DEFAULT_SCREENER_PAGE)

inject_landing_seen_on_nav()
inject_dark_mode_styles()
