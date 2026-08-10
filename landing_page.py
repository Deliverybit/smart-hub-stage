"""Mobile/tablet first-visit landing page routing."""

from __future__ import annotations

import json

import streamlit as st

LANDING_SEEN_KEY = "scoop-landing-seen"
LANDING_PAGE = "pages/0_Landing.py"
DEFAULT_SCREENER_PAGE = "pages/1_NYSE_Top_10.py"
RESPONSIVE_MAX_WIDTH = 1366
ROUTED_KEY = "_scoop_landing_routed"


def _responsive_viewport_js() -> str:
    return (
        "(() => {"
        "  const w = (window.parent && window.parent.innerWidth) || window.innerWidth || 0;"
        f"  return w <= {RESPONSIVE_MAX_WIDTH} ? '1' : '0';"
        "})()"
    )


def _landing_seen_js() -> str:
    key = json.dumps(LANDING_SEEN_KEY)
    return (
        f"(() => {{ try {{ return sessionStorage.getItem({key}) || ''; }} catch (e) {{ return ''; }} }})()"
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
    value = _js_eval(_responsive_viewport_js(), key="scoop_landing_viewport")
    if value is None:
        return None
    return str(value).strip() == "1"


def probe_landing_seen() -> bool | None:
    """True when the landing page was already shown this browser session."""
    value = _js_eval(_landing_seen_js(), key="scoop_landing_seen")
    if value is None:
        return None
    return bool(str(value).strip())


def should_redirect_to_landing() -> bool | None:
    """
    True = first mobile/tablet visit should open the landing page.
    False = go straight to the default screener.
    None = wait for client viewport / sessionStorage probe.
    """
    responsive = probe_responsive_viewport()
    if responsive is None:
        return None
    if not responsive:
        return False
    seen = probe_landing_seen()
    if seen is None:
        return None
    return not seen


def install_landing_entry_redirect() -> None:
    """Early client redirect from `/` to Landing on first mobile/tablet visit."""
    key = json.dumps(LANDING_SEEN_KEY)
    st.html(
        f"""
<script>
(function () {{
    try {{
        const path = (location.pathname || "").replace(/\\/$/, "");
        if (path !== "" && path !== "/") {{
            return;
        }}
        const w = window.innerWidth || 0;
        if (w > {RESPONSIVE_MAX_WIDTH}) {{
            return;
        }}
        if (sessionStorage.getItem({key})) {{
            return;
        }}
        window.location.replace("/Landing");
    }} catch (e) {{}}
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def inject_landing_seen_on_nav() -> None:
    """Mark landing as seen when the user navigates away from the landing page."""
    key = json.dumps(LANDING_SEEN_KEY)
    st.html(
        f"""
<script>
(function () {{
    const key = {key};
    const mark = () => {{
        try {{
            sessionStorage.setItem(key, "1");
        }} catch (e) {{}}
    }};
    document.addEventListener(
        "click",
        (event) => {{
            if (event.target.closest("a[href], button")) {{
                mark();
            }}
        }},
        true
    );
}})();
</script>
""",
        unsafe_allow_javascript=True,
    )


def redirect_if_desktop_on_landing() -> None:
    """Landing page is mobile/tablet only — desktop users go to NYSE Top 10."""
    responsive = probe_responsive_viewport()
    if responsive is None:
        st.stop()
    if responsive:
        return
    st.switch_page(DEFAULT_SCREENER_PAGE)


def route_home_entry() -> None:
    """Route `/` to Landing (mobile/tablet first visit) or NYSE Top 10."""
    if st.session_state.get(ROUTED_KEY):
        st.switch_page(DEFAULT_SCREENER_PAGE)

    decision = should_redirect_to_landing()
    if decision is None:
        st.stop()

    st.session_state[ROUTED_KEY] = True
    if decision:
        st.switch_page(LANDING_PAGE)
    else:
        st.switch_page(DEFAULT_SCREENER_PAGE)
