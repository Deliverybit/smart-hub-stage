"""Dark mode toggle and color-only theme support across all viewports."""

from __future__ import annotations

import json

import streamlit as st

from admin_tools.dark_mode_css import DARK_MODE_CSS

SESSION_KEY = "scoop_dark_mode"
TOGGLE_KEY = "scoop_dark_mode_toggle"
STORAGE_KEY = "scoop-theme"
SYNC_PENDING_KEY = "_scoop_theme_sync_pending"
SYNC_DONE_KEY = "_scoop_theme_sync_done"
THEME_PAGE_KEY = "_scoop_theme_page_id"


def is_dark_mode() -> bool:
    """Read toggle widget state first (same rerun), then session fallback."""
    if TOGGLE_KEY in st.session_state:
        return bool(st.session_state[TOGGLE_KEY])
    return bool(st.session_state.get(SESSION_KEY, False))


def _theme_known_in_session() -> bool:
    return TOGGLE_KEY in st.session_state or SESSION_KEY in st.session_state


def _set_theme_session(dark: bool, *, touch_toggle_key: bool = False) -> None:
    st.session_state[SESSION_KEY] = dark
    if touch_toggle_key:
        st.session_state[TOGGLE_KEY] = dark


def _calling_page_id() -> str:
    """Identify the active Streamlit page script (changes on sidebar navigation)."""
    import inspect

    for frame in inspect.stack():
        path = frame.filename.replace("\\", "/")
        if "/pages/" in path or path.endswith("/app.py"):
            return path
    return "unknown"


def _reset_theme_for_page_change() -> None:
    """Drop stale widget/session theme when navigating to another page."""
    page = _calling_page_id()
    if st.session_state.get(THEME_PAGE_KEY) == page:
        return
    st.session_state[THEME_PAGE_KEY] = page
    for key in (SESSION_KEY, TOGGLE_KEY, SYNC_PENDING_KEY, SYNC_DONE_KEY):
        st.session_state.pop(key, None)


def _sync_theme_from_storage() -> bool:
    """Load theme from localStorage into session state. False = js_eval not ready yet."""
    if st.session_state.get(SYNC_DONE_KEY) and _theme_known_in_session():
        return True

    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        st.session_state[SYNC_DONE_KEY] = True
        return True

    if not st.session_state.get(SYNC_PENDING_KEY):
        st.session_state[SYNC_PENDING_KEY] = True

    stored = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('{STORAGE_KEY}') || ''",
        key="scoop_theme_sync",
        want_output=True,
        height=0,
    )
    if stored is None:
        return False

    _set_theme_session(str(stored).strip().lower() == "dark", touch_toggle_key=True)
    if not st.session_state.get(SYNC_DONE_KEY):
        st.session_state[SYNC_DONE_KEY] = True
        st.rerun()
    return True


def _session_dark_css() -> str:
    """Dark overrides keyed off html — injected last so they beat page CSS."""
    if not is_dark_mode():
        return ""
    return DARK_MODE_CSS.replace('html[data-scoop-theme="dark"]', "html")


