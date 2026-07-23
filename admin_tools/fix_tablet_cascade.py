#!/usr/bin/env python3
"""Fix CSS cascade so tablet rules are not overridden by desktop sidebar title rules."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

FILES = [
    ROOT / "app.py",
    ROOT / "pages" / "7_Terms_of_Service.py",
    *sorted((ROOT / "pages").glob("*_Top_10.py")),
]

INLINE_OLD = 'style="font-size:60px !important;line-height:1.05 !important;"'
INLINE_NEW = 'class="sidebar-brand-text" style="line-height:1.05 !important;"'

# Fix duplicate class if we run twice
INLINE_OLD2 = 'class="sidebar-brand-text" class="sidebar-brand-text"'

POST_TABLET_OLD = """
    [data-testid="stSidebar"] #scoop-title {
        font-size: 60px !important;
        line-height: 1.05 !important;
    }
"""

POST_TABLET_NEW = """
    @media (min-width: 1367px) {
        [data-testid="stSidebar"] #scoop-title {
            font-size: 60px !important;
            line-height: 1.05 !important;
        }
    }
"""

DESKTOP_OPEN = "    /* ===== DESKTOP / HIGH-RES ===== */"
DESKTOP_WRAP = (
    "    /* ===== DESKTOP / HIGH-RES (1367px+) ===== */\n"
    "    @media (min-width: 1367px) {"
)
MOBILE_MARKER = "    /* ===== MOBILE ===== */"
DESKTOP_CLOSE = "    }\n\n"
WRAP_DESKTOP_SECTION = False


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")

    text = text.replace(INLINE_OLD2, 'class="sidebar-brand-text"')
    if INLINE_OLD in text:
        text = text.replace(
            f'<span id="scoop-title" class="sidebar-brand-text" {INLINE_OLD.split("=")[0]}="font-size:60px !important;line-height:1.05 !important;"',
            '<span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">',
        )
    # simpler replace
    text = text.replace(
        '<span id="scoop-title" class="sidebar-brand-text" style="font-size:60px !important;line-height:1.05 !important;">',
        '<span id="scoop-title" class="sidebar-brand-text" style="line-height:1.05 !important;">',
    )

    if POST_TABLET_OLD in text:
        text = text.replace(POST_TABLET_OLD, POST_TABLET_NEW)
    elif POST_TABLET_NEW.strip() not in text:
        raise SystemExit(f"Post-tablet scoop-title block not found in {path.name}")

    if WRAP_DESKTOP_SECTION and DESKTOP_WRAP not in text and DESKTOP_OPEN in text and MOBILE_MARKER in text:
        text = text.replace(DESKTOP_OPEN, DESKTOP_WRAP, 1)
        text = text.replace(MOBILE_MARKER, DESKTOP_CLOSE + MOBILE_MARKER, 1)

    path.write_text(text, encoding="utf-8")


def main() -> int:
    for path in FILES:
        patch_file(path)
        print(f"fixed cascade in {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
