#!/usr/bin/env python3
"""Inject desktop-only (1367px+) always-visible sidebar CSS into all pages."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import DESKTOP_SIDEBAR  # noqa: E402

MARKER = '@media (min-width: 1367px) {\n        [data-testid="stSidebar"] #scoop-title'
INJECTED = "Desktop: sidebar always visible"


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if INJECTED in text:
        print(f"skip {path.name} (already patched)")
        return
    idx = text.rfind(MARKER)
    if idx == -1:
        raise SystemExit(f"Desktop scoop-title block not found in {path.name}")
    insert_at = idx + len("@media (min-width: 1367px) {\n")
    text = text[:insert_at] + DESKTOP_SIDEBAR + text[insert_at:]
    path.write_text(text, encoding="utf-8")


def main() -> int:
    patch_file(ROOT / "app.py")
    print("patched app.py")
    patch_file(ROOT / "pages" / "7_Terms_of_Service.py")
    print("patched 7_Terms_of_Service.py")
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path)
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
