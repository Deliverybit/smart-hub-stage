import sys
from pathlib import Path

import streamlit as st

_ADMIN = Path(__file__).resolve().parent / "admin_tools"
if str(_ADMIN) not in sys.path:
    sys.path.insert(0, str(_ADMIN))

from tablet_mobile_layout_css import MOBILE_CARD_FIELD_ORDER, MOBILE_HEADLINES_CARD_OVERLAY  # noqa: E402

_MOBILE_HEADLINES_CSS = f"""
@media (max-width: 768px) {{
{MOBILE_HEADLINES_CARD_OVERLAY}
}}
"""

_MOBILE_TABLET_CARD_ORDER_CSS = f"""
@media (max-width: 1366px) {{
{MOBILE_CARD_FIELD_ORDER}
}}
"""

_DESKTOP_HEADLINES_CSS = """
@media (min-width: 1367px) {
    /* Desktop: click Headlines count to open; click outside (backdrop) to close. */
    .tip-wrap.headlines-tip .hl-tip-cb {
        position: absolute !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        pointer-events: none !important;
    }
    .tip-wrap.headlines-tip .hl-tip-count {
        cursor: pointer !important;
        text-decoration: inherit !important;
        pointer-events: auto !important;
    }
    .tip-wrap.headlines-tip .hl-tip-backdrop {
        display: none !important;
    }
    .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
        display: block !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 100019 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        background: transparent !important;
        cursor: default !important;
        pointer-events: auto !important;
    }
    .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
        display: none !important;
    }
    /* JS positions via --hl-fixed-*; disable anchor positioning (stray box at row). */
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text {
        position-anchor: none !important;
        anchor-name: none !important;
        position: fixed !important;
        top: var(--hl-fixed-top, -10000px) !important;
        left: var(--hl-fixed-left, -10000px) !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
        transform: none !important;
        transition: none !important;
        --hl-pop-w: min(21rem, 36vw);
        --hl-pop-h: min(calc(100vh - 1.5rem), 42rem);
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
        height: var(--hl-fixed-height, auto) !important;
        min-height: 0 !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        overflow: hidden !important;
        padding: 0 !important;
        z-index: 100020 !important;
        box-sizing: border-box !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        display: flex !important;
        flex-direction: column !important;
        align-items: stretch !important;
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        height: var(--hl-fixed-height, auto) !important;
        overflow: hidden !important;
        overscroll-behavior: contain !important;
        touch-action: pan-y !important;
        transition: none !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        display: block !important;
        visibility: visible !important;
        position: relative !important;
        top: auto !important;
        z-index: 2 !important;
        margin: 0 !important;
        padding: 1.45rem 1rem 0.85rem 1rem !important;
        background: #1e1e2f !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: 1.35rem !important;
        line-height: 1.25 !important;
        border-bottom: 1px solid #334155 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
        flex: 1 1 0 !important;
        display: block !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow-x: hidden !important;
        overflow-y: scroll !important;
        overscroll-behavior: contain !important;
        overscroll-behavior-y: contain !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-gutter: stable !important;
        scrollbar-width: thin !important;
        scrollbar-color: #94a3b8 #111827 !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
        padding: 0.65rem 1rem 0.65rem 1rem !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        width: 10px !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
        background: #111827 !important;
        border-radius: 999px !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
        background: #94a3b8 !important;
        border: 2px solid #111827 !important;
        border-radius: 999px !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-list {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.45rem !important;
        min-width: 0 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
        display: block !important;
        word-break: normal !important;
        overflow-wrap: break-word !important;
        white-space: normal !important;
        min-width: 0 !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::before,
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text::after {
        display: none !important;
    }
    html.scoop-tooltip-scrolling .full-results-wrap .tip-wrap.headlines-tip:not(.hl-tip-desktop-open) .tip-text,
    body.scoop-tooltip-scrolling .full-results-wrap .tip-wrap.headlines-tip:not(.hl-tip-desktop-open) .tip-text {
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    /* Override page/tablet rules inside stMarkdown on desktop open state. */
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text {
        display: flex !important;
        flex-direction: column !important;
        position: fixed !important;
        overflow: hidden !important;
        touch-action: pan-y !important;
        height: var(--hl-fixed-height, auto) !important;
        max-height: var(--hl-fixed-max-height, var(--hl-pop-h)) !important;
        width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
        max-width: var(--hl-fixed-width, var(--hl-pop-w)) !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll {
        flex: 1 1 0 !important;
        min-height: 0 !important;
        overflow-x: hidden !important;
        overflow-y: scroll !important;
        max-height: none !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .hl-tip-line a {
        word-break: normal !important;
        overflow-wrap: break-word !important;
    }
}
"""

