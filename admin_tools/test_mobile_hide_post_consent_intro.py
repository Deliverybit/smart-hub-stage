"""Phone/tablet: hide How it works, Sentiment, and Top Picks only after consent."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _agree(page) -> None:
    loc = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
    loc.locator("label").first.click(force=True, position={"x": 8, "y": 8})
    page.wait_for_timeout(8000)


def _snapshot(page) -> dict:
    return page.evaluate(
        """() => {
          const vis = (el) => {
            if (!el) return false;
            const cs = getComputedStyle(el);
            if (cs.display === "none" || cs.visibility === "hidden" || Number(cs.opacity) === 0) return false;
            const r = el.getBoundingClientRect();
            return r.width > 0 && r.height > 0;
          };
          const h3 = [...document.querySelectorAll("h3")].find((n) => /Top Picks/i.test(n.textContent || ""));
          const info = document.querySelector(".scoop-landing-compact .scoop-landing-info");
          return {
            w: window.innerWidth,
            gated: document.documentElement.getAttribute("data-scoop-screener-gated") || "",
            how: vis(info),
            howDisplay: info ? getComputedStyle(info).display : "missing",
            sentiment: vis(document.querySelector(".scoop-landing-compact .scoop-landing-sentiment")),
            top: vis(h3),
            topIsStreamlit: !!(h3 && h3.closest("[data-testid='stMarkdownContainer']")),
            metrics: vis(document.querySelector("[data-testid='stMetric']")),
            summary: vis(document.querySelector(".scoop-landing-compact .scoop-landing-summary")),
          };
        }"""
    )


def main() -> int:
    from playwright.sync_api import sync_playwright

    url = os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NYSE_Top_10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        phone = browser.new_page(viewport={"width": 390, "height": 844})
        phone.goto(url, wait_until="domcontentloaded", timeout=60000)
        phone.wait_for_timeout(5000)
        phone.wait_for_selector('[data-testid="stCheckbox"]', timeout=30000)
        phone.wait_for_timeout(3000)
        gated = _snapshot(phone)
        _agree(phone)
        phone.wait_for_selector(".full-results-wrap, [data-testid='stAlert']", timeout=60000)
        after = _snapshot(phone)

        desk = browser.new_page(viewport={"width": 1600, "height": 900})
        desk.goto(url, wait_until="domcontentloaded", timeout=60000)
        desk.wait_for_timeout(4000)
        if desk.locator('[data-testid="stCheckbox"]').filter(has_text="I agree").count():
            _agree(desk)
        desk.wait_for_selector("h3, .full-results-wrap", timeout=60000)
        desktop = _snapshot(desk)
        browser.close()

    print({"gated": gated, "after": after, "desktop": desktop})
    if gated["w"] > 1366:
        raise SystemExit("FAIL gated check was not phone width")
    if not gated["how"] or not gated["sentiment"]:
        raise SystemExit(f"FAIL consent page lost How it works/Sentiment: {gated}")
    if after["how"] or after["sentiment"] or after["top"]:
        raise SystemExit(f"FAIL post-consent phone still showing intro/top picks: {after}")
    if not after["summary"]:
        raise SystemExit(f"FAIL post-consent phone lost summary: {after}")
    if desktop["w"] < 1367:
        raise SystemExit("FAIL desktop viewport too narrow")
    if not desktop["how"] or not desktop["sentiment"] or not desktop["top"] or not desktop["metrics"]:
        raise SystemExit(f"FAIL desktop post-consent missing intro/top picks: {desktop}")
    if desktop.get("howDisplay") == "none":
        raise SystemExit(f"FAIL desktop How it works display none: {desktop}")
    if not desktop.get("topIsStreamlit"):
        raise SystemExit(f"FAIL desktop Top Picks is not the Streamlit heading: {desktop}")
    print("PASS mobile/tablet hide post-consent intro")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
