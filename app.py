"""
The Scoop 52 — home entry point.

Search is archived (see archived/search_page.py and pages/_Analyze.py).
Routes ?ticker= links to Analyze; mobile/tablet first visits open Landing; otherwise NYSE Top 10.
"""

import streamlit as st

from analyze_page import stash_analyze_ticker
from branding import logo_path_str, render_environment_banner
from landing_page import install_landing_entry_redirect, route_home_entry
from theme_mode import install_theme_support

st.set_page_config(
    page_title="The Scoop 52",
    page_icon=logo_path_str(),
    layout="wide",
)
render_environment_banner(st)
install_theme_support()
install_landing_entry_redirect()

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

route_home_entry()
