"""Playwright check: home logo size and shared mobile/tablet dark-mode toggle CSS."""

from __future__ import annotations

import sys

HOME = "http://localhost:8501/"
NYSE = "http://localhost:8501/NYSE_Top_10"

LOGO_JS = """
() => {
    const logoImg = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stImage"] img');
    if (!logoImg) return { ok: false, reason: 'logo missing' };
    const r = logoImg.getBoundingClientRect();
    return { ok: true, logoWidth: Math.round(r.width), viewport: window.innerWidth };
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


def _load(url: str) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 390, "height": 844})
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(8000)
        _load.logo = page.evaluate(LOGO_JS) if url == HOME else None
        _load.css = page.evaluate(CSS_JS)
        _load.toggle = page.evaluate(TOGGLE_JS)
        browser.close()


def main() -> int:
    try:
        _load(HOME)
        home_logo = _load.logo
        home_css = _load.css
        home_toggle = _load.toggle

        assert home_logo and home_logo.get("ok"), home_logo
        assert home_logo["logoWidth"] <= 290, f"logo width {home_logo['logoWidth']}px"
        assert home_css["hasLogoMax"], "home logo max CSS missing"
        assert home_css["hasSharedToggle"], "shared toggle CSS missing"
        assert home_css["hasUnboxedToggle"], "unboxed toggle CSS missing"
        print(f"PASS home_390 logo={home_logo['logoWidth']}px css={home_css}")

        _load(NYSE)
        nyse_css = _load.css
        nyse_toggle = _load.toggle
        assert nyse_css["hasSharedToggle"], "NYSE shared toggle CSS missing"
        assert nyse_css["hasInnerTopToggle"], "inner-top toggle CSS missing"
        print(f"PASS nyse_390 css={nyse_css}")

        if home_toggle.get("ok") and nyse_toggle.get("ok"):
            assert home_toggle["wrapMinHeight"] == nyse_toggle["wrapMinHeight"]
            assert home_toggle["switchWidth"] == nyse_toggle["switchWidth"]
            print(f"PASS toggle metrics match: {home_toggle}")
        else:
            print("SKIP runtime toggle metrics (theme not hydrated in headless)")
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("Home logo and shared toggle CSS verified.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
