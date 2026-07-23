import sys
from pathlib import Path

import streamlit as st

_ADMIN = Path(__file__).resolve().parent / "admin_tools"
if str(_ADMIN) not in sys.path:
    sys.path.insert(0, str(_ADMIN))

from tablet_mobile_layout_css import MOBILE_HEADLINES_CARD_OVERLAY  # noqa: E402

_MOBILE_HEADLINES_CSS = f"""
@media (max-width: 768px) {{
{MOBILE_HEADLINES_CARD_OVERLAY}
}}
"""

_DESKTOP_HEADLINES_CSS = """
@media (min-width: 1367px) {
    /* Headlines count uses hover on desktop; hide mobile tap checkbox/backdrop. */
    .tip-wrap.headlines-tip .hl-tip-cb,
    .tip-wrap.headlines-tip .hl-tip-backdrop {
        display: none !important;
    }
    .tip-wrap.headlines-tip .hl-tip-count {
        cursor: help !important;
        text-decoration: inherit !important;
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
    const TABLET_MIN = 769;
    const TABLET_MAX = 1366;
    const CLOSE_BTN_ID = "scoop-responsive-sidebar-close";
    const isResponsiveViewport = () =>
        window.innerWidth >= TABLET_MIN && window.innerWidth <= TABLET_MAX;

    const collapseSidebar = () => {
        const selectors = [
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

    const removeCloseButton = () => {
        document.getElementById(CLOSE_BTN_ID)?.remove();
    };

    const syncCloseButton = () => {
        if (!isResponsiveViewport()) {
            removeCloseButton();
            return;
        }
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "true") {
            removeCloseButton();
            return;
        }

        let btn = document.getElementById(CLOSE_BTN_ID);
        if (!btn) {
            btn = document.createElement("button");
            btn.id = CLOSE_BTN_ID;
            btn.type = "button";
            btn.className = "scoop-responsive-sidebar-close";
            btn.setAttribute("aria-label", "Close menu");
            btn.textContent = "\u00AB";
            btn.addEventListener(
                "click",
                (event) => {
                    event.preventDefault();
                    event.stopPropagation();
                    collapseSidebar();
                    removeCloseButton();
                },
                true
            );
            document.body.appendChild(btn);
        }

        const rect = sidebar.getBoundingClientRect();
        btn.style.top = `${Math.round(rect.top + 10)}px`;
        btn.style.left = `${Math.round(rect.left + 10)}px`;
    };

    const shouldCloseSidebar = (event) => {
        if (!isResponsiveViewport()) {
            return false;
        }
        if (event.target.closest(`#${CLOSE_BTN_ID}, .scoop-responsive-sidebar-close`)) {
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

    document.addEventListener(
        "click",
        (event) => {
            if (shouldCloseSidebar(event)) {
                collapseSidebar();
                removeCloseButton();
            }
        },
        true
    );

    document.addEventListener("keydown", (event) => {
        if (event.key === "Escape" && isResponsiveViewport()) {
            collapseSidebar();
            removeCloseButton();
        }
    });

    window.addEventListener("resize", syncCloseButton);
    window.addEventListener("scroll", syncCloseButton, { passive: true, capture: true });

    const observer = new MutationObserver(syncCloseButton);
    observer.observe(document.documentElement, {
        attributes: true,
        subtree: true,
        attributeFilter: ["aria-expanded"],
    });

    syncCloseButton();
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

    const isResponsiveHeadlinesViewport = () =>
        window.innerWidth >= RESPONSIVE_MIN && window.innerWidth <= RESPONSIVE_MAX;

    const hideTooltips = () => {
        root.classList.add(className);
        document.body.classList.add(className);
    };
    const allowTooltip = (event) => {
        const element = event.target;
        if (element && element.closest && element.closest(".tip-wrap:not(.headlines-tip)")) {
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

    const clearHeadlinesPosition = (wrap) => {
        const tip = wrap && wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        tip.style.removeProperty("--hl-fixed-top");
        tip.style.removeProperty("--hl-fixed-left");
        tip.style.removeProperty("--hl-fixed-width");
        tip.style.removeProperty("--hl-fixed-max-height");
        const scroll = tip.querySelector(".headlines-tip-scroll");
        if (scroll) {
            scroll.scrollTop = 0;
        }
    };

    const positionDesktopHeadlinesTip = (wrap) => {
        if (window.innerWidth < DESKTOP_MIN || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        const trigger = wrap.querySelector(".hl-tip-count") || wrap;
        if (!tip || !trigger) {
            return;
        }

        tip.style.setProperty("--hl-fixed-top", "0.75rem");
        tip.style.setProperty("--hl-fixed-left", "0.75rem");

        const triggerRect = trigger.getBoundingClientRect();
        const tipRect = tip.getBoundingClientRect();
        const tipWidth = tipRect.width || tip.offsetWidth;
        const tipHeight = tipRect.height || tip.offsetHeight;
        const viewBottom = window.innerHeight - VIEWPORT_PAD;
        const viewRight = window.innerWidth - VIEWPORT_PAD;

        let top = triggerRect.top - tipHeight - GAP;
        if (top < VIEWPORT_PAD) {
            top = VIEWPORT_PAD;
        }
        if (top + tipHeight > viewBottom) {
            top = Math.max(VIEWPORT_PAD, viewBottom - tipHeight);
        }

        let left = triggerRect.right - tipWidth;
        if (left < VIEWPORT_PAD) {
            left = VIEWPORT_PAD;
        }
        if (left + tipWidth > viewRight) {
            left = Math.max(VIEWPORT_PAD, viewRight - tipWidth);
        }

        tip.style.setProperty("--hl-fixed-top", `${Math.round(top)}px`);
        tip.style.setProperty("--hl-fixed-left", `${Math.round(left)}px`);
    };

    const scheduleDesktopHeadlinesPosition = (wrap) => {
        positionDesktopHeadlinesTip(wrap);
        window.requestAnimationFrame(() => positionDesktopHeadlinesTip(wrap));
    };

    const getResponsiveHeadlinesSlot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const viewRight = window.innerWidth - VIEWPORT_PAD;

        const top = Math.round(headerBottom + VIEWPORT_PAD);
        const maxHeight = Math.max(200, window.innerHeight - top - VIEWPORT_PAD);
        const width = Math.round(
            Math.min(viewRight - VIEWPORT_PAD, Math.max(280, window.innerWidth * 0.4))
        );

        const content =
            document.querySelector(".full-results-wrap") ||
            document.querySelector('[data-testid="stMainBlockContainer"]') ||
            document.querySelector('[data-testid="stAppViewContainer"]');

        let left = VIEWPORT_PAD;
        if (content) {
            left = Math.max(VIEWPORT_PAD, content.getBoundingClientRect().left);
        }
        if (left + width > viewRight) {
            left = Math.max(VIEWPORT_PAD, viewRight - width);
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

    if (!window.__scoopDesktopHeadlinesBound) {
        window.__scoopDesktopHeadlinesBound = true;

        document.addEventListener(
            "mouseleave",
            (event) => {
                const wrap = isDesktopHeadlinesWrap(event.target);
                if (!wrap) {
                    return;
                }
                const related = event.relatedTarget;
                if (related && wrap.contains(related)) {
                    return;
                }
                clearHeadlinesPosition(wrap);
            },
            true
        );

        document.addEventListener(
            "mouseover",
            (event) => {
                const wrap = isDesktopHeadlinesWrap(event.target);
                if (!wrap) {
                    return;
                }
                scheduleDesktopHeadlinesPosition(wrap);
            },
            true
        );

        window.addEventListener("resize", () => {
            document
                .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip:hover")
                .forEach((wrap) => scheduleDesktopHeadlinesPosition(wrap));
            repositionOpenResponsiveHeadlines();
        });
    }

    if (!window.__scoopResponsiveHeadlinesBound) {
        window.__scoopResponsiveHeadlinesBound = true;

        document.addEventListener(
            "change",
            (event) => {
                const checkbox = event.target;
                if (!checkbox || !checkbox.classList || !checkbox.classList.contains("hl-tip-cb")) {
                    return;
                }
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (!wrap) {
                    return;
                }
                if (checkbox.checked) {
                    scheduleResponsiveHeadlinesPosition(wrap);
                } else {
                    clearHeadlinesPosition(wrap);
                }
            },
            true
        );

        window.addEventListener("resize", repositionOpenResponsiveHeadlines, { passive: true });
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
        f"<style id='scoop-tablet-headlines-css'>{_TABLET_HEADLINES_POPUP_CSS}</style>"
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>"
        f"<script>{_COMBINED_PAGE_JS}</script>",
        unsafe_allow_javascript=True,
    )