_TABLET_HEADLINES_POPUP_CSS = """
@media (min-width: 769px) and (max-width: 1366px) {
    /* Tablet: card overlay at top of row — no JS required for width/position. */
    .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    .stMarkdown .full-results-wrap:has(.hl-tip-cb:checked) {
        overflow: visible !important;
    }
    .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
        position: relative !important;
        z-index: 100003 !important;
        overflow: visible !important;
    }
    .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) td {
        position: static !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) {
        position: static !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        display: flex !important;
        flex-direction: column !important;
        position: fixed !important;
        top: var(--hl-fixed-top, 0.75rem) !important;
        left: var(--hl-fixed-left, 0.75rem) !important;
        right: auto !important;
        bottom: auto !important;
        width: var(--hl-fixed-width, 40vw) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, 40vw) !important;
        height: auto !important;
        max-height: var(--hl-fixed-max-height, calc(100dvh - 1.5rem)) !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        touch-action: auto !important;
        text-align: left !important;
        transform: none !important;
        position-anchor: none !important;
        anchor-name: none !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        z-index: 100002 !important;
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 14px !important;
        box-sizing: border-box !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        flex-shrink: 0 !important;
        display: block !important;
        visibility: visible !important;
        position: relative !important;
        z-index: 2 !important;
        text-align: left !important;
        color: #ffffff !important;
        padding: 0.55rem 0.75rem !important;
        font-size: calc(1rem + 4pt) !important;
        font-weight: 700 !important;
        line-height: 1.2 !important;
        background: #1e1e2f !important;
        border-bottom: 1px solid #334155 !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-width: 0 !important;
        min-height: 0 !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
        overscroll-behavior-y: contain !important;
    }
}
"""

_RESPONSIVE_SIDEBAR_JS = """
(() => {
    /* 744px = iPad Mini portrait; overlay sidebar through tablet/hub range. */
    const TABLET_MIN = 744;
    const TABLET_MAX = 1366;
    const isSurfaceDuoViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        return (
            w === 540 ||
            (w === 720 && h <= 541) ||
            (w >= 1110 && w <= 1118 && h <= 741)
        );
    };
    const isIpad14ProMaxViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        return (
            (w >= 1028 && w <= 1036 && h >= 1370) ||
            (w >= 1370 && w <= 1382 && h <= 1040)
        );
    };
    const isResponsiveViewport = () =>
        isSurfaceDuoViewport() ||
        isIpad14ProMaxViewport() ||
        (window.innerWidth >= TABLET_MIN && window.innerWidth <= TABLET_MAX);

    const collapseSidebar = () => {
        const selectors = [
            '[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button',
            '[data-testid="stHeader"] [data-testid="stSidebarCollapseButton"]',
            'section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button',
            '[data-testid="stSidebarCollapseButton"] button',
            '[data-testid="stSidebarCollapseButton"]',
            '[data-testid="collapsedControl"] button',
            '[data-testid="collapsedControl"]',
        ];
        for (const selector of selectors) {
            const node = document.querySelector(selector);
            if (node) {
                node.click();
                return true;
            }
        }
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            sidebar.setAttribute("aria-expanded", "false");
            return true;
        }
        return false;
    };

    const removeLegacyCloseButton = () => {
        document.getElementById("scoop-responsive-sidebar-close")?.remove();
        document.querySelectorAll(".scoop-responsive-sidebar-close").forEach((node) => {
            if (node.id !== "scoop-responsive-sidebar-close") {
                return;
            }
            node.remove();
        });
    };

    const shouldCloseSidebar = (event) => {
        if (!isResponsiveViewport()) {
            return false;
        }
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "true") {
            return false;
        }
        if (event.target.closest('[data-testid="stSidebarBackdrop"]')) {
            return true;
        }
        if (event.target.closest('section[data-testid="stSidebar"]')) {
            return false;
        }
        if (event.target.closest('[data-testid="stHeader"]')) {
            return false;
        }
        return event.target.closest('[data-testid="stAppViewContainer"]') != null;
    };

    if (window.__scoopResponsiveSidebarBound) {
        return;
    }
    window.__scoopResponsiveSidebarBound = true;
    removeLegacyCloseButton();

    document.addEventListener(
        "click",
        (event) => {
            if (shouldCloseSidebar(event)) {
                collapseSidebar();
            }
        },
        true
    );

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && isResponsiveViewport()) {
            collapseSidebar();
        }
    });

    let tabletBootstrapped = false;
    const ensureInitialTabletCollapse = () => {
        if (!isResponsiveViewport() || tabletBootstrapped) {
            return;
        }
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "true") {
            tabletBootstrapped = true;
            removeLegacyCloseButton();
            return;
        }
        if (collapseSidebar()) {
            tabletBootstrapped = true;
            removeLegacyCloseButton();
        }
    };

    ensureInitialTabletCollapse();
    requestAnimationFrame(() => {
        ensureInitialTabletCollapse();
        removeLegacyCloseButton();
    });
    setTimeout(() => {
        ensureInitialTabletCollapse();
        removeLegacyCloseButton();
    }, 100);
    setTimeout(() => {
        ensureInitialTabletCollapse();
        removeLegacyCloseButton();
    }, 400);
})();
"""

