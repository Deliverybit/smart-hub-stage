"""Home entry routing: desktop -> NYSE Top 10; mobile/tablet -> landing + tab nav."""

from __future__ import annotations

import re

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

HOME_NAV_MARKETS: tuple[tuple[str, str], ...] = (
    ("pages/1_NYSE_Top_10.py", "📊 NYSE 10"),
    ("pages/2_NASDAQ_Top_10.py", "💹 NASDAQ 10"),
    ("pages/3_Crypto_Top_10.py", "🪙 Crypto 10"),
    ("pages/5_CME_Top_10.py", "🌾 CME Commodities 10"),
    ("pages/6_ICE_Top_10.py", "🛢️ ICE Commodities 10"),
)

SCOOP_52_DESCRIPTION = (
    "Screen major markets for assets trading at or near their 52-week lows — "
    "with headline sentiment checks to filter out fraud and bankruptcy signals."
)

# Backward-compatible alias (legacy landing labels).
HOME_MARKET_CARDS = HOME_NAV_MARKETS + ((TERMS_PAGE, "📜 Terms of Service"),)


def _responsive_viewport_js() -> str:
    return (
        "(() => {"
        "  const w = (window.parent && window.parent.innerWidth) || window.innerWidth || 0;"
        f"  return w <= {RESPONSIVE_MAX_WIDTH} ? '1' : '0';"
        "})()"
    )


def _sanitize_widget_key(value: str) -> str:
    return re.sub(r"[^a-zA-Z0-9_]+", "_", value)


def _nav_viewport_key(page: str | None) -> str:
    return f"scoop_nav_viewport_{_sanitize_widget_key(page or 'app')}"


def _js_eval(expression: str, *, key: str) -> object | None:
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        return None
    try:
        from streamlit.errors import StreamlitAPIException
    except ImportError:
        StreamlitAPIException = Exception  # type: ignore[misc, assignment]
    try:
        return streamlit_js_eval(
            js_expressions=expression,
            key=key,
            want_output=True,
            height=0,
        )
    except StreamlitAPIException:
        return None


def probe_responsive_viewport(*, key: str = "scoop_nav_viewport") -> bool | None:
    """True when layout width is mobile/tablet (<=1366px). None = JS not ready."""
    cache_key = f"_scoop_viewport_cache_{key}"
    if cache_key in st.session_state:
        return st.session_state[cache_key]

    try:
        from streamlit.runtime.scriptrunner import get_script_run_ctx

        ctx = get_script_run_ctx()
    except Exception:
        ctx = None
    if ctx is not None:
        started = getattr(ctx, "_scoop_viewport_keys", None)
        if started is None:
            started = set()
            setattr(ctx, "_scoop_viewport_keys", started)
        if key in started:
            cached = st.session_state.get(cache_key)
            return cached if isinstance(cached, bool) else None
        started.add(key)

    value = _js_eval(_responsive_viewport_js(), key=key)
    if value is None:
        return None
    result = str(value).strip() == "1"
    st.session_state[cache_key] = result
    return result


