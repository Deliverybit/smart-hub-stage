"""Home entry routing: desktop -> NYSE Top 10; mobile/tablet -> landing + tab nav."""

from __future__ import annotations

import streamlit as st

DEFAULT_SCREENER_PAGE = "pages/1_NYSE_Top_10.py"
TERMS_PAGE = "pages/7_Terms_of_Service.py"
HOME_PAGE = "app.py"
RESPONSIVE_MAX_WIDTH = 1366

# Mobile/tablet top tabs: home + one tab per market (Terms linked from gating copy).
APP_NAV_PAGES: tuple[tuple[str, str], ...] = (
    (HOME_PAGE, "🏠 Home"),
    ("pages/1_NYSE_Top_10.py", "📊 NYSE"),
    ("pages/2_NASDAQ_Top_10.py", "💹 NASDAQ"),
    ("pages/3_Crypto_Top_10.py", "🪙 Crypto"),
    ("pages/5_CME_Top_10.py", "🌾 CME"),
    ("pages/6_ICE_Top_10.py", "🛢️ ICE"),
)

HOME_MARKET_CARDS: tuple[tuple[str, str], ...] = (
    ("pages/1_NYSE_Top_10.py", "📊 NYSE Top 10"),
    ("pages/2_NASDAQ_Top_10.py", "💹 NASDAQ Top 10"),
    ("pages/3_Crypto_Top_10.py", "🪙 Crypto Top 10"),
    ("pages/5_CME_Top_10.py", "🌾 CME Commodities"),
    ("pages/6_ICE_Top_10.py", "🛢️ ICE Commodities"),
    (TERMS_PAGE, "📜 Terms of Service"),
)


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


def probe_responsive_viewport(*, key: str = "scoop_nav_viewport") -> bool | None:
    """True when layout width is mobile/tablet (<=1366px). None = JS not ready."""
    cache_key = f"_scoop_viewport_cache_{key}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    value = _js_eval(_responsive_viewport_js(), key=key)
    if value is None:
        return None
    result = str(value).strip() == "1"
    st.session_state[cache_key] = result
    return result


def is_mobile_tablet_viewport() -> bool:
    """True for mobile/tablet; defaults mobile-safe while the viewport probe is loading."""
    responsive = probe_responsive_viewport()
    return responsive is not False


def resolve_home_entry() -> str | None:
    """Return 'desktop', 'mobile', or None while the viewport probe is loading."""
    responsive = probe_responsive_viewport(key="scoop_home_viewport")
    if responsive is None:
        return None
    return "mobile" if responsive else "desktop"


def install_responsive_tab_nav() -> None:
    """Enable mobile/tablet tab navigation (hides slide-out sidebar via CSS)."""
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP

    st.markdown(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_html=True,
    )
    st.html(
        '<script>document.documentElement.setAttribute("data-scoop-tab-nav","1");</script>',
        unsafe_allow_javascript=True,
    )


def render_desktop_sidebar_nav() -> None:
    """Desktop-only sidebar navigation."""
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
    st.sidebar.page_link(TERMS_PAGE, label="📜 Terms of Service")


def render_mobile_inner_top_bar(
    *,
    current_page: str | None,
) -> None:
    """Mobile/tablet inner pages: compact back link + dark mode (no extra header/tabs)."""
    if not current_page or current_page == HOME_PAGE:
        return
    from admin_tools.tablet_mobile_layout_css import MOBILE_INNER_TOP_BAR
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    install_responsive_tab_nav()
    inject_dark_mode_styles()
    st.html(
        '<script>document.documentElement.removeAttribute("data-scoop-home-page");</script>',
        unsafe_allow_javascript=True,
    )

    st.markdown(
        f'<style id="scoop-mobile-inner-top-css">{MOBILE_INNER_TOP_BAR}</style>',
        unsafe_allow_html=True,
    )
    st.markdown('<div class="scoop-mobile-inner-top">', unsafe_allow_html=True)
    bar = st.columns([5, 2], gap="small")
    with bar[0]:
        st.markdown(
            '<a class="scoop-mobile-back-home" href="/" target="_self">← Back to Home</a>',
            unsafe_allow_html=True,
        )
    with bar[1]:
        st.markdown('<div class="scoop-mobile-inner-top-toggle">', unsafe_allow_html=True)
        render_dark_mode_toggle_main()
        st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)


def render_mobile_back_home_link(*, current_page: str | None) -> None:
    """Backward-compatible alias — use render_mobile_inner_top_bar."""
    render_mobile_inner_top_bar(current_page=current_page)


def prepare_mobile_home_landing() -> None:
    """Mark the landing page and enable tab-nav CSS before first paint."""
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP

    st.markdown(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_html=True,
    )
    st.html(
        '<script>'
        'document.documentElement.setAttribute("data-scoop-tab-nav","1");'
        'document.documentElement.setAttribute("data-scoop-home-page","1");'
        '</script>',
        unsafe_allow_javascript=True,
    )


def render_mobile_home_shell() -> None:
    """Mobile/tablet landing header — logo + dark mode only (title is in welcome h1)."""
    from branding import logo_path_str
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    inject_dark_mode_styles()

    header = st.columns([2, 1], gap="small")
    with header[0]:
        st.image(logo_path_str(), width=96)
    with header[1]:
        st.markdown('<div class="scoop-mobile-home-toggle">', unsafe_allow_html=True)
        render_dark_mode_toggle_main()
        st.markdown("</div>", unsafe_allow_html=True)


def render_mobile_tab_nav_shell(*, current_page: str | None = None) -> None:
    """Mobile/tablet header + horizontal tab bar in the main content area."""
    from branding import logo_path_str
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    install_responsive_tab_nav()
    inject_dark_mode_styles()
    st.html(
        '<script>document.documentElement.removeAttribute("data-scoop-home-page");</script>',
        unsafe_allow_javascript=True,
    )

    st.markdown('<div class="scoop-mobile-nav-shell">', unsafe_allow_html=True)

    header = st.columns([1, 4, 2], gap="small")
    with header[0]:
        st.image(logo_path_str(), width=52)
    with header[1]:
        st.markdown(
            '<p class="scoop-mobile-nav-title">The Scoop 52</p>',
            unsafe_allow_html=True,
        )
    with header[2]:
        st.markdown('<div class="scoop-mobile-nav-toggle">', unsafe_allow_html=True)
        render_dark_mode_toggle_main()
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="scoop-mobile-tab-row">', unsafe_allow_html=True)
    tab_cols = st.columns(len(APP_NAV_PAGES), gap="small")
    for col, (path, label) in zip(tab_cols, APP_NAV_PAGES):
        with col:
            st.page_link(path, label=label, use_container_width=False)
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_responsive_navigation(*, current_page: str | None = None) -> None:
    """Render desktop sidebar or mobile/tablet compact top bar — never both."""
    if is_mobile_tablet_viewport():
        render_mobile_inner_top_bar(current_page=current_page)
        return
    render_desktop_sidebar_nav()


def render_mobile_tablet_home() -> None:
    """Mobile/tablet home: landing page with market buttons (no top tab row)."""
    render_mobile_home_shell()

    st.markdown(
        """
        <div class="scoop-home-landing">
          <h1>Welcome to The Scoop 52</h1>
          <p>
            Screen major markets for assets trading at or near their 52-week lows —
            with headline sentiment checks to filter out fraud and bankruptcy signals.
          </p>
          <p>Select a market below to review the disclaimer and open the Top 10 screener.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for path, label in HOME_MARKET_CARDS:
        st.page_link(path, label=label, use_container_width=True)
