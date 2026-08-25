"""Playwright check: home logo size and shared mobile/tablet dark-mode toggle CSS."""

from __future__ import annotations

import sys

HOME = "http://localhost:8501/"
NYSE = "http://localhost:8501/NYSE_Top_10"
VIEWPORTS = (
    ("mobile_390", {"width": 390, "height": 844}),
    ("tablet_768", {"width": 768, "height": 1024}),
)

LOGO_JS = """
() => {
    const logoImg = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stImage"] img');
    const header = document.querySelector('[data-testid="stHeader"]');
    if (!logoImg) return { ok: false, reason: 'logo missing' };
    const r = logoImg.getBoundingClientRect();
    const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
    return {
        ok: true,
        logoWidth: Math.round(r.width),
        logoTop: Math.round(r.top),
        headerBottom: Math.round(headerBottom),
        viewport: window.innerWidth,
    };
}
"""

CSS_JS = """
() => {
    const css = [...document.querySelectorAll('style')].map((el) => el.textContent || '').join('\\n');
    return {
        hasLogoMax: css.includes('clamp(190px, 48vw, 280px)'),
        hasSharedToggle: css.includes('html[data-scoop-tab-nav="1"]') && css.includes('[data-testid="stToggle"]'),
        hasUnboxedToggle: css.includes('background: transparent !important') && css.includes(':not(:has([data-testid="stToggle"]))'),
        hasInnerTopToggle: css.includes('.scoop-mobile-inner-top-toggle'),
    };
}
"""

TOGGLE_JS = """
() => {
    const toggleWrap = document.querySelector(
        '[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stToggle"])'
    );
    if (!toggleWrap) return { ok: false };
    const wrapStyle = getComputedStyle(toggleWrap);
    const sw = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-baseweb="switch"]');
    const swStyle = sw ? getComputedStyle(sw) : null;
    return {
        ok: true,
        wrapMinHeight: wrapStyle.minHeight,
        switchWidth: swStyle ? swStyle.width : null,
        switchHeight: swStyle ? swStyle.height : null,
    };
}
"""


def _load(url: str, viewport: dict | None = None) -> None:
    from playwright.sync_api import sync_playwright

    viewport = viewport or {"width": 390, "height": 844}
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)
        _load.logo = page.evaluate(LOGO_JS) if url == HOME else None
        _load.css = page.evaluate(CSS_JS)
        _load.toggle = page.evaluate(TOGGLE_JS)
        browser.close()


def main() -> int:
    try:
        for label, viewport in VIEWPORTS:
            _load(HOME, viewport=viewport)
            home_logo = _load.logo
            assert home_logo and home_logo.get("ok"), f"{label}: {home_logo}"
            assert home_logo["logoWidth"] <= 290, f"{label}: logo width {home_logo['logoWidth']}px"
            assert home_logo["logoTop"] >= home_logo["headerBottom"] - 2, (
                f"{label}: logo top {home_logo['logoTop']}px overlaps header bottom {home_logo['headerBottom']}px"
            )
            print(
                f"PASS {label}: logo={home_logo['logoWidth']}px top={home_logo['logoTop']}px "
                f"header={home_logo['headerBottom']}px"
            )

        _load(HOME)
        home_css = _load.css
        assert home_css["hasLogoMax"], "home logo max CSS missing"
        assert home_css["hasSharedToggle"], "shared toggle CSS missing"
        assert home_css["hasUnboxedToggle"], "unboxed toggle CSS missing"
        print(f"PASS home css={home_css}")

        _load(NYSE)
        nyse_css = _load.css
        assert nyse_css["hasSharedToggle"], "NYSE shared toggle CSS missing"
        assert nyse_css["hasInnerTopToggle"], "inner-top toggle CSS missing"
        print(f"PASS nyse_390 css={nyse_css}")
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("Home logo clearance and shared toggle CSS verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
