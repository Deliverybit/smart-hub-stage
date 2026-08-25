"""Playwright check: mobile/tablet spacing below Dark mode and Terms checkbox."""

from __future__ import annotations

import sys

URL = "http://localhost:8501/NASDAQ_Top_10"
VIEWPORTS = (
    ("mobile_390", {"width": 390, "height": 844}),
    ("tablet_768", {"width": 768, "height": 1024}),
)

SPACING_JS = """
() => {
    const main = document.querySelector('[data-testid="stMainBlockContainer"]');
    if (!main) return { ok: false, reason: 'missing main block' };

    const darkModeWrap = main.querySelector(
        '[data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="stElementContainer"]:has([data-testid="stToggle"], [data-testid="stCheckbox"]), '
        + '[data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="element-container"]:has([data-testid="stToggle"], [data-testid="stCheckbox"])'
    );

    let bannerWrap = null;
    for (const el of main.querySelectorAll('[data-testid="stElementContainer"], [data-testid="element-container"]')) {
        const text = el.textContent || '';
        if (text.includes('NASDAQ Composite') && text.includes('Today')) {
            bannerWrap = el;
            break;
        }
    }

    const termsWrap = main.querySelector(
        '[data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):has(+ [data-testid="stElementContainer"] .disclaimer-footer), '
        + '[data-testid="element-container"]:has([data-testid="stCheckbox"]):has(+ [data-testid="element-container"] .disclaimer-footer)'
    );
    const disclaimer = document.querySelector('.disclaimer-footer');

    const toggleGap = darkModeWrap && bannerWrap
        ? Math.round(bannerWrap.getBoundingClientRect().top - darkModeWrap.getBoundingClientRect().bottom)
        : null;
    const consentGap = termsWrap && disclaimer
        ? Math.round(disclaimer.getBoundingClientRect().top - termsWrap.getBoundingClientRect().bottom)
        : null;

    return {
        ok: true,
        width: window.innerWidth,
        tabNav: document.documentElement.getAttribute('data-scoop-tab-nav'),
        gated: document.documentElement.getAttribute('data-scoop-screener-gated'),
        hasDarkModeWrap: !!darkModeWrap,
        hasBannerWrap: !!bannerWrap,
        hasTermsWrap: !!termsWrap,
        toggleGap,
        consentGap,
        darkModeMb: darkModeWrap ? getComputedStyle(darkModeWrap).marginBottom : null,
        darkModePb: darkModeWrap ? getComputedStyle(darkModeWrap).paddingBottom : null,
        bannerMt: bannerWrap ? getComputedStyle(bannerWrap).marginTop : null,
        termsMb: termsWrap ? getComputedStyle(termsWrap).marginBottom : null,
        disclaimerMt: disclaimer ? getComputedStyle(disclaimer).marginTop : null,
    };
}
"""


def verify_spacing(label: str, viewport: dict) -> None:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch(headless=True)
        page = browser.new_page(viewport=viewport)
        page.goto(URL, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(7000)
        result = page.evaluate(SPACING_JS)
        browser.close()

    assert result.get("ok"), f"{label}: {result.get('reason')}"
    assert result["tabNav"] == "1", f"{label}: tab nav flag missing"
    assert result["gated"] == "1", f"{label}: screener gated flag missing"
    assert result["hasDarkModeWrap"], f"{label}: dark mode row not found"
    assert result["hasTermsWrap"], f"{label}: terms checkbox row not found"
    assert result["toggleGap"] is not None and result["toggleGap"] >= 10, (
        f"{label}: dark-mode gap is {result['toggleGap']}px (expected >= 10px)"
    )
    assert result["consentGap"] is not None and result["consentGap"] >= 10, (
        f"{label}: consent gap is {result['consentGap']}px (expected >= 10px)"
    )
    print(
        f"PASS {label}: toggleGap={result['toggleGap']}px consentGap={result['consentGap']}px "
        f"darkModeMb={result['darkModeMb']} darkModePb={result['darkModePb']} "
        f"bannerMt={result['bannerMt']} termsMb={result['termsMb']} "
        f"disclaimerMt={result['disclaimerMt']}"
    )


def main() -> int:
    try:
        for label, viewport in VIEWPORTS:
            verify_spacing(label, viewport)
    except Exception as exc:
        print(f"FAIL {exc}", file=sys.stderr)
        return 1
    print("Mobile/tablet button spacing verified on NASDAQ.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
