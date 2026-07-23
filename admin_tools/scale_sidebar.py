#!/usr/bin/env python3
"""Make sidebar width scale with zoom and prevent nav label clipping."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SIDEBAR_ROOT = """    :root {
        --scoop-sidebar-width: clamp(12rem, 20vw, 36rem);
    }
    /* Sidebar: rem-based width scales with browser zoom; no label clipping */
    [data-testid="stSidebar"],
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        min-width: var(--scoop-sidebar-width) !important;
        width: var(--scoop-sidebar-width) !important;
        max-width: min(92vw, 36rem) !important;
        overflow-x: visible !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stPageLink"] a,
    [data-testid="stSidebar"] [data-testid="stPageLink"] span,
    [data-testid="stSidebar"] [data-testid="stPageLink"] p {
        white-space: normal !important;
        overflow: visible !important;
        text-overflow: clip !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] .stCaption p,
    [data-testid="stSidebar"] [data-testid="stCaptionContainer"] p {
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }
"""

OLD_DESKTOP_SIDEBAR = '[data-testid="stSidebar"] { min-width: 380px !important; }'

OLD_MOBILE_SIDEBAR = """        [data-testid="stSidebar"] {
            min-width: 360px !important;
            width: min(92vw, 360px) !important;
            max-width: 360px !important;
        }
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            width: 100% !important;
        }"""

NEW_MOBILE_SIDEBAR = """        :root { --scoop-sidebar-width: clamp(20rem, 92vw, 36rem); }
        [data-testid="stSidebar"],
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: 92vw !important;
            overflow-x: visible !important;
        }"""

OLD_FOOTER_ROOT = ":root { --footer-sidebar-width: 360px; }"
NEW_FOOTER_ROOT = ":root { --footer-sidebar-width: clamp(12rem, 20vw, 36rem); }"


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    changed = False

    if SIDEBAR_ROOT.strip() not in text:
        marker = "    <style>\n"
        if marker in text:
            text = text.replace(marker, marker + SIDEBAR_ROOT + "\n", 1)
            changed = True
        else:
            print(f"skip root insert: {path.name}")
            return

    if OLD_DESKTOP_SIDEBAR in text:
        text = text.replace(OLD_DESKTOP_SIDEBAR, "")
        changed = True

    if OLD_MOBILE_SIDEBAR in text:
        text = text.replace(OLD_MOBILE_SIDEBAR, NEW_MOBILE_SIDEBAR)
        changed = True

    if OLD_FOOTER_ROOT in text:
        text = text.replace(OLD_FOOTER_ROOT, NEW_FOOTER_ROOT)
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")
        print(f"patched {path.name}")


def main() -> int:
    files = [ROOT / "app.py", *sorted((ROOT / "pages").glob("*.py"))]
    for path in files:
        if "<style>" in path.read_text(encoding="utf-8"):
            patch_file(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