_TOOLTIP_SCROLL_JS = """
(() => {
    const root = document.documentElement;
    const className = "scoop-tooltip-scrolling";
    const DESKTOP_MIN = 1367;
    const RESPONSIVE_MIN = 769;
    const RESPONSIVE_MAX = 1366;
    const VIEWPORT_PAD = 12;
    const GAP = 10;
    const HEADLINES_DESKTOP_OFFSET = 12;
    const DESKTOP_HEADLINES_MIN_WIDTH = 320;

    if (!window.__scoopDesktopHeadlinesHideTimers) {
        window.__scoopDesktopHeadlinesHideTimers = new WeakMap();
    }
    window.__scoopDesktopHeadlinesSyncing = false;

    const isResponsiveHeadlinesViewport = () =>
        window.innerWidth >= RESPONSIVE_MIN && window.innerWidth <= RESPONSIVE_MAX;

    const isInsideDesktopHeadlinesPopup = (node) => {
        if (window.innerWidth < DESKTOP_MIN || !node || !node.closest) {
            return false;
        }
        return !!node.closest(
            ".full-results-wrap .tip-wrap.headlines-tip .tip-text, .full-results-wrap .tip-wrap.headlines-tip .headlines-tip-scroll"
        );
    };

    const isDesktopHeadlinesSessionOpen = () =>
        window.innerWidth >= DESKTOP_MIN &&
        !!document.querySelector(
            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
        );

    const lockDesktopHeadlinesPageScroll = () => {};
    const unlockDesktopHeadlinesPageScroll = () => {};

    const getDesktopHeadlinesScrollContainer = (wrap) => {
        if (!wrap) {
            return null;
        }
        return wrap.querySelector(":scope > .tip-text > .headlines-tip-scroll");
    };

    const applyDesktopHeadlinesScrollStyles = (wrap) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const heading = tip?.querySelector(".hl-tip-heading");
        if (!tip || !scroll) {
            return;
        }
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("overflow", "hidden", "important");
        scroll.style.setProperty("flex", "1 1 0", "important");
        scroll.style.setProperty("min-height", "0", "important");
        scroll.style.setProperty("overflow-x", "hidden", "important");
        scroll.style.setProperty("overflow-y", "scroll", "important");
        scroll.style.setProperty("-webkit-overflow-scrolling", "touch", "important");
        scroll.style.setProperty("pointer-events", "auto", "important");
        scroll.style.setProperty("touch-action", "pan-y", "important");

        const tipStyles = getComputedStyle(tip);
        const tipBorderY =
            (parseFloat(tipStyles.borderTopWidth) || 0) +
            (parseFloat(tipStyles.borderBottomWidth) || 0);
        const headingHeight = heading ? heading.offsetHeight : 0;
        const scrollHeight = Math.max(80, tip.clientHeight - headingHeight - tipBorderY);
        scroll.style.setProperty("height", `${scrollHeight}px`, "important");
        scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
    };

    const hideTooltips = (event) => {
        if (isDesktopHeadlinesSessionOpen()) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (event && getDesktopHeadlinesScrollEl(event.target)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        if (event && isInsideDesktopHeadlinesPopup(event.target)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        root.classList.add(className);
        document.body.classList.add(className);
    };
    const allowTooltip = (event) => {
        if (isDesktopHeadlinesSessionOpen()) {
            root.classList.remove(className);
            document.body.classList.remove(className);
            return;
        }
        const element = event.target;
        if (!element || !element.closest) {
            return;
        }
        if (element.closest(".tip-wrap:not(.headlines-tip)")) {
            root.classList.remove(className);
            document.body.classList.remove(className);
        }
        if (isInsideDesktopHeadlinesPopup(element)) {
            root.classList.remove(className);
            document.body.classList.remove(className);
        }
    };

    const isDesktopHeadlinesWrap = (node) => {
        if (!node || !node.closest) {
            return null;
        }
        return node.closest(".full-results-wrap .tip-wrap.headlines-tip");
    };

    const ensureDesktopHeadlinesVisible = (wrap) => {
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        tip.style.setProperty("visibility", "visible", "important");
        tip.style.setProperty("opacity", "1", "important");
        tip.style.setProperty("pointer-events", "auto", "important");
    };

    const clearHeadlinesPosition = (wrap) => {
        if (wrap) {
            wrap.classList.remove("hl-tip-desktop-open");
            const timerId = window.__scoopDesktopHeadlinesHideTimers?.get(wrap);
            if (timerId) {
                window.clearTimeout(timerId);
                window.__scoopDesktopHeadlinesHideTimers.delete(wrap);
            }
        }
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        tip.style.removeProperty("--hl-fixed-top");
        tip.style.removeProperty("--hl-fixed-left");
        tip.style.removeProperty("--hl-fixed-width");
        tip.style.removeProperty("--hl-fixed-max-height");
        tip.style.removeProperty("--hl-fixed-height");
        tip.style.removeProperty("height");
        tip.style.removeProperty("position-anchor");
        tip.style.removeProperty("visibility");
        tip.style.removeProperty("opacity");
        tip.style.removeProperty("pointer-events");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        if (scroll) {
            scroll.scrollTop = 0;
            scroll.style.removeProperty("flex");
            scroll.style.removeProperty("min-height");
            scroll.style.removeProperty("overflow-x");
            scroll.style.removeProperty("overflow-y");
            scroll.style.removeProperty("-webkit-overflow-scrolling");
            scroll.style.removeProperty("pointer-events");
            scroll.style.removeProperty("touch-action");
            scroll.style.removeProperty("height");
            scroll.style.removeProperty("max-height");
            scroll.style.removeProperty("--hl-scroll-max-height");
            scroll.style.removeProperty("--hl-scroll-overflow-y");
        }
        tip.style.removeProperty("display");
        tip.style.removeProperty("flex-direction");
        tip.style.removeProperty("overflow");
        unbindDesktopHeadlinesScrollWheel(wrap);
    };

    const measureDesktopHeadlinesContentHeight = (tip) => {
        const heading = tip.querySelector(".hl-tip-heading");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const headingHeight = heading ? heading.offsetHeight : 0;
        if (!scroll) {
            return headingHeight;
        }
        const list = scroll.querySelector(".headlines-tip-list");
        const styles = getComputedStyle(scroll);
        const scrollPadding =
            (parseFloat(styles.paddingTop) || 0) + (parseFloat(styles.paddingBottom) || 0);
        const listHeight = list ? list.scrollHeight : scroll.scrollHeight;
        return headingHeight + listHeight + scrollPadding;
    };

    const fitDesktopHeadlinesTip = (tip, slot) => {
        if (!tip || !slot) {
            return;
        }
        const scroll = tip.querySelector(".headlines-tip-scroll");
        const maxHeight = slot.maxHeight;

        tip.style.removeProperty("height");
        tip.style.removeProperty("--hl-fixed-height");
        if (scroll) {
            scroll.scrollTop = 0;
            scroll.style.removeProperty("height");
            scroll.style.removeProperty("max-height");
            scroll.style.removeProperty("overflow-y");
            scroll.style.removeProperty("--hl-scroll-max-height");
            scroll.style.removeProperty("--hl-scroll-overflow-y");
        }

        tip.style.height = "auto";
        const contentHeight = Math.max(tip.scrollHeight, measureDesktopHeadlinesContentHeight(tip));
        const tipStyles = getComputedStyle(tip);
        const tipBorderY =
            (parseFloat(tipStyles.borderTopWidth) || 0) +
            (parseFloat(tipStyles.borderBottomWidth) || 0);
        const usableMaxHeight = Math.max(120, maxHeight - tipBorderY);
        const tipHeight = Math.min(contentHeight, usableMaxHeight);

        tip.style.setProperty("--hl-fixed-height", `${tipHeight}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${maxHeight}px`);
        tip.style.setProperty("height", `${tipHeight}px`);
    };

    const bindDesktopHeadlinesScrollWheel = (wrap) => {
        if (window.innerWidth < DESKTOP_MIN || !wrap) {
            return;
        }
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        if (!scroll) {
            return;
        }
        if (scroll.__hlWheelHandler) {
            scroll.removeEventListener("wheel", scroll.__hlWheelHandler, true);
        }
        scroll.__hlWheelHandler = (event) => {
            scrollDesktopHeadlinesFromWheel(event, scroll);
        };
        scroll.addEventListener("wheel", scroll.__hlWheelHandler, { passive: false, capture: true });
    };

    const unbindDesktopHeadlinesScrollWheel = (wrap) => {
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        if (scroll?.__hlWheelHandler) {
            scroll.removeEventListener("wheel", scroll.__hlWheelHandler, true);
            delete scroll.__hlWheelHandler;
        }
    };

    const getFullResultsTableRect = () => {
        const table = document.querySelector(".full-results-wrap .full-results-table");
        return table ? table.getBoundingClientRect() : null;
    };

    const getTableHeaderColumnRect = (pattern) => {
        const header = [...document.querySelectorAll(".full-results-wrap .full-results-table thead th")].find(
            (th) => pattern.test((th.textContent || "").trim())
        );
        return header ? header.getBoundingClientRect() : null;
    };

    const getHeadlinesColumnRect = () => {
        return getTableHeaderColumnRect(/Headlines/i);
    };

    const getDesktopHeadlinesPanelRect = () => {
        const marketMood = getTableHeaderColumnRect(/Market\\s*Mood/i);
        const headlineSentiment = getTableHeaderColumnRect(/Headline\\s*Sentiment/i);
        if (marketMood && headlineSentiment) {
            const left = Math.min(marketMood.left, headlineSentiment.left);
            const right = Math.max(marketMood.right, headlineSentiment.right);
            return {
                left,
                right,
                width: Math.max(DESKTOP_HEADLINES_MIN_WIDTH, right - left),
            };
        }

        const headlinesCol = getHeadlinesColumnRect();
        if (headlinesCol) {
            const width = Math.max(280, headlinesCol.width * 2.5);
            const left = headlinesCol.right + HEADLINES_DESKTOP_OFFSET;
            return { left, right: left + width, width };
        }

        return null;
    };

    const getDesktopHeadlinesSlot = () => {
        const viewLeft = VIEWPORT_PAD;
        const viewRight = window.innerWidth - VIEWPORT_PAD;
        const rootSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;

        const tableRect = getFullResultsTableRect();
        let top = VIEWPORT_PAD;
        let maxHeight = Math.max(200, window.innerHeight - VIEWPORT_PAD * 2);

        if (tableRect && tableRect.height > 0) {
            const viewportTop = VIEWPORT_PAD;
            const viewportBottom = window.innerHeight - VIEWPORT_PAD;
            const visibleTop = Math.max(tableRect.top, viewportTop);
            const visibleBottom = Math.min(tableRect.bottom, viewportBottom);
            top = Math.round(visibleTop);
            maxHeight = Math.max(160, Math.round(visibleBottom - visibleTop));
        }

        let left = viewLeft;
        let width = Math.round(
            Math.min(viewRight - viewLeft, Math.max(280, Math.min(21 * rootSize, window.innerWidth * 0.36)))
        );

        const panelRect = getDesktopHeadlinesPanelRect();
        if (panelRect && panelRect.width > 0) {
            left = Math.round(panelRect.left);
            width = Math.round(panelRect.width);
        }

        if (left > viewRight - DESKTOP_HEADLINES_MIN_WIDTH) {
            left = Math.max(viewLeft, viewRight - width);
        }
        if (left + width > viewRight) {
            left = Math.max(viewLeft, viewRight - width);
        }
        if (left < viewLeft) {
            left = viewLeft;
        }
        width = Math.min(Math.max(DESKTOP_HEADLINES_MIN_WIDTH, width), viewRight - left);

        return {
            top,
            left: Math.round(left),
            width: Math.round(width),
            maxHeight: Math.round(maxHeight),
            tableBottom: tableRect ? Math.round(tableRect.bottom) : null,
        };
    };

    const positionDesktopHeadlinesTip = (wrap, preserveScroll = false) => {
        if (window.innerWidth < DESKTOP_MIN || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const prevScrollTop = preserveScroll && scroll ? scroll.scrollTop : 0;

        tip.style.setProperty("position-anchor", "none");

        const slot = getDesktopHeadlinesSlot();

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.removeProperty("height");

        if (!preserveScroll && scroll) {
            scroll.scrollTop = 0;
        }
        fitDesktopHeadlinesTip(tip, slot);
        applyDesktopHeadlinesScrollStyles(wrap);
        if (preserveScroll && scroll) {
            scroll.scrollTop = prevScrollTop;
        }
        if (wrap.classList.contains("hl-tip-desktop-open")) {
            ensureDesktopHeadlinesVisible(wrap);
            bindDesktopHeadlinesScrollWheel(wrap);
        }
    };

    const scheduleDesktopHeadlinesPosition = (wrap, preserveScroll = false) => {
        positionDesktopHeadlinesTip(wrap, preserveScroll);
        window.requestAnimationFrame(() => {
            const tip = wrap && wrap.querySelector(":scope > .tip-text");
            if (!tip) {
                return;
            }
            positionDesktopHeadlinesTip(wrap, preserveScroll);
            fitDesktopHeadlinesTip(tip, getDesktopHeadlinesSlot());
            applyDesktopHeadlinesScrollStyles(wrap);
            if (wrap.classList.contains("hl-tip-desktop-open")) {
                ensureDesktopHeadlinesVisible(wrap);
                bindDesktopHeadlinesScrollWheel(wrap);
            }
        });
    };

    const resolveDesktopHeadlinesWrap = (node) => {
        if (!node || !node.closest) {
            return null;
        }
        return node.closest(".full-results-wrap .tip-wrap.headlines-tip");
    };

    const getDesktopHeadlinesScrollEl = (node, event) => {
        if (window.innerWidth < DESKTOP_MIN) {
            return null;
        }
        let target = node;
        if (event && Number.isFinite(event.clientX) && Number.isFinite(event.clientY)) {
            const hit = document.elementFromPoint(event.clientX, event.clientY);
            if (hit) {
                target = hit;
            }
        }
        if (!target || !target.closest) {
            return null;
        }
        const wrap = target.closest(
            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
        );
        if (!wrap) {
            return null;
        }
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        if (!scroll) {
            return null;
        }
        if (target.closest(".tip-text") && wrap.contains(target.closest(".tip-text"))) {
            return scroll;
        }
        return null;
    };

    const cancelDesktopHeadlinesHide = (wrap) => {
        if (!wrap || !window.__scoopDesktopHeadlinesHideTimers) {
            return;
        }
        const timerId = window.__scoopDesktopHeadlinesHideTimers.get(wrap);
        if (timerId) {
            window.clearTimeout(timerId);
            window.__scoopDesktopHeadlinesHideTimers.delete(wrap);
        }
    };

    const hideDesktopHeadlines = (wrap) => {
        if (!wrap) {
            return;
        }
        cancelDesktopHeadlinesHide(wrap);
        wrap.classList.remove("hl-tip-desktop-open");
        clearHeadlinesPosition(wrap);
    };

    const showDesktopHeadlines = (wrap) => {
        if (window.innerWidth < DESKTOP_MIN || !wrap) {
            return;
        }
        cancelDesktopHeadlinesHide(wrap);
        wrap.classList.add("hl-tip-desktop-open");
        root.classList.remove(className);
        document.body.classList.remove(className);
        ensureDesktopHeadlinesVisible(wrap);
        scheduleDesktopHeadlinesPosition(wrap, false);
    };

    const closeOtherDesktopHeadlines = (activeCheckbox) => {
        window.__scoopDesktopHeadlinesSyncing = true;
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                if (checkbox === activeCheckbox) {
                    return;
                }
                checkbox.checked = false;
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    hideDesktopHeadlines(wrap);
                }
            });
        window.__scoopDesktopHeadlinesSyncing = false;
    };

    const handleDesktopHeadlinesChange = (checkbox) => {
        if (window.innerWidth < DESKTOP_MIN || !checkbox) {
            return;
        }
        const wrap = checkbox.closest(".tip-wrap.headlines-tip");
        if (!wrap) {
            return;
        }
        if (window.__scoopDesktopHeadlinesSyncing) {
            return;
        }
        if (checkbox.checked) {
            closeOtherDesktopHeadlines(checkbox);
            showDesktopHeadlines(wrap);
            return;
        }
        hideDesktopHeadlines(wrap);
    };

    const handleHeadlinesCheckboxChange = (event) => {
        const checkbox = event.target;
        if (!checkbox || !checkbox.classList || !checkbox.classList.contains("hl-tip-cb")) {
            return;
        }
        const wrap = checkbox.closest(".tip-wrap.headlines-tip");
        if (!wrap) {
            return;
        }
        if (window.innerWidth >= DESKTOP_MIN) {
            handleDesktopHeadlinesChange(checkbox);
            return;
        }
        if (checkbox.checked) {
            scheduleResponsiveHeadlinesPosition(wrap);
        } else {
            clearHeadlinesPosition(wrap);
        }
    };

    const scrollDesktopHeadlinesFromWheel = (event, scrollEl) => {
        if (window.innerWidth < DESKTOP_MIN || !scrollEl) {
            return false;
        }
        const maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
        if (maxScroll <= 0) {
            return false;
        }
        const delta = event.deltaY;
        if (!delta) {
            return false;
        }
        event.preventDefault();
        event.stopPropagation();
        scrollEl.scrollTop = Math.max(0, Math.min(maxScroll, scrollEl.scrollTop + delta));
        return true;
    };

    const handleDesktopHeadlinesWheel = (event) => {
        if (window.innerWidth < DESKTOP_MIN) {
            return;
        }
        if (!isDesktopHeadlinesSessionOpen()) {
            return;
        }
        const scrollEl = getDesktopHeadlinesScrollEl(event.target, event);
        if (!scrollEl) {
            return;
        }
        scrollDesktopHeadlinesFromWheel(event, scrollEl);
    };

    const repositionOpenDesktopHeadlines = () => {
        if (window.innerWidth < DESKTOP_MIN) {
            return;
        }
        document
            .querySelectorAll(
                ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
            )
            .forEach((wrap) => scheduleDesktopHeadlinesPosition(wrap, true));
    };

    /* Refresh on every Streamlit rerun — listeners are bound once below. */
    window.__scoopDesktopHeadlinesApi = {
        clearHeadlinesPosition,
        fitDesktopHeadlinesTip,
        getDesktopHeadlinesSlot,
        positionDesktopHeadlinesTip,
        scheduleDesktopHeadlinesPosition,
        repositionOpenDesktopHeadlines,
        showDesktopHeadlines,
        hideDesktopHeadlines,
        cancelDesktopHeadlinesHide,
        ensureDesktopHeadlinesVisible,
        handleDesktopHeadlinesChange,
        handleHeadlinesCheckboxChange,
        handleDesktopHeadlinesWheel,
        scrollDesktopHeadlinesFromWheel,
        getDesktopHeadlinesScrollEl,
        getDesktopHeadlinesScrollContainer,
        applyDesktopHeadlinesScrollStyles,
        bindDesktopHeadlinesScrollWheel,
        unbindDesktopHeadlinesScrollWheel,
    };

    const getResponsiveHeadlinesSlot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const viewRight = window.innerWidth - VIEWPORT_PAD;

        const top = Math.round(headerBottom + VIEWPORT_PAD);
        const maxHeight = Math.max(200, window.innerHeight - top - VIEWPORT_PAD);

        let viewLeft = VIEWPORT_PAD;
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            const sidebarRight = sidebar.getBoundingClientRect().right;
            viewLeft = Math.max(VIEWPORT_PAD, Math.round(sidebarRight + VIEWPORT_PAD));
        }

        const content =
            document.querySelector(".full-results-wrap") ||
            document.querySelector('[data-testid="stMainBlockContainer"]') ||
            document.querySelector('[data-testid="stAppViewContainer"]');

        let left = viewLeft;
        if (content) {
            left = Math.max(viewLeft, content.getBoundingClientRect().left);
        }

        const availableWidth = viewRight - left;
        const width = Math.round(
            Math.min(availableWidth, Math.max(280, window.innerWidth * 0.4))
        );

        if (left + width > viewRight) {
            left = Math.max(viewLeft, viewRight - width);
        }

        return {
            top,
            left: Math.round(left),
            width,
            maxHeight: Math.round(maxHeight),
        };
    };

    const positionResponsiveHeadlinesTip = (wrap) => {
        if (!isResponsiveHeadlinesViewport() || !wrap) {
            return;
        }
        const checkbox = wrap.querySelector(".hl-tip-cb");
        if (!checkbox || !checkbox.checked) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }

        const slot = getResponsiveHeadlinesSlot();

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);

        const scroll = tip.querySelector(".headlines-tip-scroll");
        if (scroll) {
            scroll.scrollTop = 0;
        }
    };

    const scheduleResponsiveHeadlinesPosition = (wrap) => {
        positionResponsiveHeadlinesTip(wrap);
        window.requestAnimationFrame(() => positionResponsiveHeadlinesTip(wrap));
    };

    const repositionOpenResponsiveHeadlines = () => {
        if (!isResponsiveHeadlinesViewport()) {
            return;
        }
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    scheduleResponsiveHeadlinesPosition(wrap);
                }
            });
    };

    if (!window.__scoopTooltipScrollBound) {
        window.__scoopTooltipScrollBound = true;

        window.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
        document.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
        document.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
        document.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
    }

    if (window.__scoopDesktopHeadlinesBindVersion !== 15) {
        window.__scoopDesktopHeadlinesBindVersion = 15;

        if (window.__scoopDesktopHeadlinesMouseLeave) {
            document.removeEventListener("mouseleave", window.__scoopDesktopHeadlinesMouseLeave, true);
        }
        if (window.__scoopDesktopHeadlinesMouseOut) {
            document.removeEventListener("mouseout", window.__scoopDesktopHeadlinesMouseOut, true);
        }
        if (window.__scoopDesktopHeadlinesMouseOver) {
            document.removeEventListener("mouseover", window.__scoopDesktopHeadlinesMouseOver, true);
        }
        if (window.__scoopDesktopHeadlinesPointerMove) {
            document.removeEventListener("pointermove", window.__scoopDesktopHeadlinesPointerMove, true);
        }
        if (window.__scoopDesktopHeadlinesWheel) {
            document.removeEventListener("wheel", window.__scoopDesktopHeadlinesWheel, true);
            document.removeEventListener("wheel", window.__scoopDesktopHeadlinesWheel, false);
        }
        if (window.__scoopDesktopHeadlinesResize) {
            window.removeEventListener("resize", window.__scoopDesktopHeadlinesResize);
        }
        if (window.__scoopDesktopHeadlinesWindowScroll) {
            window.removeEventListener("scroll", window.__scoopDesktopHeadlinesWindowScroll, true);
        }
        if (window.__scoopDesktopHeadlinesDocScroll) {
            document.removeEventListener("scroll", window.__scoopDesktopHeadlinesDocScroll, true);
        }

        window.__scoopDesktopHeadlinesWheel = (event) => {
            window.__scoopDesktopHeadlinesApi?.handleDesktopHeadlinesWheel(event);
        };

        window.__scoopDesktopHeadlinesResize = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            repositionOpenResponsiveHeadlines();
        };

        window.__scoopDesktopHeadlinesWindowScroll = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
        };

        window.__scoopDesktopHeadlinesDocScroll = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
        };

        window.addEventListener("resize", window.__scoopDesktopHeadlinesResize);
        window.addEventListener("scroll", window.__scoopDesktopHeadlinesWindowScroll, {
            passive: true,
            capture: true,
        });
        document.addEventListener("scroll", window.__scoopDesktopHeadlinesDocScroll, {
            passive: true,
            capture: true,
        });
        document.addEventListener("wheel", window.__scoopDesktopHeadlinesWheel, {
            passive: false,
            capture: true,
        });
    }

    if (!window.__scoopResponsiveHeadlinesBound) {
        window.__scoopResponsiveHeadlinesBound = true;

        document.addEventListener(
            "change",
            (event) => {
                window.__scoopDesktopHeadlinesApi?.handleHeadlinesCheckboxChange(event);
            },
            true
        );

        window.addEventListener("resize", repositionOpenResponsiveHeadlines, { passive: true });

        const sidebarHeadlinesObserver = new MutationObserver(repositionOpenResponsiveHeadlines);
        sidebarHeadlinesObserver.observe(document.documentElement, {
            attributes: true,
            subtree: true,
            attributeFilter: ["aria-expanded"],
        });
    }
})();
"""


