"""
Terms of Service & Financial Disclaimer
"""

import streamlit as st
from branding import logo_path_str

st.set_page_config(
    page_title="Terms of Service",
    page_icon=logo_path_str(),
    layout="wide",
)

# ── Global responsive styling (shared with other pages) ───────────────
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
    /* Alerts */
    .stAlert p, [data-testid="stAlert"] p { font-size: 1.6rem !important; }
    /* Captions */
    .stCaption p, [data-testid="stCaptionContainer"] p { font-size: 1.4rem !important; }

    /* Sidebar — larger text & inputs */
    [data-testid="stSidebar"] { min-width: 380px !important; }
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] span,
    [data-testid="stSidebar"] div { font-size: 1.5rem !important; }
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
    [data-testid="stSidebar"] a { font-size: 1.5rem !important; }
    [data-testid="stSidebarNav"] { display: none !important; }

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

        .stCaption p { font-size: clamp(0.98rem, 3.4vw, 1.12rem) !important; }

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
        [data-testid="stSidebar"] { min-width: 280px !important; }

        /* Sticky disclaimer: keep readable but not overwhelming */
        .disclaimer-footer {
            font-size: clamp(0.76rem, 2.9vw, 0.92rem) !important;
            line-height: 1.4 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.78rem, 3vw, 0.94rem) !important;
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
            font-size: clamp(1.25rem, 4.6vw, 1.55rem) !important;
            line-height: 1.25 !important;
        }
    }

    /* ===== TABLET ===== */
    @media (min-width: 769px) and (max-width: 1200px) {
        html, body, [class*="css"] { font-size: 26px !important; }
        h1 { font-size: 3.4rem !important; }
    }
    [data-testid="stSidebar"] #scoop-title {
        font-size: 60px !important;
        line-height: 1.05 !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Sidebar navigation ───────────────────────────────────────────────
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
st.sidebar.page_link("pages/7_Terms_of_Service.py", label="📜 Terms of Service")
st.sidebar.page_link("app.py", label="🔎 Search")

# ── Financial Disclaimer ─────────────────────────────────────────────
st.title("📜 Terms of Service & Financial Disclaimer")

st.markdown("---")

st.markdown(
    '<div style="'
    "background:linear-gradient(135deg,#1e293b 0%,#0f172a 100%);"
    "border:1px solid #334155;border-left:4px solid #f59e0b;"
    "border-radius:12px;padding:2rem 2.5rem;margin-bottom:2rem;"
    'font-size:1.4rem;line-height:1.8;color:#e2e8f0;">'
    '<h2 style="color:#f59e0b;font-size:2rem;margin-top:0;">'
    "⚠️ DISCLAIMER — NOT FINANCIAL ADVICE</h2>"
    "<p>The information provided by this market sentiment aggregator, including but not limited to "
    '<b>"Market Mood,"</b> and <b>"Recommendations,"</b> is for '
    "<b>informational and educational purposes only.</b></p>"
    "<p><b>No Advice:</b> This tool does not constitute investment, legal, or tax advice. "
    "We are not a registered broker-dealer or investment advisor.</p>"
    "<p><b>Risk of Loss:</b> Trading stocks and cryptocurrencies involves significant risk. "
    "You should never invest more than you are willing to lose.</p>"
    "<p><b>Accuracy:</b> While we strive for data accuracy, our AI models and sentiment analysis "
    "are based on third-party news and market data which may be delayed or incorrect.</p>"
    "<p><b>DIY Research:</b> Users are solely responsible for their own investment decisions. "
    "We strongly recommend consulting with a qualified professional before making any financial commitments.</p>"
    '<p style="font-weight:700;color:#f59e0b;font-size:1.5rem;margin-bottom:0;">'
    "PAST PERFORMANCE IS NOT INDICATIVE OF FUTURE RESULTS.</p>"
    "</div>",
    unsafe_allow_html=True,
)

