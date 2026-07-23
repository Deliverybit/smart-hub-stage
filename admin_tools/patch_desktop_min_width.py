#!/usr/bin/env python3
"""Limit desktop tooltip/headlines CSS to 1367px+ so tablet uses mobile card layout."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD = "@media (min-width: 769px) {"
NEW = "@media (min-width: 1367px) {"


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        text = path.read_text(encoding="utf-8")
        if OLD not in text:
            raise SystemExit(f"Expected desktop media query not found in {path.name}")
        updated = text.replace(OLD, NEW)
        if updated.count(NEW) < 2:
            raise SystemExit(f"Expected at least 2 replacements in {path.name}")
        path.write_text(updated, encoding="utf-8")
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
