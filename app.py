"""
The Scoop 52 — home entry point.

Routes ?ticker= links to Analyze; desktop opens NYSE Top 10; mobile/tablet opens landing + tabs.
"""

import streamlit as st

from analyze_page import stash_analyze_ticker
from branding import logo_path_str, render_environment_banner
from landing_page import DEFAULT_SCREENER_PAGE, prepare_mobile_home_landing, render_mobile_tablet_home, resolve_home_entry
from theme_mode import install_theme_support

st.set_page_config(
    page_title="The Scoop 52",
    page_icon=logo_path_str(),
    layout="wide",
)
install_theme_support()

if "analyze" in st.query_params:
    raw = st.query_params.get("analyze", "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    if str(raw).strip():
        stash_analyze_ticker(str(raw).strip())
        st.switch_page("pages/_Analyze.py")

if "ticker" in st.query_params:
    raw = st.query_params.get("ticker", "")
    if isinstance(raw, list):
        raw = raw[0] if raw else ""
    if str(raw).strip():
        stash_analyze_ticker(str(raw).strip())
        st.switch_page("pages/_Analyze.py")

entry = resolve_home_entry()
if entry is None:
    st.stop()
if entry == "desktop":
    st.switch_page(DEFAULT_SCREENER_PAGE)

prepare_mobile_home_landing()
render_environment_banner(st)
render_mobile_tablet_home()
