"""Playwright check: no sidebar slideout arrow on mobile/tablet tab navigation."""

from __future__ import annotations

import sys

URL = "http://localhost:8501/"
MARKET_URL = "http://localhost:8501/NYSE_Top_10"
VIEWPORTS = (
    ("mobile_390", {"width": 390, "height": 844}),
    ("tablet_768", {"width": 768, "height": 1024}),
)

HIDE_JS = """
() => {
    const sel =
        '[data-testid="stExpandSidebarButton"], [data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"]';
    const found = [];
    for (const el of document.querySelectorAll(sel)) {
        const r = el.getBoundingClientRect();
        const cs = getComputedStyle(el);
        if (r.width > 0 && r.height > 0 && cs.display !== 'none' && cs.visibility !== 'hidden' && cs.opacity !== '0') {
            found.push({
                testid: el.getAttribute('data-testid'),
                width: Math.round(r.width),
                height: Math.round(r.height),
                display: cs.display,
                visibility: cs.visibility,
            });
        }
    }
    return {
        tabNav: document.documentElement.getAttribute('data-scoop-tab-nav'),
        found,
    };
}
"""


def verify_no_sidebar_arrows(url: str, label: str, viewport: dict) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)
        result = page.evaluate(HIDE_JS)
        browser.close()

    assert result["tabNav"] == "1", f"{label}: data-scoop-tab-nav not set"
    assert not result["found"], f"{label}: visible sidebar controls {result['found']}"
    print(f"PASS {label} @ {url}")


def main() -> int:
    try:
        for viewport_name, viewport in VIEWPORTS:
            verify_no_sidebar_arrows(URL, f"home_{viewport_name}", viewport)
            verify_no_sidebar_arrows(MARKET_URL, f"nyse_{viewport_name}", viewport)
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("No sidebar slideout arrows at mobile/tablet widths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
