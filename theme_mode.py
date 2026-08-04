"""Dark mode toggle and color-only theme support across all viewports."""

from __future__ import annotations

import json

import streamlit as st

from admin_tools.dark_mode_css import DARK_MODE_CSS

SESSION_KEY = "scoop_dark_mode"
TOGGLE_KEY = "scoop_dark_mode_toggle"
STORAGE_KEY = "scoop-theme"
HYDRATED_KEY = "_scoop_theme_hydrated"


def is_dark_mode() -> bool:
    """Read toggle widget state first (same rerun), then session/localStorage hydrate."""
    if TOGGLE_KEY in st.session_state:
        return bool(st.session_state[TOGGLE_KEY])
    return bool(st.session_state.get(SESSION_KEY, False))


def _hydrate_from_storage() -> None:
    if st.session_state.get(HYDRATED_KEY):
        return
    try:
        from streamlit_js_eval import streamlit_js_eval
    except ImportError:
        st.session_state[HYDRATED_KEY] = True
        return
    stored = streamlit_js_eval(
        js_expressions=f"localStorage.getItem('{STORAGE_KEY}')",
        key="scoop_theme_hydrate",
        want_output=True,
        height=0,
    )
    if stored == "dark":
        st.session_state[SESSION_KEY] = True
        st.session_state[TOGGLE_KEY] = True
    elif stored == "light":
        st.session_state[SESSION_KEY] = False
        st.session_state[TOGGLE_KEY] = False
    st.session_state[HYDRATED_KEY] = True


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


def install_theme_support() -> None:
    """Hydrate saved preference early; CSS is injected last via inject_dark_mode_styles()."""
    if SESSION_KEY not in st.session_state:
        st.session_state[SESSION_KEY] = False
    _hydrate_from_storage()


def render_dark_mode_toggle() -> None:
    """Sidebar toggle; persists across pages via session state + localStorage."""
    _hydrate_from_storage()
    dark = st.sidebar.toggle(
        "Dark mode",
        value=is_dark_mode(),
        key=TOGGLE_KEY,
        help="Switch light/dark colors on desktop, tablet, and phone.",
    )
    st.session_state[SESSION_KEY] = dark
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