# ── Terms of Service ─────────────────────────────────────────────────
st.markdown("## 📋 Terms of Service")

st.markdown(
    '<div style="'
    "background:#0f172a;border:1px solid #334155;border-left:4px solid #60a5fa;"
    "border-radius:12px;padding:2rem 2.5rem;margin-bottom:2rem;"
    'font-size:1.35rem;line-height:1.8;color:#e2e8f0;">'
    '<h3 style="color:#60a5fa;font-size:1.5rem;">1. Acceptance of Terms</h3>'
    "<p>By accessing this website, you agree to be bound by these Terms of Service and all applicable "
    "laws and regulations. If you do not agree with any of these terms, you are prohibited from using "
    "or accessing this site.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">2. Use License</h3>'
    "<p>Permission is granted to use this market sentiment aggregator for <b>personal, non-commercial "
    "transitory viewing only.</b> You may not:</p>"
    "<ul>"
    "<li>Modify or copy the materials;</li>"
    "<li>Use the materials for any commercial purpose or public display;</li>"
    "<li>Attempt to decompile or reverse engineer any software contained on the website.</li>"
    "</ul>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">3. Limitation of Liability</h3>'
    "<p>In no event shall the creators of this market sentiment aggregator or its partners be liable for any damages "
    "(including, without limitation, damages for loss of data or profit, or due to business "
    "interruption) arising out of the use or inability to use the materials on this website.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">4. Affiliate Disclosure</h3>'
    "<p>This website may contain affiliate links. If you click on an affiliate link and make a "
    "purchase or sign up for a service, we may receive a commission at no additional cost to you. "
    "This helps support the development of our free market tools.</p>"
    "<p>Exchange listings (Coinbase, Binance, Kraken, KuCoin, Gemini) shown in our screening tools "
    "are provided for informational purposes. Some links may be affiliate links.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">5. Data Sources</h3>'
    "<p>Market data is sourced from Alpha Vantage and other third-party providers. "
    "News headline sentiment is computed using TextBlob natural language processing. "
    "Data may be delayed, incomplete, or inaccurate. We make no guarantees about data freshness "
    "or accuracy.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">6. Changes to Terms</h3>'
    "<p>We reserve the right to revise these terms at any time without notice. By continuing to "
    "use this website, you agree to be bound by the current version of these Terms of Service.</p>"
    '<h3 style="color:#60a5fa;font-size:1.5rem;">7. Privacy Policy</h3>'
    "<p>"
    "We do not sell your personal information to third parties or share it for cross-contextual behavioral advertising. "
    "Our data collection is limited to strictly necessary information required to document your acceptance of our Terms of Use "
    "and to maintain the security of our services."
    "</p>"
    "<p><b>Information collected (stored in the <code>legal_consents</code> SQL table):</b></p>"
    "<ul>"
    "<li><code>id</code></li>"
    "<li><code>timestamp_utc</code></li>"
    "<li><code>timestamp_local</code></li>"
    "<li><code>timezone_name</code></li>"
    "<li><code>timezone_offset</code></li>"
    "<li><code>ip_address</code></li>"
    "<li><code>user_agent</code></li>"
    "<li><code>tos_version</code></li>"
    "<li><code>fingerprint_hash</code></li>"
    "<li><code>consent_action</code></li>"
    "<li><code>is_vpn</code></li>"
    "<li><code>vpn_service_provider</code></li>"
    "<li><code>gpc_signal</code></li>"
    "<li><code>manual_opt_out</code></li>"
    "<li><code>opt_out_effective</code></li>"
    "<li><code>opt_out_source</code></li>"
    "<li><code>tracking_mode</code></li>"
    "</ul>"
    "<p><b>Retention:</b> These records are retained for <b>6 years</b> pursuant to applicable statute(s) of law.</p>"
    "</div>",
    unsafe_allow_html=True,
)

st.markdown(
    "<p style='text-align:center; color:#64748b; font-size:1.2rem;'>"
    "Last updated: February 2026</p>",
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
