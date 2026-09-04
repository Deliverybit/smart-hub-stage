"""Desktop-only: on-screen, scrollable, narrow Headlines panel right of the column."""

from __future__ import annotations

import streamlit as st

_CSS = """
@media (min-width: 1367px) {
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text:hover {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked):hover > .tip-text,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open:hover > .tip-text {
        position: fixed !important;
        display: flex !important;
        flex-direction: column !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        transform: none !important;
        right: auto !important;
        bottom: auto !important;
        box-sizing: border-box !important;
        width: 280px !important;
        max-width: 280px !important;
        min-width: 280px !important;
        min-height: 12rem !important;
        max-height: calc(100vh - 24px) !important;
        overflow: hidden !important;
        z-index: 2147483000 !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        hyphens: none !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-heading,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        white-space: normal !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        hyphens: none !important;
        line-height: 1.3 !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .headlines-tip-scroll,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .headlines-tip-scroll {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        flex: 1 1 auto !important;
        min-height: 8rem !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        pointer-events: auto !important;
        scrollbar-width: thin !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open > .tip-text .hl-tip-line,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) > .tip-text .hl-tip-line a {
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #ffffff !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
}
"""

_JS = r"""
(() => {
    const VERSION = 1;
    const DESKTOP_MIN = 1367;
    const BOX_W = 280;
    const M = 12;
    const GAP = 12;
    let appDoc = document;
    let appWin = window;
    try {
        if (window.parent && window.parent !== window && window.parent.document) {
            appDoc = window.parent.document;
            appWin = window.parent;
        }
    } catch (e) {}
    appWin.__scoopDesktopHlNarrowV = VERSION;

    const isDesktop = () => (appWin.innerWidth || 0) >= DESKTOP_MIN;

    const headlinesTh = () => [...appDoc.querySelectorAll(".full-results-wrap .full-results-table thead th")].find((th) => {
        const t = (th.textContent || "").replace(/\s+/g, " ").trim();
        return t.startsWith("Headlines") && !t.startsWith("Headline ");
    }) || null;

    const headingBase = (heading) => {
        if (!heading) return "Headlines";
        if (!heading.dataset.hlBaseLabel) {
            const current = (heading.textContent || "Headlines").trim();
            heading.dataset.hlBaseLabel = current.split(" - ")[0].trim() || "Headlines";
        }
        return heading.dataset.hlBaseLabel;
    };

    const companyName = (wrap) => {
        const row = wrap && wrap.closest("tr");
        if (!row) return "";
        const inCommodity = !!wrap.closest(".commodity-results");
        const valueCell =
            row.querySelector('td[data-label="Company"] .fr-val') ||
            row.querySelector('td[data-label="Name"] .fr-val') ||
            (inCommodity ? row.querySelector('td[data-label="Commodity"] .fr-val') : null);
        if (!valueCell) return "";
        const tipWrap = valueCell.querySelector(".tip-wrap");
        if (tipWrap) {
            const clone = tipWrap.cloneNode(true);
            clone.querySelectorAll(".tip-text").forEach((n) => n.remove());
            return (clone.textContent || "").replace(/\s+/g, " ").trim();
        }
        return (valueCell.textContent || "").replace(/\s+/g, " ").trim();
    };

    const place = (wrap) => {
        if (!isDesktop() || !wrap) return;
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) return;
        wrap.classList.add("hl-tip-desktop-open");
        appWin.__scoopDesktopHlOpenedAt = Date.now();
        const heading = tip.querySelector(".hl-tip-heading");
        if (heading) {
            const company = companyName(wrap);
            heading.textContent = company ? `${headingBase(heading)} - ${company}` : headingBase(heading);
        }
        const td = wrap.closest('td[data-label="Headlines"]');
        const th = headlinesTh();
        const colRight = td ? td.getBoundingClientRect().right : (th ? th.getBoundingClientRect().right : M);
        const vw = appWin.innerWidth || 1600;
        const vh = appWin.innerHeight || 900;
        let left = Math.round(colRight + GAP);
        if (left + BOX_W > vw - M) left = vw - M - BOX_W;
        if (left < M) left = M;

        tip.style.setProperty("position", "fixed", "important");
        tip.style.setProperty("left", left + "px", "important");
        tip.style.setProperty("width", BOX_W + "px", "important");
        tip.style.setProperty("max-width", BOX_W + "px", "important");
        tip.style.setProperty("min-width", BOX_W + "px", "important");
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
        tip.style.setProperty("--hl-fixed-left", left + "px");
        tip.style.setProperty("--hl-fixed-width", BOX_W + "px");

        const scroll = tip.querySelector(".headlines-tip-scroll");
        const headingEl = tip.querySelector(".hl-tip-heading");
        const list = scroll && scroll.querySelector(".headlines-tip-list");
        const headingH = headingEl ? headingEl.offsetHeight : 48;
        const listH = list ? list.scrollHeight : (scroll ? scroll.scrollHeight : 240);
        const contentH = headingH + listH + 24;
        const maxH = Math.max(200, vh - 2 * M);
        const height = Math.min(Math.max(contentH, headingH + 128), maxH);
        let top = M;
        if (th) {
            const preferred = Math.round(th.getBoundingClientRect().top - 30 - height);
            if (preferred >= M) top = preferred;
        }
        if (top + height > vh - M) top = Math.max(M, vh - M - height);
        if (top < M) top = M;

        tip.style.setProperty("top", top + "px", "important");
        tip.style.setProperty("height", height + "px", "important");
        tip.style.setProperty("max-height", maxH + "px", "important");
        tip.style.setProperty("--hl-fixed-top", top + "px");
        tip.style.setProperty("--hl-fixed-height", height + "px");
        tip.style.setProperty("--hl-fixed-max-height", maxH + "px");
        if (scroll) {
            const scrollH = Math.max(128, height - headingH);
            scroll.style.setProperty("overflow-y", "auto", "important");
            scroll.style.setProperty("height", scrollH + "px", "important");
            scroll.style.setProperty("max-height", scrollH + "px", "important");
            scroll.style.setProperty("min-height", "8rem", "important");
            scroll.style.setProperty("visibility", "visible", "important");
        }
    };

    const onClick = (event) => {
        if (!isDesktop() || !event.target || !event.target.closest) return;
        const label = event.target.closest(".hl-tip-count");
        if (!label) return;
        const wrap = label.closest(".tip-wrap.headlines-tip");
        if (!wrap) return;
        const run = () => place(wrap);
        run();
        appWin.requestAnimationFrame(run);
        appWin.setTimeout(run, 40);
        appWin.setTimeout(run, 180);
    };

    const onChange = (event) => {
        if (!isDesktop() || !event.target || !event.target.classList) return;
        if (!event.target.classList.contains("hl-tip-cb")) return;
        const wrap = event.target.closest(".tip-wrap.headlines-tip");
        if (event.target.checked) place(wrap);
    };

    if (appWin.__scoopHlNarrowClick) {
        appDoc.removeEventListener("click", appWin.__scoopHlNarrowClick, true);
        appDoc.removeEventListener("change", appWin.__scoopHlNarrowChange, true);
    }
    appWin.__scoopHlNarrowClick = onClick;
    appWin.__scoopHlNarrowChange = onChange;
    appDoc.addEventListener("click", onClick, true);
    appDoc.addEventListener("change", onChange, true);
})();
"""


def inject_desktop_headlines_narrow() -> None:
    st.html(
        f"<style id='scoop-desktop-hl-narrow'>{_CSS}</style>"
        f"<script id='scoop-desktop-hl-narrow-js'>{_JS}</script>",
        unsafe_allow_javascript=True,
    )
