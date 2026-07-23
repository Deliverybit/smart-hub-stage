#!/usr/bin/env python3
"""Widen mobile slide-out sidebar so nav labels are not clipped."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_SIDEBAR = '        [data-testid="stSidebar"] { min-width: 280px !important; }'
NEW_SIDEBAR = """        [data-testid="stSidebar"] {
            min-width: 360px !important;
            width: min(92vw, 360px) !important;
            max-width: 360px !important;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            width: 100% !important;
        }"""

OLD_LINKS = """        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.25rem, 4.6vw, 1.55rem) !important;
            line-height: 1.25 !important;
        }"""

NEW_LINKS = """        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.15rem, 4.2vw, 1.45rem) !important;
            line-height: 1.25 !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }"""


def main() -> int:
    files = [ROOT / "app.py", *sorted((ROOT / "pages").glob("*.py"))]
    for path in files:
        text = path.read_text(encoding="utf-8")
        if OLD_SIDEBAR not in text:
            print(f"skip sidebar: {path.name}")
            continue
        text = text.replace(OLD_SIDEBAR, NEW_SIDEBAR)
        if OLD_LINKS in text:
            text = text.replace(OLD_LINKS, NEW_LINKS)
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
