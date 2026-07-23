#!/usr/bin/env python3
"""Patch mobile (≤768px) headlines CSS to use card-overlay behavior like tablet."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "admin_tools"))

from tablet_mobile_layout_css import MOBILE_HEADLINES_CARD_OVERLAY  # noqa: E402

MOBILE_HEADLINES_RE = re.compile(
    r"/\* Headlines: tap count.*?\n"
    r"        \.stMarkdown \.tip-wrap\.headlines-tip:has\(\.hl-tip-cb:checked\) \.tip-text \.hl-tip-line a \{.*?\n"
    r"        \}",
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if not MOBILE_HEADLINES_RE.search(text):
        raise SystemExit(f"No mobile headlines block found in {path.name}")
    text = MOBILE_HEADLINES_RE.sub(MOBILE_HEADLINES_CARD_OVERLAY.strip(), text, count=1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path)
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
