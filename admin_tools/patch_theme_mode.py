#!/usr/bin/env python3
"""Wire theme_mode toggle and CSS into app.py and all multipage scripts."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

IMPORT_LINE = "from theme_mode import install_theme_support, render_dark_mode_toggle\n"

INSTALL_AFTER_BANNER = (
    "render_environment_banner(st)\ninstall_theme_support()"
)

INSTALL_AFTER_BANNER_OLD = "render_environment_banner(st)"

TOGGLE_BLOCK = """
render_dark_mode_toggle()
st.sidebar.markdown("---")
"""

SIDEBAR_IMAGE_RE = re.compile(
    r"(st\.sidebar\.image\(logo_path_str\(\), use_container_width=True\)\n"
    r"st\.sidebar\.markdown\(\n"
    r'    """\n'
    r"    <div class=\"sidebar-brand\">.*?"
    r'    unsafe_allow_html=True,\n\)\n)',
    re.S,
)


def patch_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    changed = False

    if "from theme_mode import" not in text:
        if "from branding import" in text:
            text = text.replace(
                "from branding import logo_path_str, render_environment_banner\n",
                "from branding import logo_path_str, render_environment_banner\n" + IMPORT_LINE,
                1,
            )
        else:
            raise SystemExit(f"No branding import in {path.name}")
        changed = True

    if "install_theme_support()" not in text:
        if INSTALL_AFTER_BANNER not in text:
            if INSTALL_AFTER_BANNER_OLD not in text:
                raise SystemExit(f"No render_environment_banner in {path.name}")
            text = text.replace(
                INSTALL_AFTER_BANNER_OLD,
                INSTALL_AFTER_BANNER,
                1,
            )
            changed = True

    if "render_dark_mode_toggle()" not in text:
        match = SIDEBAR_IMAGE_RE.search(text)
        if not match:
            raise SystemExit(f"No sidebar brand block in {path.name}")
        insert_at = match.end()
        text = text[:insert_at] + TOGGLE_BLOCK + text[insert_at:]
        changed = True

    if changed:
        path.write_text(text, encoding="utf-8")


def main() -> int:
    for rel in [
        "app.py",
        "pages/7_Terms_of_Service.py",
        *[f"pages/{p.name}" for p in sorted((ROOT / "pages").glob("*_Top_10.py"))],
    ]:
        patch_file(ROOT / rel)
        print(f"patched {Path(rel).name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