_DESKTOP_SIDEBAR_JS = """
(() => {
    const DESKTOP_MIN = 1367;

    const isDesktopViewport = () => window.innerWidth >= DESKTOP_MIN;

    const expandSidebarIfNeeded = () => {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "false") {
            return;
        }
        const expand =
            document.querySelector('[data-testid="stExpandSidebarButton"]') ||
            document.querySelector('[data-testid="collapsedControl"] button') ||
            document.querySelector('[data-testid="collapsedControl"]');
        if (expand) {
            expand.click();
        }
    };

    const ensureDesktopSidebarOpen = () => {
        if (!isDesktopViewport()) {
            return;
        }
        expandSidebarIfNeeded();
    };

    if (window.__scoopDesktopSidebarBound) {
        return;
    }
    window.__scoopDesktopSidebarBound = true;

    ensureDesktopSidebarOpen();
    window.addEventListener("resize", ensureDesktopSidebarOpen);

    document.addEventListener(
        "click",
        (event) => {
            if (!isDesktopViewport()) {
                return;
            }
            const collapseTarget = event.target.closest(
                '[data-testid="stSidebarCollapseButton"], [data-testid="collapsedControl"]'
            );
            if (collapseTarget) {
                event.preventDefault();
                event.stopImmediatePropagation();
            }
        },
        true
    );

    const observer = new MutationObserver(() => {
        ensureDesktopSidebarOpen();
    });
    observer.observe(document.documentElement, {
        attributes: true,
        subtree: true,
        attributeFilter: ["aria-expanded"],
    });
})();
"""

_COMBINED_PAGE_JS = _TOOLTIP_SCROLL_JS + _RESPONSIVE_SIDEBAR_JS + _DESKTOP_SIDEBAR_JS


def install_responsive_sidebar_handler() -> None:
    """Responsive sidebar close (tablet) + always-open sidebar (desktop)."""
    st.html(
        f"<script>{_RESPONSIVE_SIDEBAR_JS}</script>"
        f"<script>{_DESKTOP_SIDEBAR_JS}</script>",
        unsafe_allow_javascript=True,
    )


def install_tooltip_scroll_handler() -> None:
    """Inject mobile headline CSS; HTML backdrop label closes panel on outside tap."""
    st.html(
        f"<style id='scoop-mobile-headlines-css'>{_MOBILE_HEADLINES_CSS}</style>"
        f"<style id='scoop-mobile-tablet-card-order-css'>{_MOBILE_TABLET_CARD_ORDER_CSS}</style>"
        f"<style id='scoop-tablet-headlines-css'>{_TABLET_HEADLINES_POPUP_CSS}</style>"
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>"
        f"<script>{_COMBINED_PAGE_JS}</script>",
        unsafe_allow_javascript=True,
    )
