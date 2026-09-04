"""Desktop Headlines: narrow on-screen scrollable panel beside the column."""

from __future__ import annotations

import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))


def main() -> int:
    from playwright.sync_api import sync_playwright

    url = os.environ.get("SCOOP_URL", "http://localhost:8501") + "/NYSE_Top_10"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page(viewport={"width": 1600, "height": 900})
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        agree = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
        if agree.count():
            agree.locator("label").first.click(force=True, position={"x": 8, "y": 8})
        page.wait_for_selector(".full-results-wrap", timeout=90000)
        page.wait_for_timeout(400)
        page.locator(".hl-tip-count").first.click()
        page.wait_for_timeout(80)
        early = page.evaluate(
            """() => {
              const tip = document.querySelector(".tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text");
              if (!tip) return {ok: false};
              const r = tip.getBoundingClientRect();
              return {w: r.width, h: r.height, vis: getComputedStyle(tip).visibility};
            }"""
        )
        page.wait_for_timeout(1500)
        page.screenshot(path=str(ROOT / "admin_tools" / "_hl_desktop_nyse.png"), full_page=False)
        info = page.evaluate(
            """() => {
              const wrap = document.querySelector(".tip-wrap.headlines-tip.hl-tip-desktop-open, .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)");
              const tip = wrap && wrap.querySelector(":scope > .tip-text");
              const td = wrap && wrap.closest('td[data-label="Headlines"]');
              const scroll = tip && tip.querySelector(".headlines-tip-scroll");
              if (!tip) return {ok: false};
              const r = tip.getBoundingClientRect();
              const colRight = td ? td.getBoundingClientRect().right : 0;
              const moodTh = [...document.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) =>
                (th.textContent || "").replace(/\\s+/g, " ").trim().startsWith("Market Mood")
              );
              const moodTd = [...document.querySelectorAll('.full-results-wrap td[data-label="Market Mood"]')].find((el) => {
                const r = el.getBoundingClientRect();
                return r.width > 40 && r.bottom > 0 && r.top < window.innerHeight;
              });
              const mood = moodTd ? moodTd.getBoundingClientRect() : (moodTh ? moodTh.getBoundingClientRect() : null);
              const tbody = document.querySelector(".full-results-wrap .full-results-table tbody");
              const tbodyBottom = tbody ? tbody.getBoundingClientRect().bottom : 0;
              return {
                w: window.innerWidth,
                h: window.innerHeight,
                vis: getComputedStyle(tip).visibility,
                boxW: r.width,
                boxH: r.height,
                top: r.top,
                left: r.left,
                bottom: r.bottom,
                right: r.right,
                moodLeft: mood ? mood.left : 0,
                moodW: mood ? mood.width : 0,
                moodTop: mood ? mood.top : 0,
                tbodyBottom,
                links: tip.querySelectorAll(".hl-tip-line a").length,
                heading: (tip.querySelector(".hl-tip-heading") || {}).textContent || "",
                headingColor: tip.querySelector(".hl-tip-heading") ? getComputedStyle(tip.querySelector(".hl-tip-heading")).color : "",
                borderColor: getComputedStyle(tip).borderTopColor,
                linkColor: (() => { const a = tip.querySelector(".hl-tip-line a"); return a ? getComputedStyle(a).color : ""; })(),
                theme: document.documentElement.getAttribute("data-scoop-theme") || "",
                scrollY: scroll ? getComputedStyle(scroll).overflowY : "",
                canScroll: !!(scroll && scroll.scrollHeight > scroll.clientHeight + 4),
                standalone: window.__scoopDesktopHeadlinesStandalone || 0,
              };
            }"""
        )
        print("early", early)
        print(info)
        browser.close()

    if not early.get("ok", True) and early.get("vis") != "visible":
        raise SystemExit(f"FAIL did not open: {early}")
    if early.get("h", 0) > 80 and info.get("boxH", 0) < early["h"] * 0.5:
        raise SystemExit(f"FAIL panel collapsed after open: early={early} later={info}")

    if info.get("w", 0) < 1367:
        raise SystemExit("FAIL not desktop")
    if info.get("vis") != "visible" or info.get("links", 0) < 1:
        raise SystemExit(f"FAIL not open with links: {info}")
    if info.get("standalone", 0) < 1:
        raise SystemExit(f"FAIL desktop Headlines script not loaded: {info}")
    if "147, 197, 253" not in (info.get("headingColor") or ""):
        raise SystemExit(f"FAIL heading is not blue: {info}")
    if info.get("theme") == "dark":
        if "255, 255, 255" not in (info.get("borderColor") or ""):
            raise SystemExit(f"FAIL dark desktop container is not white: {info}")
        if "255, 255, 255" not in (info.get("linkColor") or ""):
            raise SystemExit(f"FAIL dark desktop links are not white: {info}")
    else:
        if "34, 197, 94" not in (info.get("borderColor") or ""):
            raise SystemExit(f"FAIL container is not green: {info}")
        if "255, 255, 255" not in (info.get("linkColor") or ""):
            raise SystemExit(f"FAIL light desktop links are not white: {info}")
    if info.get("boxW", 0) < 250 or info.get("boxH", 0) < 250:
        raise SystemExit(f"FAIL postage-stamp panel: {info}")
    if info.get("moodW", 0) > 40 and info.get("moodTop", 0) > 0 and info.get("moodTop", 0) < info.get("h", 900):
        if abs(info.get("left", 0) - info.get("moodLeft", 0)) > 36:
            raise SystemExit(f"FAIL not over Market Mood column: {info}")
        if info.get("top", 0) > info.get("moodTop", 0) + 24:
            raise SystemExit(f"FAIL not starting at visible Market Mood: {info}")
    if info.get("top", -1) < 8 or info.get("left", -1) < 8:
        raise SystemExit(f"FAIL clipped top/left: {info}")
    if info.get("right", 0) > info.get("w", 0) - 8:
        raise SystemExit(f"FAIL clipped right: {info}")
    if info.get("bottom", 0) > info.get("h", 0) - 8:
        raise SystemExit(f"FAIL clipped bottom: {info}")
    if info.get("boxH", 0) < 180:
        raise SystemExit(f"FAIL too short to show headlines: {info}")
    if info.get("scrollY") not in ("auto", "scroll") and not info.get("canScroll"):
        # tall enough to fit without scroll is OK if all links exist
        if info.get("links", 0) < 5:
            raise SystemExit(f"FAIL no scroll and too few links: {info}")
    print("PASS desktop Headlines on-screen scrollable narrow panel")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, channel="chrome")
        page = browser.new_page(viewport={"width": 1024, "height": 768})
        page.goto(url, wait_until="domcontentloaded", timeout=60000)
        page.wait_for_timeout(4000)
        agree = page.locator('[data-testid="stCheckbox"]').filter(has_text="I agree")
        if agree.count():
            agree.locator("label").first.click(force=True, position={"x": 8, "y": 8})
            page.wait_for_timeout(8000)
        counts = page.locator(".hl-tip-count")
        if counts.count() == 0:
            print("tablet gated or no Headlines counts; CSS remains @media (min-width: 1367px) only")
            browser.close()
            print("PASS tablet did not get desktop Headlines side panel")
            return 0
        counts.nth(min(3, counts.count() - 1)).click()
        page.wait_for_timeout(800)
        page.screenshot(path=str(ROOT / "admin_tools" / "_hl_tablet_nyse.png"), full_page=False)
        tablet = page.evaluate(
            """() => {
              const wrap = document.querySelector(".tip-wrap.headlines-tip:has(.hl-tip-cb:checked)");
              const tip = wrap && wrap.querySelector(":scope > .tip-text");
              const td = wrap && wrap.closest('td[data-label="Headlines"]');
              if (!tip) return {open: false, w: window.innerWidth};
              const r = tip.getBoundingClientRect();
              const colRight = td ? td.getBoundingClientRect().right : 0;
              return {
                open: true,
                w: window.innerWidth,
                boxW: r.width,
                left: r.left,
                colRight,
                leftGap: r.left - colRight,
                vis: getComputedStyle(tip).visibility,
              };
            }"""
        )
        print("tablet", tablet)
        browser.close()

    if tablet.get("w", 0) >= 1367:
        raise SystemExit("FAIL tablet test used desktop width")
    if tablet.get("open") and tablet.get("vis") == "visible":
        # Tablet overlay is allowed; it must not be the 280px desktop side panel.
        if 270 <= tablet.get("boxW", 0) <= 300 and 8 <= tablet.get("leftGap", -1) <= 20:
            raise SystemExit(f"FAIL desktop side panel appeared on tablet: {tablet}")
    print("PASS tablet did not get desktop Headlines side panel")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
