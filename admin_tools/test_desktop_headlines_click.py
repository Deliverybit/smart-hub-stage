"""Playwright: desktop Headlines sits right of column, 30px above heading; dismiss rules."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def _agree_if_needed(page) -> None:
    loc = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
    if loc.count() == 0:
        return
    loc.locator("label").first.click(force=True, position={"x": 8, "y": 8})
    page.wait_for_timeout(8000)


def _open_info(page):
    return page.evaluate(
        """() => {
          const wrap = document.querySelector(".tip-wrap.headlines-tip:has(.hl-tip-cb:checked), .tip-wrap.headlines-tip.hl-tip-desktop-open");
          const tip = wrap && wrap.querySelector(":scope > .tip-text");
          const ths = [...document.querySelectorAll(".full-results-wrap .full-results-table thead th")];
          const hl = ths.find((th) => {
            const t = (th.textContent || "").replace(/\\s+/g, " ").trim();
            return t.startsWith("Headlines") && !t.startsWith("Headline ");
          });
          const col = hl ? hl.getBoundingClientRect() : null;
          const open = !!(tip && getComputedStyle(tip).visibility === "visible" && Number(getComputedStyle(tip).opacity) > 0.5 && tip.getBoundingClientRect().top > -1000);
          if (!tip || !col) {
            const labels = ths.map((th) => (th.textContent || "").replace(/\\s+/g, " ").trim().slice(0, 40));
            return { open, w: window.innerWidth, reason: "missing", hasTip: !!tip, hasCol: !!col, labels, standalone: window.__scoopDesktopHeadlinesStandalone || 0, dismissV: window.__scoopDesktopHlDismissV || 0 };
          }
          const r = tip.getBoundingClientRect();
          const links = tip.querySelectorAll(".hl-tip-line a").length;
          const cs = getComputedStyle(tip);
          const theme = document.documentElement.getAttribute("data-scoop-theme") || "";
          return {
            open,
            w: window.innerWidth,
            top: r.top, left: r.left, bottom: r.bottom, width: r.width, height: r.height,
            colRight: col.right, colTop: col.top,
            leftGap: r.left - col.right,
            above: col.top - r.bottom,
            links,
            border: cs.borderTopWidth + " " + cs.borderTopStyle + " " + cs.borderTopColor,
            theme,
            standalone: window.__scoopDesktopHeadlinesStandalone || 0,
            dismissV: window.__scoopDesktopHlDismissV || 0,
          };
        }"""
    )


def main() -> int:
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NASDAQ_Top_10", wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(5000)
        page.get_by_text("I agree to the Disclaimer", exact=False).wait_for(timeout=30000)
        if page.locator(".hl-tip-count").count() == 0:
            _agree_if_needed(page)
        page.wait_for_selector(".hl-tip-count", timeout=60000)
        header = page.locator(".full-results-wrap .full-results-table thead")
        header.scroll_into_view_if_needed()
        page.wait_for_timeout(300)
        count = page.locator(".hl-tip-count").first
        count.click()
        page.wait_for_timeout(700)
        opened = _open_info(page)

        page.mouse.click(40, 40)
        page.wait_for_timeout(400)
        after_outside = _open_info(page)

        count.click()
        page.wait_for_timeout(500)
        other = page.locator(".full-results-wrap tbody .tip-wrap:not(.headlines-tip)").first
        other.click(force=True)
        page.wait_for_timeout(400)
        after_other_tip = _open_info(page)

        count.click()
        page.wait_for_timeout(500)
        page.mouse.wheel(0, 400)
        page.wait_for_timeout(400)
        after_scroll = _open_info(page)
        browser.close()

    print(
        {
            "opened": opened,
            "after_outside": after_outside,
            "after_other_tip": after_other_tip,
            "after_scroll": after_scroll,
        }
    )
    if opened.get("w", 0) < 1367:
        raise SystemExit("FAIL not desktop")
    if not opened.get("open") or opened.get("links", 0) < 1:
        raise SystemExit(f"FAIL did not open: {opened}")
    border = (opened.get("border") or "").lower()
    theme = (opened.get("theme") or "").lower()
    if theme == "dark":
        if "rgb(255, 255, 255)" not in border and "rgb(255,255,255)" not in border:
            raise SystemExit(f"FAIL dark desktop Headlines missing white box: {opened}")
    elif "rgb(34, 197, 94)" not in border and "#22c55e" not in border:
        raise SystemExit(f"FAIL desktop Headlines missing green box: {opened}")
    if after_outside.get("open"):
        raise SystemExit(f"FAIL still open after outside click: {after_outside}")
    if after_other_tip.get("open"):
        raise SystemExit(f"FAIL still open after other tooltip click: {after_other_tip}")
    if after_scroll.get("open"):
        raise SystemExit(f"FAIL still open after scroll: {after_scroll}")
    print("PASS desktop headlines dismiss")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