def is_mobile_tablet_viewport(*, page: str | None = None) -> bool:
    """True for mobile/tablet; defaults mobile-safe while the viewport probe is loading."""
    responsive = probe_responsive_viewport(key=_nav_viewport_key(page))
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

    st.html(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_javascript=True,
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
    for path, label in HOME_NAV_MARKETS:
        st.sidebar.page_link(path, label=label)
    st.sidebar.markdown("---")
    st.sidebar.page_link(TERMS_PAGE, label="📜 Terms of Service")


def render_mobile_back_home_bar(*, current_page: str | None) -> None:
    """Fixed top-left back link on inner pages; CSS hides on desktop (1367px+)."""
    if not current_page or current_page == HOME_PAGE:
        return
    import importlib
    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    MOBILE_BACK_HOME_BAR = _tml.MOBILE_BACK_HOME_BAR

    st.markdown(
        f'<style id="scoop-mobile-back-home-css">{MOBILE_BACK_HOME_BAR}</style>',
        unsafe_allow_html=True,
    )
    st.markdown(
        (
            '<div class="scoop-mobile-back-home-bar">'
            '<a class="scoop-mobile-back-home" href="/" target="_self">← Back to Home</a>'
            '<label class="scoop-mobile-fixed-dark" title="Switch light/dark colors.">'
            '<input type="checkbox" id="scoop-mobile-dark-cb" class="scoop-mobile-fixed-dark-cb" />'
            '<span class="scoop-mobile-fixed-dark-switch" aria-hidden="true"></span>'
            '<span class="scoop-mobile-fixed-dark-label">Dark mode</span>'
            "</label>"
            "</div>"
            '<div class="scoop-mobile-back-home-spacer" aria-hidden="true"></div>'
        ),
        unsafe_allow_html=True,
    )
    st.html(
        """
<script>
(function() {
    const STORAGE = "scoop-theme";
    const win = (window.parent && window.parent !== window) ? window.parent : window;
    function roots() {
        const out = [document.documentElement];
        try {
            if (win.document && win.document.documentElement) {
                out.push(win.document.documentElement);
            }
        } catch (e) {}
        return out;
    }
    function readDark() {
        try {
            return (win.sessionStorage || sessionStorage).getItem(STORAGE) === "dark";
        } catch (e) {
            return false;
        }
    }
    function apply(dark) {
        roots().forEach(function(root) {
            root.setAttribute("data-scoop-theme", dark ? "dark" : "light");
            root.classList.toggle("scoop-dark", dark);
        });
        try {
            const store = win.sessionStorage || sessionStorage;
            if (dark) store.setItem(STORAGE, "dark");
            else store.removeItem(STORAGE);
            (win.localStorage || localStorage).removeItem(STORAGE);
        } catch (e) {}
    }
    const cb = document.getElementById("scoop-mobile-dark-cb");
    if (!cb) return;
    cb.checked = readDark();
    apply(cb.checked);
    cb.addEventListener("change", function() {
        apply(cb.checked);
    });
})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def render_mobile_inner_top_bar(
    *,
    current_page: str | None,
) -> None:
    """Mobile/tablet inner pages: tab-nav CSS (dark mode lives in the fixed back bar)."""
    if not current_page or current_page == HOME_PAGE:
        return
    import importlib
    import admin_tools.tablet_mobile_layout_css as _tml

    importlib.reload(_tml)
    from theme_mode import inject_dark_mode_styles

    install_responsive_tab_nav()
    inject_dark_mode_styles()
    st.html(
        '<script>document.documentElement.removeAttribute("data-scoop-home-page");</script>',
        unsafe_allow_javascript=True,
    )

    st.html(
        f'<style id="scoop-mobile-inner-top-css">{_tml.MOBILE_INNER_TOP_BAR}</style>'
        f'<style id="scoop-dark-mode-unbox-css">{_tml._MOBILE_TABLET_DARK_MODE_UNBOX_ALWAYS}</style>',
        unsafe_allow_javascript=True,
    )


def render_mobile_back_home_link(*, current_page: str | None) -> None:
    """Backward-compatible alias — use render_mobile_back_home_bar."""
    render_mobile_back_home_bar(current_page=current_page)


def prepare_mobile_home_landing() -> None:
    """Mark the landing page and enable tab-nav CSS before first paint."""
    from admin_tools.tablet_mobile_layout_css import RESPONSIVE_TAB_NAV_BOOTSTRAP

    st.html(
        f'<style id="scoop-responsive-tab-nav-css">{RESPONSIVE_TAB_NAV_BOOTSTRAP}</style>',
        unsafe_allow_javascript=True,
    )
    st.html(
        '<script>'
        'document.documentElement.setAttribute("data-scoop-tab-nav","1");'
        'document.documentElement.setAttribute("data-scoop-home-page","1");'
        '</script>',
        unsafe_allow_javascript=True,
    )


def render_mobile_tablet_home() -> None:
    """Mobile/tablet home: sidebar-style landing (logo, title, dark mode, description, nav)."""
    from branding import logo_path_str
    from theme_mode import inject_dark_mode_styles, render_dark_mode_toggle_main

    inject_dark_mode_styles()

    st.markdown('<div class="scoop-mobile-home-shell-marker" aria-hidden="true"></div>', unsafe_allow_html=True)
    st.image(logo_path_str(), use_container_width=True)
    st.markdown(
        """
        <div class="sidebar-brand">
          <div class="sidebar-brand-row">
            <span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">The Scoop 52</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('<div class="scoop-mobile-inner-top">', unsafe_allow_html=True)
    st.markdown('<div class="scoop-mobile-inner-top-toggle">', unsafe_allow_html=True)
    render_dark_mode_toggle_main(label="Dark mode")
    st.markdown("</div></div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown(
        f'<div class="scoop-home-landing"><p>{SCOOP_52_DESCRIPTION}</p></div>',
        unsafe_allow_html=True,
    )
    for path, label in HOME_NAV_MARKETS:
        st.page_link(path, label=label, use_container_width=True)
    st.markdown("---")
    st.page_link(TERMS_PAGE, label="📜 Terms of Service", use_container_width=True)


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
        render_dark_mode_toggle_main(label="Dark mode")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="scoop-mobile-tab-row">', unsafe_allow_html=True)
    tab_cols = st.columns(len(APP_NAV_PAGES), gap="small")
    for col, (path, label) in zip(tab_cols, APP_NAV_PAGES):
        with col:
            st.page_link(path, label=label, use_container_width=False)
    st.markdown("</div></div>", unsafe_allow_html=True)


def render_responsive_navigation(*, current_page: str | None = None) -> None:
    """Render desktop sidebar or mobile/tablet chrome — never both."""
    render_mobile_back_home_bar(current_page=current_page)
    render_mobile_inner_top_bar(current_page=current_page)
    if is_mobile_tablet_viewport(page=current_page):
        return
    render_desktop_sidebar_nav()
