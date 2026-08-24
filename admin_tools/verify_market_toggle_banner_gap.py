"""Playwright check: gap between dark toggle row and market banner on screener pages."""

from __future__ import annotations

import sys

URL = "http://localhost:8501/NYSE_Top_10"
VIEWPORTS = (
    ("mobile_390", {"width": 390, "height": 844}),
    ("tablet_768", {"width": 768, "height": 1024}),
)

GAP_JS = """
() => {
    const toggleWrap = document.querySelector('[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]), [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stCheckbox"]), [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stToggle"]), [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stToggle"])');
    let bannerWrap = null;
    for (const el of document.querySelectorAll('[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]')) {
        if ((el.textContent || '').includes('NYSE Composite') && (el.textContent || '').includes('Today')) {
            bannerWrap = el;
            break;
        }
    }
    if (!toggleWrap || !bannerWrap) {
        return { ok: false, reason: 'missing elements' };
    }
    const t = toggleWrap.getBoundingClientRect();
    const b = bannerWrap.getBoundingClientRect();
    const gap = Math.round(b.top - t.bottom);
    const toggleMb = getComputedStyle(toggleWrap).marginBottom;
    const bannerMt = getComputedStyle(bannerWrap).marginTop;
    return {
        ok: true,
        gap,
        toggleMb,
        bannerMt,
        tabNav: document.documentElement.getAttribute('data-scoop-tab-nav'),
        screener: document.documentElement.getAttribute('data-scoop-screener-active'),
    };
}
"""


def verify_toggle_banner_gap(label: str, viewport: dict) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(6000)
        result = page.evaluate(GAP_JS)
        browser.close()

    assert result.get("ok"), f"{label}: {result.get('reason')}"
    assert result["tabNav"] == "1", f"{label}: tab nav flag missing"
    assert result["screener"] == "1", f"{label}: screener flag missing"
    assert result["gap"] >= 10, f"{label}: gap is {result['gap']}px (expected at least 10px)"
    print(f"PASS {label}: gap={result['gap']}px toggleMb={result['toggleMb']} bannerMt={result['bannerMt']}")


def main() -> int:
    try:
        for label, viewport in VIEWPORTS:
            verify_toggle_banner_gap(label, viewport)
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("Toggle-to-banner spacing verified on NYSE at mobile and tablet widths.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
