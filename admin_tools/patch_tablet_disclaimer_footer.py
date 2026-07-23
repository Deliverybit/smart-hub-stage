#!/usr/bin/env python3
"""Tablet-only: flow disclaimer below content so consent checkbox stays visible."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

TABLET_FOOTER_CSS = """
    @media (min-width: 769px) and (max-width: 1366px) {
        .disclaimer-footer {
            position: static !important;
            left: 0 !important;
            width: 100% !important;
            margin-top: 1.25rem !important;
            padding: 0.5rem 0.75rem !important;
            font-size: clamp(0.76rem, 1.8vw, 0.92rem) !important;
            line-height: 1.35 !important;
        }
        .disclaimer-footer strong,
        .disclaimer-footer a {
            font-size: inherit !important;
        }
        .stMainBlockContainer,
        [data-testid="stMainBlockContainer"] {
            padding-bottom: 2.5rem !important;
        }
    }"""

ANCHOR = """        .stMainBlockContainer { padding-bottom: 2rem !important; }
    }
    </style>"""

REPLACEMENT = (
    """        .stMainBlockContainer { padding-bottom: 2rem !important; }
    }"""
    + TABLET_FOOTER_CSS
    + """
    </style>"""
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if TABLET_FOOTER_CSS.strip() in text:
        print(f"skip {path.name} (already patched)")
        return
    if ANCHOR not in text:
        raise SystemExit(f"Footer anchor not found in {path.name}")
    path.write_text(text.replace(ANCHOR, REPLACEMENT, 1), encoding="utf-8")
    print(f"patched {path.name}")


def main() -> int:
    files = [ROOT / "app.py", ROOT / "pages" / "7_Terms_of_Service.py"]
    files.extend(sorted((ROOT / "pages").glob("*_Top_10.py")))
    for path in files:
        patch_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
