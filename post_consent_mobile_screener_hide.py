"""Hide How it works, Sentiment, and Top Picks on phone/tablet after consent.

Desktop (min-width: 1367px) is unchanged from the last committed screener layout.
"""

from __future__ import annotations

import streamlit as st

_CSS = """
/* Marker only — never takes layout space on any viewport. */
[data-testid="stElementContainer"]:has(.scoop-top-picks-anchor),
[data-testid="element-container"]:has(.scoop-top-picks-anchor) {
    display: none !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
    overflow: hidden !important;
}

@media (max-width: 1366px) {
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-info,
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-sentiment,
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-divider {
        display: none !important;
    }
    html:not([data-scoop-screener-gated="1"]) [data-testid="stElementContainer"]:has(.scoop-top-picks-anchor) + [data-testid="stElementContainer"],
    html:not([data-scoop-screener-gated="1"]) [data-testid="element-container"]:has(.scoop-top-picks-anchor) + [data-testid="element-container"],
    html:not([data-scoop-screener-gated="1"]) [data-testid="stElementContainer"]:has(.scoop-top-picks-anchor) + [data-testid="stElementContainer"] + [data-testid="stElementContainer"],
    html:not([data-scoop-screener-gated="1"]) [data-testid="element-container"]:has(.scoop-top-picks-anchor) + [data-testid="element-container"] + [data-testid="element-container"] {
        display: none !important;
    }
}

/* Desktop: keep How it works, Sentiment, divider, and Top Picks as last commit. */
@media (min-width: 1367px) {
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-compact .scoop-landing-info,
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-compact .scoop-landing-sentiment,
    html:not([data-scoop-screener-gated="1"]) .scoop-landing-divider {
        display: block !important;
    }
}
"""


def inject_post_consent_mobile_screener_hide() -> None:
    st.html(
        f"<style id='scoop-post-consent-mobile-screener-hide'>{_CSS}</style>",
        unsafe_allow_javascript=True,
    )


def render_top_picks_heading(st_module) -> None:
    """Same Streamlit ### heading as last commit; hidden marker is for mobile CSS only."""
    st_module.markdown(
        '<div class="scoop-top-picks-anchor" hidden></div>',
        unsafe_allow_html=True,
    )
    st_module.markdown("### 🏆 Top Picks")
