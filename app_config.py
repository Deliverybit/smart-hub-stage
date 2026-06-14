import os


def get_alpha_vantage_api_key(required: bool = False) -> str | None:
    """Load the Alpha Vantage API key from deployment secrets or local env."""
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not key:
        try:
            import streamlit as st

            key = st.secrets.get("ALPHA_VANTAGE_API_KEY")
        except Exception:
            key = None

    if key == "replace-with-your-alpha-vantage-key":
        key = None

    if required and not key:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY is not configured")

    return key


def get_screener_symbol_limit(default: int = 4) -> int:
    """Limit Alpha Vantage screener calls so the free key can populate test data."""
    raw_limit = os.getenv("SCREENER_SYMBOL_LIMIT")
    if not raw_limit:
        try:
            import streamlit as st

            raw_limit = st.secrets.get("SCREENER_SYMBOL_LIMIT")
        except Exception:
            raw_limit = None

    try:
        limit = int(raw_limit) if raw_limit is not None else default
    except (TypeError, ValueError):
        limit = default

    return max(1, limit)
