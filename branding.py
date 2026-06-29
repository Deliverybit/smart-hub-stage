from __future__ import annotations

from pathlib import Path


def logo_path_str() -> str:
    """
    Return the app logo path as a string for Streamlit page_icon/sidebar usage.
    """

    root = Path(__file__).resolve().parent
    # Prefer a top-level logo if present, otherwise fall back to assets.
    preferred = root / "The Scoop 52 Logo.png"
    fallback = root / "assets" / "scoop52_logo.png"
    return str(preferred if preferred.exists() else fallback)


def render_environment_banner(st_module) -> None:
    """Show a banner when not running in production."""
    from app_config import get_app_env

    env = get_app_env()
    if env == "production":
        return
    label = env.upper()
    st_module.markdown(
        f'<div style="background:#f59e0b;color:#1e293b;text-align:center;'
        f'padding:0.45rem 0.75rem;font-weight:600;border-radius:6px;'
        f'margin-bottom:0.75rem;">⚠️ {label} ENVIRONMENT — not production</div>',
        unsafe_allow_html=True,
    )