def _persist_theme_script(theme: str) -> None:
    payload = json.dumps(theme)
    storage = json.dumps(STORAGE_KEY)
    st.html(
        f"""
<script>
(function() {{
    const theme = {payload};
    const doc = window.parent && window.parent.document ? window.parent.document : document;
    const root = doc.documentElement;
    root.setAttribute("data-scoop-theme", theme);
    root.classList.toggle("scoop-dark", theme === "dark");
    try {{ localStorage.setItem({storage}, theme); }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def inject_dark_mode_styles() -> None:
    """Apply dark palette last in the document (after inline page <style> blocks)."""
    css = _session_dark_css()
    css_json = json.dumps(css)
    st.html(
        f"""
<script>
(function() {{
    const css = {css_json};
    const id = "scoop-dark-mode-css";
    function apply(doc) {{
        if (!doc || !doc.documentElement) return;
        let el = doc.getElementById(id);
        if (!css) {{
            if (el) el.remove();
            return;
        }}
        if (!el) {{
            el = doc.createElement("style");
            el.id = id;
        }}
        el.textContent = css;
        const root = doc.body || doc.documentElement;
        root.appendChild(el);
    }}
    const parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    apply(parentDoc || document);
    if (parentDoc && parentDoc !== document) apply(document);
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def _early_theme_bootstrap_script() -> None:
    """Apply localStorage theme to <html> before first paint on every page load."""
    storage = json.dumps(STORAGE_KEY)
    st.html(
        f"""
<script>
(function() {{
    const doc = window.parent && window.parent.document ? window.parent.document : document;
    const root = doc.documentElement;
    let theme = "light";
    try {{
        const stored = localStorage.getItem({storage});
        if (stored === "dark" || stored === "light") {{
            theme = stored;
        }} else if (root.classList.contains("scoop-dark")) {{
            theme = "dark";
        }} else if (root.getAttribute("data-scoop-theme") === "dark") {{
            theme = "dark";
        }}
    }} catch (e) {{}}
    root.setAttribute("data-scoop-theme", theme);
    root.classList.toggle("scoop-dark", theme === "dark");
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def apply_theme_from_query_param() -> None:
    """Honor ?theme=dark|light once when landing from Analyze links, then drop it."""
    if "theme" not in st.query_params:
        return
    raw = st.query_params.get("theme", "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    theme = str(raw).strip().lower()
    if theme == "dark":
        _set_theme_session(True, touch_toggle_key=TOGGLE_KEY not in st.session_state)
        st.session_state[SYNC_DONE_KEY] = True
    elif theme == "light":
        _set_theme_session(False, touch_toggle_key=TOGGLE_KEY not in st.session_state)
        st.session_state[SYNC_DONE_KEY] = True
    try:
        del st.query_params["theme"]
    except Exception:
        pass


def apply_theme_early() -> None:
    """Inject theme CSS/scripts before main page content renders."""
    _reset_theme_for_page_change()
    apply_theme_from_query_param()
    if not _theme_known_in_session() and not _sync_theme_from_storage():
        return
    dark = is_dark_mode()
    st.session_state[SESSION_KEY] = dark
    if TOGGLE_KEY not in st.session_state:
        st.session_state[TOGGLE_KEY] = dark
    if _theme_known_in_session():
        theme = "dark" if dark else "light"
        _persist_theme_script(theme)
    inject_dark_mode_styles()


def install_theme_support() -> None:
    """Hydrate saved preference early; CSS is injected last via inject_dark_mode_styles()."""
    _early_theme_bootstrap_script()
    apply_theme_early()
    from tooltip_scroll import install_responsive_layout_bootstrap

    install_responsive_layout_bootstrap()


def render_dark_mode_toggle() -> None:
    """Sidebar toggle; persists across pages via session state + localStorage."""
    if not _theme_known_in_session():
        return

    if TOGGLE_KEY not in st.session_state:
        st.session_state[TOGGLE_KEY] = bool(st.session_state.get(SESSION_KEY, False))

    st.sidebar.toggle(
        "Dark mode",
        key=TOGGLE_KEY,
        help="Switch light/dark colors on desktop, tablet, and phone.",
    )
    dark = bool(st.session_state[TOGGLE_KEY])
    st.session_state[SESSION_KEY] = dark
    st.session_state[SYNC_DONE_KEY] = True
    theme = "dark" if dark else "light"
    _persist_theme_script(theme)
    inject_dark_mode_styles()


def chart_axis_colors() -> tuple[dict, dict]:
    """Plotly tick/title font colors for current theme."""
    color = "#e2e8f0" if is_dark_mode() else "#111827"
    tick = dict(color=color)
    title = dict(color=color)
    return tick, title


def chart_hoverlabel() -> dict:
    if is_dark_mode():
        return dict(
            bgcolor="#1e293b",
            bordercolor="#475569",
            font=dict(color="#f1f5f9", size=26),
            align="left",
            namelength=-1,
        )
    return dict(
        bgcolor="#ffffff",
        bordercolor="#cbd5e1",
        font=dict(color="#111827", size=26),
        align="left",
        namelength=-1,
    )


def chart_paper_bgcolor() -> str:
    return "#111827" if is_dark_mode() else "#ffffff"


def chart_plot_bgcolor() -> str:
    return "#0b1220" if is_dark_mode() else "#ffffff"


def chart_template() -> str:
    return "plotly_dark" if is_dark_mode() else "plotly_white"
