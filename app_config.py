import os
from pathlib import Path
import tomllib


def get_alpha_vantage_api_key(required: bool = False) -> str | None:
    """Load the Alpha Vantage API key from deployment secrets or local env."""
    key = os.getenv("ALPHA_VANTAGE_API_KEY")
    if not key:
        try:
            import streamlit as st

            key = st.secrets.get("ALPHA_VANTAGE_API_KEY")
        except Exception:
            key = None
    if not key:
        key = _load_local_streamlit_secret("ALPHA_VANTAGE_API_KEY")

    if key == "replace-with-your-alpha-vantage-key":
        key = None

    if required and not key:
        raise RuntimeError("ALPHA_VANTAGE_API_KEY is not configured")

    return key


def _load_local_streamlit_secret(name: str):
    """Read ignored local Streamlit secrets when not running inside Streamlit."""
    secrets_path = Path(__file__).resolve().parent / ".streamlit" / "secrets.toml"
    try:
        with secrets_path.open("rb") as secrets_file:
            return tomllib.load(secrets_file).get(name)
    except (OSError, tomllib.TOMLDecodeError):
        return None


def get_screener_symbol_limit(default: int = 1000) -> int:
    """Limit Alpha Vantage screener calls; high default scans each full page universe."""
    raw_limit = os.getenv("SCREENER_SYMBOL_LIMIT")
    if not raw_limit:
        try:
            import streamlit as st

            raw_limit = st.secrets.get("SCREENER_SYMBOL_LIMIT")
        except Exception:
            raw_limit = None
    if not raw_limit:
        raw_limit = _load_local_streamlit_secret("SCREENER_SYMBOL_LIMIT")

    try:
        limit = int(raw_limit) if raw_limit is not None else default
    except (TypeError, ValueError):
        limit = default

    return max(1, limit)


# Bump when screener/API behavior changes to invalidate stale Streamlit caches.
SCREENER_CACHE_VERSION = 4

# Back-compat aliases used by some page variants.
ALPHAVANTAGE_CACHE_TIMEOUT = 900


def get_selected_symbol_list(symbols, limit: int | None = None):
    """Return up to ``limit`` symbols from a screener universe."""
    max_symbols = limit if limit is not None else get_screener_symbol_limit()
    return list(symbols)[:max_symbols]
