"""Home entry routing: desktop -> NYSE Top 10; mobile/tablet -> sidebar slide-out."""

from __future__ import annotations

import json

import streamlit as st

DEFAULT_SCREENER_PAGE = "pages/1_NYSE_Top_10.py"
RESPONSIVE_MAX_WIDTH = 1366
SIDEBAR_BOOTSTRAP_KEY = "scoop-responsive-sidebar-ready"


def _responsive_viewport_js() -> str:
    return (
        "(() => {"
        "  const w = (window.parent && window.parent.innerWidth) || window.innerWidth || 0;"
        f"  return w <= {RESPONSIVE_MAX_WIDTH} ? '1' : '0';"
        "})()"
    )


def _js_eval(expression: str, *, key: str) -> object | None:
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        return None
    return streamlit_js_eval(
        js_expressions=expression,
        key=key,
        want_output=True,
        height=0,
    )


def probe_responsive_viewport() -> bool | None:
    """True when layout width is mobile/tablet (<=1366px). None = JS not ready."""
    value = _js_eval(_responsive_viewport_js(), key="scoop_home_viewport")
    if value is None:
        return None
    return str(value).strip() == "1"


def resolve_home_entry() -> str | None:
    """
    Return 'desktop', 'mobile', or None while the viewport probe is loading.
    """
    responsive = probe_responsive_viewport()
    if responsive is None:
        return None
    return "mobile" if responsive else "desktop"


def render_app_sidebar() -> None:
    """Shared sidebar navigation used on the mobile/tablet home entry."""
    from branding import logo_path_str
    from theme_mode import render_dark_mode_toggle

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


def render_mobile_tablet_home() -> None:
    """Mobile/tablet home: slide-out sidebar navigation (no separate landing page)."""
    from theme_mode import inject_dark_mode_styles
    from tooltip_scroll import install_responsive_sidebar_handler

    st.markdown(
        """
        <style>
        [data-testid="stSidebarNav"] { display: none !important; }
        @media (max-width: 1366px) {
            [data-testid="stMainBlockContainer"] {
                min-height: 0 !important;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    render_app_sidebar()
    install_responsive_sidebar_handler()
    bootstrap_key = json.dumps(SIDEBAR_BOOTSTRAP_KEY)
    st.html(
        f"""
<script>
(function () {{
    const appWin = window.parent || window;
    try {{
        appWin.sessionStorage.removeItem({bootstrap_key});
    }} catch (e) {{}}
    const expand = () => appWin.__scoopLayout?.expandSidebar?.();
    expand();
    appWin.requestAnimationFrame(expand);
    [50, 150, 400, 900].forEach((delay) => appWin.setTimeout(expand, delay));
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )
    inject_dark_mode_styles()
