#!/usr/bin/env python3
"""Fix desktop headlines popup: header always visible, panel clamped to viewport."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

OLD_TIP_TEXT = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: block !important;
            position: absolute !important;
            left: auto !important;
            right: 0 !important;
            top: auto !important;
            bottom: calc(100% + 10px) !important;
            transform: none !important;
            /* Popup sits just above the Headlines count in the row */
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-pop-w) !important;
            min-width: var(--hl-pop-w) !important;
            max-width: var(--hl-pop-w) !important;
            height: auto !important;
            min-height: 0 !important;
            max-height: var(--hl-pop-h) !important;
            overflow-x: hidden !important;
            overflow-y: scroll !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #111827 !important;
            -webkit-overflow-scrolling: touch !important;
            white-space: normal !important;
            text-align: left !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            z-index: 100020 !important;
            color: #ffffff !important;
            padding: 2.1rem 1rem 0.85rem 1rem !important;
            box-sizing: border-box !important;
            transition: opacity 0.25s ease-in-out 0.18s, visibility 0s linear 0.9s !important;
        }"""

NEW_TIP_TEXT = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
            display: flex !important;
            flex-direction: column !important;
            position: fixed !important;
            top: var(--hl-fixed-top, 0.75rem) !important;
            left: var(--hl-fixed-left, 0.75rem) !important;
            right: auto !important;
            bottom: auto !important;
            transform: none !important;
            --hl-pop-w: min(21rem, 36vw);
            --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
            width: var(--hl-pop-w) !important;
            min-width: var(--hl-pop-w) !important;
            max-width: var(--hl-pop-w) !important;
            height: auto !important;
            min-height: 0 !important;
            max-height: var(--hl-pop-h) !important;
            overflow: hidden !important;
            white-space: normal !important;
            text-align: left !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            z-index: 100020 !important;
            color: #ffffff !important;
            padding: 0 !important;
            box-sizing: border-box !important;
            transition: opacity 0.25s ease-in-out 0.18s, visibility 0s linear 0.9s !important;
        }"""

OLD_SCROLLBAR = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::-webkit-scrollbar {
            width: 10px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::-webkit-scrollbar-track {
            background: #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border: 2px solid #111827 !important;
            border-radius: 999px !important;
        }"""

NEW_SCROLLBAR = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #111827 !important;
            -webkit-overflow-scrolling: touch !important;
            padding: 0.65rem 1rem 0.85rem 1rem !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
            width: 10px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
            background: #111827 !important;
            border-radius: 999px !important;
        }
        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
            background: #94a3b8 !important;
            border: 2px solid #111827 !important;
            border-radius: 999px !important;
        }"""

OLD_HEADING = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
            display: block !important;
            position: sticky !important;
            top: 0 !important;
            z-index: 2 !important;
            margin: -2.1rem -1rem 0.95rem -1rem !important;
            padding: 1.45rem 1rem 0.85rem 1rem !important;
            background: #1e1e2f !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            border-bottom: 1px solid #334155 !important;
        }"""

NEW_HEADING = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
            display: block !important;
            flex: 0 0 auto !important;
            position: static !important;
            margin: 0 !important;
            padding: 1.45rem 1rem 0.85rem 1rem !important;
            background: #1e1e2f !important;
            color: #ffffff !important;
            font-weight: 700 !important;
            font-size: 1.35rem !important;
            line-height: 1.25 !important;
            border-bottom: 1px solid #334155 !important;
        }"""

OLD_LIST = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.45rem !important;
            padding-top: 0.65rem !important;
            min-width: 0 !important;
        }"""

NEW_LIST = """        .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.45rem !important;
            padding-top: 0 !important;
            min-width: 0 !important;
        }"""

OLD_SUPPORTS = """        @supports (position-anchor: auto) {
            .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
                position: fixed !important;
                left: anchor(right) !important;
                top: anchor(top) !important;
                right: auto !important;
                bottom: auto !important;
                transform: translate(0, calc(-100% - 10px)) !important;
            }
        }
        .full-results-wrap:has(.tip-wrap.headlines-tip:hover) {
            overflow: visible !important;
        }"""

NEW_SUPPORTS = """        .full-results-wrap:has(.tip-wrap.headlines-tip:hover) {
            overflow: visible !important;
        }"""


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for old, new, label in (
        (OLD_TIP_TEXT, NEW_TIP_TEXT, "tip-text"),
        (OLD_SCROLLBAR, NEW_SCROLLBAR, "scrollbar"),
        (OLD_HEADING, NEW_HEADING, "heading"),
        (OLD_LIST, NEW_LIST, "list"),
        (OLD_SUPPORTS, NEW_SUPPORTS, "supports"),
    ):
        if old not in text:
            raise SystemExit(f"Missing {label} block in {path.name}")
        text = text.replace(old, new, 1)
    path.write_text(text, encoding="utf-8")


def main() -> int:
    for path in sorted((ROOT / "pages").glob("*_Top_10.py")):
        patch_file(path)
        print(f"patched {path.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
