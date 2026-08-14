import json

import streamlit as st

from admin_tools.tablet_mobile_layout_css import (
    DESKTOP_SIDEBAR_LAYOUT,
    DESKTOP_ZOOM_LAYOUT,
    MOBILE_CARD_FIELD_ORDER,
    MOBILE_HEADLINES_CARD_OVERLAY,
    RESPONSIVE_GENERIC_TOOLTIP_LAYOUT,
    RESPONSIVE_SIDEBAR_BOOTSTRAP,
    SIDEBAR_NAV_COMPACT,
)

_MOBILE_HEADLINES_CSS = f"""
@media (max-width: 768px) {{
{MOBILE_HEADLINES_CARD_OVERLAY}
}}
"""

_MOBILE_PHONE_HEADLINES_FIXED_CSS = """
@media (max-width: 743px) {
    /* Phone mobile: fixed slot below Deploy bar; reserve bottom space for backdrop tap. */
    .stMarkdown .full-results-wrap .full-results-table tbody tr:has(.hl-tip-cb:checked) {
        position: static !important;
        z-index: auto !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        position: fixed !important;
        top: var(--hl-fixed-top, 20px) !important;
        left: var(--hl-fixed-left, 0.75rem) !important;
        right: auto !important;
        bottom: auto !important;
        width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        min-width: 0 !important;
        max-width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        height: auto !important;
        max-height: var(--hl-fixed-max-height, 75dvh) !important;
        display: flex !important;
        flex-direction: column !important;
        overflow: hidden !important;
        transform: none !important;
        position-anchor: none !important;
        anchor-name: none !important;
        z-index: 100002 !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        position: fixed !important;
        top: var(--hl-fixed-top, 20px) !important;
        left: var(--hl-fixed-left, 0.75rem) !important;
        width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        max-width: var(--hl-fixed-width, calc(100vw - 1.5rem)) !important;
        box-sizing: border-box !important;
        z-index: 100003 !important;
        flex: 0 0 auto !important;
        flex-shrink: 0 !important;
        display: block !important;
        visibility: visible !important;
        opacity: 1 !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
        color: #ffffff !important;
        background: #1e1e2f !important;
        border: 1px solid #334155 !important;
        border-bottom: 1px solid #334155 !important;
        border-radius: 14px 14px 0 0 !important;
        padding: 0.45rem 0.6rem !important;
        font-size: calc(0.82rem + 4pt) !important;
        font-weight: 700 !important;
        line-height: 1.15 !important;
    }
    html.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading,
    body.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        visibility: visible !important;
        opacity: 1 !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        overflow-y: auto !important;
    }
    html.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text,
    body.scoop-tooltip-scrolling .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }
}
"""

_MOBILE_TABLET_CARD_ORDER_CSS = f"""
@media (max-width: 1366px),
       (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px) {{
{MOBILE_CARD_FIELD_ORDER}
}}
"""

_RESPONSIVE_GENERIC_TOOLTIP_CSS = f"""
@media (max-width: 1366px) {{
{RESPONSIVE_GENERIC_TOOLTIP_LAYOUT}
}}
"""

_DARK_RESPONSIVE_TIP_UNDERLINE_CSS = """
@media (max-width: 1366px) {
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown [data-testid="stMarkdownContainer"] .tip-wrap:not(.headlines-tip),
html[data-scoop-theme="dark"] .stMarkdown div .tip-wrap:not(.headlines-tip) {
    border-bottom: 2px dashed #ffffff !important;
}
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip {
    border-bottom: none !important;
}
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
    border-bottom: 2px dashed #ffffff !important;
    display: inline-block !important;
    text-decoration: none !important;
}
}
"""

_DARK_POPUP_OUTLINE_CSS = """
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap .tip-text,
html[data-scoop-theme="dark"] .tip-wrap .tip-text {
    border: 2px solid #ffffff !important;
}
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text,
html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .tip-text {
    border: 2px solid #ffffff !important;
}
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
    border: 2px solid #ffffff !important;
    border-bottom: 1px solid rgba(255, 255, 255, 0.45) !important;
}
html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll,
html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
    border-left: 2px solid #ffffff !important;
    border-right: 2px solid #ffffff !important;
    border-bottom: 2px solid #ffffff !important;
}
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
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll {
        flex: 1 1 0 !important;
        display: block !important;
        min-height: 0 !important;
        max-height: none !important;
        overflow-x: hidden !important;
        overflow-y: auto !important;
        max-height: var(--hl-scroll-max-height, none) !important;
        overscroll-behavior: contain !important;
        overscroll-behavior-y: contain !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        scrollbar-gutter: auto !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
        padding: 0.65rem 1rem 0.65rem 1rem !important;
    }
    .full-results-wrap .full-results-table tbody .tip-wrap.headlines-tip .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
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
        overflow-y: auto !important;
        max-height: var(--hl-scroll-max-height, none) !important;
        scrollbar-width: none !important;
        scrollbar-gutter: auto !important;
        pointer-events: auto !important;
        touch-action: pan-y !important;
    }
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        display: none !important;
        width: 0 !important;
        height: 0 !important;
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

_TABLET_HEADLINES_POPUP_RULES = """
    /* Tablet / iPad Pro-style headlines popup (fixed slot via --hl-fixed-*). */
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
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
        white-space: normal !important;
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
"""

_TABLET_HEADLINES_POPUP_CSS = f"""
@media (min-width: 769px) and (max-width: 1366px) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_IPAD_MINI_SURFACE_DUO_HEADLINES_CSS = f"""
@media (min-width: 744px) and (max-width: 768px),
       (width: 540px),
       ((width: 720px) and (max-height: 541px)),
       ((min-width: 1110px) and (max-width: 1118px) and (max-height: 741px)) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_ASUS_ZENBOOK_FOLD_HEADLINES_CSS = f"""
@media (min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),
       (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px),
       (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),
       (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),
       (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px) {{
{_TABLET_HEADLINES_POPUP_RULES}
}}
"""

_RESPONSIVE_DOC_HELPER_JS = """
const __scoopGetAppDoc = () => {
    try {
        const parentDoc = window.parent && window.parent.document;
        if (parentDoc && parentDoc.querySelector('[data-testid="stAppViewContainer"]')) {
            return parentDoc;
        }
    } catch (e) {}
    return document;
};
const __scoopGetAppWin = () => __scoopGetAppDoc().defaultView || window;
const __scoopViewportWidth = () => __scoopGetAppWin().innerWidth || window.innerWidth;
const __scoopViewportHeight = () => __scoopGetAppWin().innerHeight || window.innerHeight;
const __scoopIsAnalyzePage = () => {
    try {
        return /Analyze/i.test(__scoopGetAppWin().location.pathname || "");
    } catch (e) {
        return false;
    }
};
"""

_RESPONSIVE_LAYOUT_CORE_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const appWin = __scoopGetAppWin();
    const doc = __scoopGetAppDoc();

    if (appWin.__scoopLayout) {
        return;
    }

    const PHONE_MAX = 743;
    const TABLET_MIN = 744;
    const TABLET_MAX = 1366;
    const DESKTOP_MIN = 1367;
    // Layout viewport floor when browser zoom shrinks CSS width on a physical desktop screen.
    const DESKTOP_ZOOM_MIN = 1024;

    const isPhoneViewport = () => __scoopViewportWidth() <= PHONE_MAX;
    const isSurfaceDuoViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        return (
            w === 540 ||
            (w === 720 && h <= 541) ||
            (w >= 1110 && w <= 1118 && h <= 741)
        );
    };
    const isIpad14ProMaxViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        return (
            (w >= 1028 && w <= 1036 && h >= 1370) ||
            (w >= 1370 && w <= 1382 && h <= 1040)
        );
    };
    const isAsusZenbookFoldViewport = () => {
        const w = __scoopViewportWidth();
        const h = __scoopViewportHeight();
        const near853 = (value) => value >= 849 && value <= 857;
        const near1280 = (value) => value >= 1276 && value <= 1284;
        const near1707 = (value) => value >= 1700 && value <= 1714;
        const near1920 = (value) => value >= 1910 && value <= 1930;
        const near1280u = (value) => value >= 1270 && value <= 1290;
        return (
            (near853(w) && near1280(h)) ||
            (near1280(w) && near853(h)) ||
            (near1707(w) && h >= 1000 && h <= 1120) ||
            (near1920(w) && near1280u(h)) ||
            (near1280u(w) && near1920(h))
        );
    };
    const isResponsiveViewport = () =>
        isPhoneViewport() ||
        isSurfaceDuoViewport() ||
        isIpad14ProMaxViewport() ||
        isAsusZenbookFoldViewport() ||
        (__scoopViewportWidth() >= TABLET_MIN && __scoopViewportWidth() <= TABLET_MAX);
    const isDesktopViewport = () => {
        const innerW = __scoopViewportWidth();
        const screenW = appWin.screen?.width || 0;
        if (isAsusZenbookFoldViewport()) {
            return false;
        }
        if (innerW >= DESKTOP_MIN) {
            return true;
        }
        // Browser zoom on a desktop monitor shrinks layout width below 1367px — keep split sidebar.
        return screenW >= DESKTOP_MIN && innerW >= DESKTOP_ZOOM_MIN;
    };

    const setDesktopLayoutFlag = (on) => {
        const root = doc.documentElement;
        if (on) {
            root.setAttribute("data-scoop-desktop-layout", "1");
        } else {
            root.removeAttribute("data-scoop-desktop-layout");
        }
    };

    const isAnalyzeReturnSuppressed = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        return !!(
            appWin.__scoopSuppressSidebarExpand &&
            Date.now() < appWin.__scoopSuppressSidebarExpand
        );
    };

    const shouldKeepResponsiveSidebarCollapsed = () => {
        if (!isResponsiveViewport()) {
            return false;
        }
        if (appWin.__scoopResponsiveSidebarUserToggled) {
            return false;
        }
        if (__scoopIsAnalyzePage()) {
            return !appWin.__scoopAnalyzeSidebarUserOpened;
        }
        return isAnalyzeReturnSuppressed();
    };

    const DESKTOP_INLINE_PROPS = {
        view: ["display", "flex-direction", "position", "width", "max-width", "margin-left", "padding-left"],
        sidebar: [
            "flex", "position", "transform", "translate", "transition", "visibility", "opacity",
            "overflow", "z-index", "height", "max-height", "min-height", "min-width", "width",
            "max-width", "left", "top", "box-shadow", "pointer-events", "align-self",
        ],
        inner: ["overflow-x", "overflow-y", "height", "max-height", "width", "max-width"],
        mainWrap: ["flex", "min-width", "width", "max-width"],
        mainSection: ["width", "max-width"],
    };

    const clearInlineProps = (node, props) => {
        if (!node) {
            return;
        }
        props.forEach((prop) => node.style.removeProperty(prop));
    };

    const clearDesktopInlineLayout = () => {
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        clearInlineProps(view, DESKTOP_INLINE_PROPS.view);
        clearInlineProps(sidebar, DESKTOP_INLINE_PROPS.sidebar);
        const inner =
            sidebar?.querySelector('[data-testid="stSidebarContent"]') ||
            sidebar?.firstElementChild;
        clearInlineProps(inner, DESKTOP_INLINE_PROPS.inner);
        const mainWrap = view?.querySelector(':scope > div:not([data-testid="stSidebar"])');
        clearInlineProps(mainWrap, DESKTOP_INLINE_PROPS.mainWrap);
        clearInlineProps(view?.querySelector("section.main"), DESKTOP_INLINE_PROPS.mainSection);
    };

    const applyResponsiveSidebarLayout = () => {
        if (!isResponsiveViewport()) {
            return;
        }
        clearDesktopInlineLayout();
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!view || !sidebar) {
            return;
        }

        view.style.setProperty("display", "block", "important");
        view.style.setProperty("width", "100%", "important");
        view.style.setProperty("max-width", "100vw", "important");
        view.style.setProperty("margin-left", "0", "important");
        view.style.setProperty("padding-left", "0", "important");

        if (shouldKeepResponsiveSidebarCollapsed()) {
            sidebar.setAttribute("aria-expanded", "false");
        }
        const expanded = shouldKeepResponsiveSidebarCollapsed()
            ? false
            : sidebar.getAttribute("aria-expanded") === "true";
        sidebar.style.setProperty("position", "fixed", "important");
        sidebar.style.setProperty("top", "0", "important");
        sidebar.style.setProperty("left", "0", "important");
        sidebar.style.setProperty("height", "100dvh", "important");
        sidebar.style.setProperty("min-height", "100dvh", "important");
        sidebar.style.setProperty("z-index", "1000010", "important");
        sidebar.style.setProperty("width", "min(92vw, 36rem)", "important");
        sidebar.style.setProperty("max-width", "min(92vw, 36rem)", "important");
        sidebar.style.setProperty(
            "transition",
            "transform 0.28s ease, visibility 0.28s ease",
            "important"
        );
        sidebar.style.setProperty(
            "transform",
            expanded ? "translateX(0)" : "translateX(-100vw)",
            "important"
        );
        sidebar.style.setProperty("visibility", expanded ? "visible" : "hidden", "important");
        sidebar.style.setProperty("pointer-events", expanded ? "auto" : "none", "important");

        const mainSection = view.querySelector("section.main");
        if (mainSection) {
            mainSection.style.setProperty("width", "100%", "important");
            mainSection.style.setProperty("max-width", "100vw", "important");
        }
        const mainWrap = view.querySelector(':scope > div:not([data-testid="stSidebar"])');
        if (mainWrap) {
            mainWrap.style.setProperty("width", "100%", "important");
            mainWrap.style.setProperty("max-width", "100vw", "important");
        }
    };

    const applyDesktopSidebarLayout = () => {
        if (!isDesktopViewport()) {
            return;
        }
        const view = doc.querySelector('[data-testid="stAppViewContainer"]');
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!view || !sidebar) {
            return;
        }
        view.style.setProperty("display", "flex", "important");
        view.style.setProperty("flex-direction", "row", "important");
        view.style.setProperty("position", "relative", "important");
        sidebar.style.setProperty("flex", "0 1 auto", "important");
        sidebar.style.setProperty("position", "relative", "important");
        sidebar.style.setProperty("transform", "none", "important");
        sidebar.style.setProperty("visibility", "visible", "important");
        sidebar.style.setProperty("overflow", "visible", "important");
        sidebar.style.setProperty("z-index", "2", "important");
        sidebar.style.setProperty("min-width", "min(10rem, 28vw)", "important");
        sidebar.style.setProperty("width", "var(--scoop-desktop-sidebar-width, clamp(10rem, min(20vw, 28rem), 36rem))", "important");
        sidebar.style.setProperty("max-width", "min(32vw, 36rem)", "important");
        sidebar.style.setProperty("height", "100vh", "important");
        sidebar.style.setProperty("max-height", "100vh", "important");
        const inner =
            sidebar.querySelector('[data-testid="stSidebarContent"]') ||
            sidebar.firstElementChild;
        if (inner) {
            inner.style.setProperty("overflow-x", "visible", "important");
            inner.style.setProperty("overflow-y", "auto", "important");
            inner.style.setProperty("min-width", "0", "important");
            inner.style.setProperty("height", "100vh", "important");
            inner.style.setProperty("max-height", "100vh", "important");
        }
        const mainWrap = view.querySelector(':scope > div:not([data-testid="stSidebar"])');
        if (mainWrap) {
            mainWrap.style.setProperty("flex", "1 1 0", "important");
            mainWrap.style.setProperty("min-width", "0", "important");
            mainWrap.style.setProperty("max-width", "100%", "important");
            mainWrap.style.setProperty("overflow-x", "auto", "important");
        }
        const mainSection = view.querySelector("section.main");
        if (mainSection) {
            mainSection.style.setProperty("min-width", "0", "important");
            mainSection.style.setProperty("max-width", "100%", "important");
            mainSection.style.setProperty("overflow-x", "auto", "important");
        }
    };

    const syncSidebarLayout = () => {
        if (isDesktopViewport()) {
            setDesktopLayoutFlag(true);
            applyDesktopSidebarLayout();
            return;
        }
        setDesktopLayoutFlag(false);
        if (isResponsiveViewport()) {
            applyResponsiveSidebarLayout();
            return;
        }
        clearDesktopInlineLayout();
    };

    appWin.__scoopLayout = {
        isResponsiveViewport,
        isDesktopViewport,
        isAnalyzePage: __scoopIsAnalyzePage,
        isAnalyzeReturnSuppressed,
        shouldKeepResponsiveSidebarCollapsed,
        applyResponsiveSidebarLayout,
        applyDesktopSidebarLayout,
        clearDesktopInlineLayout,
        syncSidebarLayout,
    };
})();
"""
)

_RESPONSIVE_LAYOUT_SYNC_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const sync = () => appWin.__scoopLayout?.syncSidebarLayout();
    let syncTimer = null;
    const schedule = () => {
        if (syncTimer) {
            return;
        }
        syncTimer = appWin.setTimeout(() => {
            syncTimer = null;
            sync();
        }, 80);
    };
    schedule();
    if (appWin.__scoopLayoutSyncBound) {
        return;
    }
    appWin.__scoopLayoutSyncBound = true;
    if (doc.readyState === "loading") {
        doc.addEventListener("DOMContentLoaded", schedule, { once: true });
    }
    if (!appWin.__scoopLayoutResizeBound) {
        appWin.__scoopLayoutResizeBound = true;
        appWin.addEventListener("resize", schedule);
        if (appWin.visualViewport) {
            appWin.visualViewport.addEventListener("resize", schedule);
        }
    }
    const bindSidebarObserver = () => {
        if (appWin.__scoopLayoutObserver) {
            return true;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) {
            return false;
        }
        appWin.__scoopLayoutObserver = new MutationObserver(schedule);
        appWin.__scoopLayoutObserver.observe(sidebar, {
            attributes: true,
            attributeFilter: ["aria-expanded", "class"],
        });
        return true;
    };
    if (!bindSidebarObserver()) {
        let attempts = 0;
        const retry = appWin.setInterval(() => {
            attempts += 1;
            if (bindSidebarObserver() || attempts >= 12) {
                appWin.clearInterval(retry);
            }
        }, 250);
    }
})();
"""
)

_ANALYZE_RETURN_NAV_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const RETURN_KEY = "scoop-return-from-analyze";
    const SUPPRESS_MS = 10000;

    const markAnalyzeReturn = () => {
        try {
            appWin.sessionStorage.setItem(RETURN_KEY, "1");
            appWin.sessionStorage.setItem("scoop-landing-seen", "1");
            appWin.__scoopSuppressSidebarExpand = Date.now() + SUPPRESS_MS;
            if (typeof appWin.__scoopClearResponsiveExpandTimers === "function") {
                appWin.__scoopClearResponsiveExpandTimers();
            }
        } catch (e) {}
    };

    const shouldForceScreenerMainView = () => {
        if (__scoopIsAnalyzePage()) {
            return false;
        }
        const layout = appWin.__scoopLayout;
        if (!layout?.isResponsiveViewport?.()) {
            return false;
        }
        try {
            if (appWin.sessionStorage.getItem(RETURN_KEY) === "1") {
                return true;
            }
        } catch (e) {}
        return !!(appWin.__scoopSuppressSidebarExpand && Date.now() < appWin.__scoopSuppressSidebarExpand);
    };

    const forceScreenerMainView = () => {
        if (!shouldForceScreenerMainView()) {
            return;
        }
        try {
            if (appWin.sessionStorage.getItem(RETURN_KEY) === "1") {
                appWin.sessionStorage.removeItem(RETURN_KEY);
            }
        } catch (e) {}
        appWin.__scoopSuppressSidebarExpand = Date.now() + SUPPRESS_MS;
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar) {
            sidebar.setAttribute("aria-expanded", "false");
        }
        appWin.__scoopLayout?.syncSidebarLayout?.();
    };

    if (!appWin.__scoopAnalyzeReturnNavBound) {
        appWin.__scoopAnalyzeReturnNavBound = true;
        doc.addEventListener(
            "click",
            (event) => {
                if (event.target.closest("a.scoop-analyze-back")) {
                    markAnalyzeReturn();
                }
            },
            true
        );
    }
})();
"""
)

_RESPONSIVE_SIDEBAR_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;
    const isResponsiveViewport = () => layout()?.isResponsiveViewport() ?? false;
    const isAnalyzeReturnSuppressed = () => layout()?.isAnalyzeReturnSuppressed?.() ?? false;

    const collapseSidebar = () => {
        if (isResponsiveViewport()) {
            appWin.__scoopResponsiveSidebarUserToggled = true;
            appWin.__scoopSuppressSidebarExpand = 0;
        }
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
            const node = doc.querySelector(selector);
            if (node) {
                node.click();
                layout()?.syncSidebarLayout();
                return true;
            }
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            sidebar.setAttribute("aria-expanded", "false");
            layout()?.syncSidebarLayout();
            return true;
        }
        return false;
    };

    const expandSidebar = () => {
        if (
            isAnalyzeReturnSuppressed() &&
            !appWin.__scoopResponsiveSidebarUserToggled
        ) {
            return false;
        }
        if (__scoopIsAnalyzePage() && isResponsiveViewport() && !appWin.__scoopAnalyzeSidebarUserOpened) {
            return false;
        }
        const selectors = [
            '[data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button',
            '[data-testid="stHeader"] [data-testid="stExpandSidebarButton"]',
            '[data-testid="collapsedControl"] button',
            '[data-testid="collapsedControl"]',
        ];
        for (const selector of selectors) {
            const node = doc.querySelector(selector);
            if (node) {
                node.click();
                layout()?.syncSidebarLayout();
                return true;
            }
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "false") {
            sidebar.setAttribute("aria-expanded", "true");
            layout()?.syncSidebarLayout();
            return true;
        }
        return false;
    };

    const removeLegacyCloseButton = () => {
        doc.getElementById("scoop-responsive-sidebar-close")?.remove();
        doc.querySelectorAll(".scoop-responsive-sidebar-close").forEach((node) => {
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
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
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

    let tabletBootstrapped = false;
    const ANALYZE_RETURN_KEY = "scoop-return-from-analyze";
    const POST_CONSENT_KEY = "scoop-post-consent-collapse";
    const SIDEBAR_BOOTSTRAP_KEY = "scoop-responsive-sidebar-ready";

    const markSidebarBootstrapped = () => {
        tabletBootstrapped = true;
        try {
            appWin.sessionStorage.setItem(SIDEBAR_BOOTSTRAP_KEY, "1");
        } catch (e) {}
    };

    try {
        tabletBootstrapped = appWin.sessionStorage.getItem(SIDEBAR_BOOTSTRAP_KEY) === "1";
    } catch (e) {}

    const isReturningFromAnalyze = () => {
        try {
            return appWin.sessionStorage.getItem(ANALYZE_RETURN_KEY) === "1";
        } catch (e) {
            return false;
        }
    };

    const clearReturningFromAnalyze = () => {
        try {
            appWin.sessionStorage.removeItem(ANALYZE_RETURN_KEY);
        } catch (e) {}
    };

    const isPostConsentCollapse = () => {
        if (!isResponsiveViewport()) {
            return false;
        }
        try {
            return appWin.sessionStorage.getItem(POST_CONSENT_KEY) === "1";
        } catch (e) {
            return false;
        }
    };

    const clearPostConsentCollapse = () => {
        try {
            appWin.sessionStorage.removeItem(POST_CONSENT_KEY);
        } catch (e) {}
    };

    const holdScreenerMainView = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        const suppressed =
            isAnalyzeReturnSuppressed() ||
            isReturningFromAnalyze();
        if (!suppressed) {
            return false;
        }
        if (isReturningFromAnalyze()) {
            clearReturningFromAnalyze();
        }
        appWin.__scoopSuppressSidebarExpand = Date.now() + 10000;
        markSidebarBootstrapped();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
            sidebar.setAttribute("aria-expanded", "false");
        }
        layout()?.syncSidebarLayout?.();
        removeLegacyCloseButton();
        return true;
    };

    const holdMainViewAfterConsent = () => {
        if (!isResponsiveViewport() || __scoopIsAnalyzePage()) {
            return false;
        }
        if (!isPostConsentCollapse()) {
            return false;
        }
        clearPostConsentCollapse();
        appWin.__scoopSuppressSidebarExpand = Date.now() + 12000;
        markSidebarBootstrapped();
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
            sidebar.setAttribute("aria-expanded", "false");
        }
        layout()?.syncSidebarLayout?.();
        removeLegacyCloseButton();
        return true;
    };

    const ensureScreenerContentVisible = () => {
        holdScreenerMainView();
    };

    const scheduleCollapseAfterAnalyzeReturn = () => {
        if (appWin.__scoopAnalyzeReturnCollapseTimers) {
            appWin.__scoopAnalyzeReturnCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
        }
        appWin.__scoopAnalyzeReturnCollapseTimers = [];
        const run = () => holdScreenerMainView();
        run();
        appWin.requestAnimationFrame(run);
        [150, 500, 1200].forEach((delay) => {
            const timerId = appWin.setTimeout(run, delay);
            appWin.__scoopAnalyzeReturnCollapseTimers.push(timerId);
        });
    };

    const scheduleCollapseAfterConsent = () => {
        if (appWin.__scoopPostConsentCollapseTimers) {
            appWin.__scoopPostConsentCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
        }
        appWin.__scoopPostConsentCollapseTimers = [];
        const run = () => holdMainViewAfterConsent();
        run();
        appWin.requestAnimationFrame(run);
        [150, 500, 1200].forEach((delay) => {
            const timerId = appWin.setTimeout(run, delay);
            appWin.__scoopPostConsentCollapseTimers.push(timerId);
        });
    };

    appWin.__scoopResponsiveSidebarBound = appWin.__scoopResponsiveSidebarBound || false;
    removeLegacyCloseButton();

    if (!appWin.__scoopResponsiveSidebarBound) {
        appWin.__scoopResponsiveSidebarBound = true;

        if (appWin.__scoopLayout) {
            appWin.__scoopLayout.collapseSidebar = collapseSidebar;
            appWin.__scoopLayout.expandSidebar = expandSidebar;
        }

        doc.addEventListener(
            "click",
            (event) => {
                if (shouldCloseSidebar(event)) {
                    collapseSidebar();
                }
            },
            true
        );

        doc.addEventListener("keydown", (event) => {
            if (event.key === "Escape" && isResponsiveViewport()) {
                collapseSidebar();
            }
        });

        doc.addEventListener(
            "click",
            (event) => {
                if (!isResponsiveViewport()) {
                    return;
                }
                const expandTarget = event.target.closest(
                    '[data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"]'
                );
                const collapseTarget = event.target.closest(
                    '[data-testid="stSidebarCollapseButton"]'
                );
                if (!expandTarget && !collapseTarget) {
                    return;
                }
                event.preventDefault();
                event.stopPropagation();
                appWin.__scoopResponsiveSidebarUserToggled = true;
                appWin.__scoopSuppressSidebarExpand = 0;
                if (expandTarget && __scoopIsAnalyzePage()) {
                    appWin.__scoopAnalyzeSidebarUserOpened = true;
                }
                const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
                if (!sidebar) {
                    return;
                }
                sidebar.setAttribute(
                    "aria-expanded",
                    expandTarget ? "true" : "false"
                );
                layout()?.syncSidebarLayout?.();
            },
            true
        );
    }

    if (appWin.__scoopResponsiveSidebarInitDone) {
        if (__scoopIsAnalyzePage() && isResponsiveViewport()) {
            if (!appWin.__scoopAnalyzeSidebarUserOpened) {
                const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
                if (sidebar && sidebar.getAttribute("aria-expanded") !== "false") {
                    sidebar.setAttribute("aria-expanded", "false");
                }
            }
            layout()?.syncSidebarLayout();
            return;
        }
        if (isReturningFromAnalyze() || isAnalyzeReturnSuppressed()) {
            holdScreenerMainView();
        } else if (isPostConsentCollapse()) {
            holdMainViewAfterConsent();
        } else {
            layout()?.syncSidebarLayout();
        }
        return;
    }

    const ensureAnalyzeSidebarCollapsed = () => {
        if (!isResponsiveViewport() || !__scoopIsAnalyzePage()) {
            return;
        }
        if (appWin.__scoopAnalyzeSidebarUserOpened) {
            layout()?.syncSidebarLayout();
            return;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            collapseSidebar();
        }
        layout()?.syncSidebarLayout();
        removeLegacyCloseButton();
    };

    const scheduleAnalyzeSidebarCollapse = () => {
        if (!__scoopIsAnalyzePage() || !isResponsiveViewport()) {
            return;
        }
        appWin.__scoopAnalyzeSidebarUserOpened = false;
        ensureAnalyzeSidebarCollapsed();
        appWin.requestAnimationFrame(ensureAnalyzeSidebarCollapsed);
        [50, 150, 400, 900, 1600, 2500, 4000].forEach((delay) => {
            appWin.setTimeout(ensureAnalyzeSidebarCollapsed, delay);
        });
    };

    const ensureInitialResponsiveExpand = () => {
        if (!isResponsiveViewport()) {
            layout()?.syncSidebarLayout();
            return;
        }
        layout()?.syncSidebarLayout();
        if (__scoopIsAnalyzePage()) {
            markSidebarBootstrapped();
            scheduleAnalyzeSidebarCollapse();
            return;
        }
        if (
            isReturningFromAnalyze() ||
            isAnalyzeReturnSuppressed()
        ) {
            markSidebarBootstrapped();
            scheduleCollapseAfterAnalyzeReturn();
            return;
        }
        if (isPostConsentCollapse()) {
            markSidebarBootstrapped();
            scheduleCollapseAfterConsent();
            return;
        }
        if (tabletBootstrapped) {
            layout()?.syncSidebarLayout();
            return;
        }
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar) {
            return;
        }
        if (sidebar.getAttribute("aria-expanded") === "true") {
            markSidebarBootstrapped();
            layout()?.syncSidebarLayout();
            removeLegacyCloseButton();
            return;
        }
        if (expandSidebar()) {
            markSidebarBootstrapped();
            layout()?.syncSidebarLayout();
            removeLegacyCloseButton();
        }
    };

    ensureInitialResponsiveExpand();
    appWin.__scoopResponsiveSidebarInitDone = true;
    appWin.__scoopResponsiveExpandTimers = appWin.__scoopResponsiveExpandTimers || [];
    appWin.__scoopClearResponsiveExpandTimers = () => {
        (appWin.__scoopResponsiveExpandTimers || []).forEach((timerId) => {
            appWin.clearTimeout(timerId);
        });
        appWin.__scoopResponsiveExpandTimers = [];
        if (appWin.__scoopAnalyzeReturnCollapseTimers) {
            appWin.__scoopAnalyzeReturnCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
            appWin.__scoopAnalyzeReturnCollapseTimers = [];
        }
        if (appWin.__scoopPostConsentCollapseTimers) {
            appWin.__scoopPostConsentCollapseTimers.forEach((timerId) => {
                appWin.clearTimeout(timerId);
            });
            appWin.__scoopPostConsentCollapseTimers = [];
        }
    };
    if (
        !isAnalyzeReturnSuppressed() &&
        !isReturningFromAnalyze() &&
        !isPostConsentCollapse() &&
        !tabletBootstrapped
    ) {
        appWin.requestAnimationFrame(() => {
            ensureInitialResponsiveExpand();
            removeLegacyCloseButton();
        });
        const timerId = appWin.setTimeout(() => {
            ensureInitialResponsiveExpand();
            removeLegacyCloseButton();
        }, 400);
        appWin.__scoopResponsiveExpandTimers.push(timerId);
    }
})();
"""
)

_TOOLTIP_SCROLL_JS = """
(() => {
    const root = document.documentElement;
    const className = "scoop-tooltip-scrolling";
    const DESKTOP_MIN = 1367;
    const MOBILE_MAX = 768;
    const MOBILE_HEADLINES_BOTTOM_TAP_PAD = 80;
    const RESPONSIVE_MIN = 769;
    const RESPONSIVE_MAX = 1366;
    const IPAD_MINI_MIN = 744;
    const IPAD_MINI_MAX = 768;
    const VIEWPORT_PAD = 12;
    const GAP = 10;
    const HEADLINES_DESKTOP_OFFSET = 12;
    const DESKTOP_HEADLINES_MIN_WIDTH = 320;
    const DESKTOP_HEADLINES_WIDTH_TRIM = 70;
    const DESKTOP_HEADLINES_TOP = 100;
    const DESKTOP_HEADLINES_ANCHOR_GAP = 10;

    if (!window.__scoopDesktopHeadlinesHideTimers) {
        window.__scoopDesktopHeadlinesHideTimers = new WeakMap();
    }
    window.__scoopDesktopHeadlinesSyncing = false;

    const isResponsiveHeadlinesViewport = () =>
        window.innerWidth >= RESPONSIVE_MIN && window.innerWidth <= RESPONSIVE_MAX;

    const isIpadMiniViewport = () => {
        const w = window.innerWidth;
        return w >= IPAD_MINI_MIN && w <= IPAD_MINI_MAX;
    };

    const isIpadAirViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const near820 = (value) => value >= 816 && value <= 824;
        const near1180 = (value) => value >= 1176 && value <= 1184;
        return (
            (near820(w) && near1180(h)) ||
            (near1180(w) && near820(h))
        );
    };

    const isIpadMiniOrAirHeadlinesViewport = () =>
        isIpadMiniViewport() || isIpadAirViewport();

    const isSurfaceDuoViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        return (
            w === 540 ||
            (w === 720 && h <= 541) ||
            (w >= 1110 && w <= 1118 && h <= 741)
        );
    };

    const isAsusZenbookFoldViewport = () => {
        const w = window.innerWidth;
        const h = window.innerHeight;
        const near853 = (value) => value >= 849 && value <= 857;
        const near1280 = (value) => value >= 1276 && value <= 1284;
        const near1707 = (value) => value >= 1700 && value <= 1714;
        const near1920 = (value) => value >= 1910 && value <= 1930;
        const near1280u = (value) => value >= 1270 && value <= 1290;
        return (
            (near853(w) && near1280(h)) ||
            (near1280(w) && near853(h)) ||
            (near1707(w) && h >= 1000 && h <= 1120) ||
            (near1920(w) && near1280u(h)) ||
            (near1280u(w) && near1920(h))
        );
    };

    const isDesktopLayoutViewport = () =>
        window.innerWidth >= DESKTOP_MIN && !isAsusZenbookFoldViewport();

    const usesTabletProHeadlinesPopup = () =>
        isResponsiveHeadlinesViewport() ||
        isIpadMiniViewport() ||
        isSurfaceDuoViewport() ||
        isAsusZenbookFoldViewport();

    const isPhoneMobileHeadlinesViewport = () =>
        window.innerWidth <= MOBILE_MAX && !usesTabletProHeadlinesPopup();

    const isPhoneMobileHeadlinesOpen = () =>
        isPhoneMobileHeadlinesViewport() &&
        !!document.querySelector(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked");

    const isInsideDesktopHeadlinesPopup = (node) => {
        if (!isDesktopLayoutViewport() || !node || !node.closest) {
            return false;
        }
        return !!node.closest(
            ".full-results-wrap .tip-wrap.headlines-tip .tip-text, .full-results-wrap .tip-wrap.headlines-tip .headlines-tip-scroll"
        );
    };

    const isDesktopHeadlinesSessionOpen = () =>
        isDesktopLayoutViewport() &&
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

    const isDesktopHeadlinesOpenWrap = (wrap) => {
        if (!wrap) {
            return false;
        }
        return (
            wrap.classList.contains("hl-tip-desktop-open") ||
            !!wrap.querySelector(":scope > .hl-tip-cb:checked")
        );
    };

    const getDesktopHeadlinesTipBorderY = (tip) => {
        const tipStyles = getComputedStyle(tip);
        return (
            (parseFloat(tipStyles.borderTopWidth) || 0) +
            (parseFloat(tipStyles.borderBottomWidth) || 0)
        );
    };

    const applyDesktopHeadlinesScrollStyles = (wrap, slot) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const heading = tip?.querySelector(".hl-tip-heading");
        if (!tip || !scroll) {
            return;
        }

        const tipHeight =
            parseFloat(tip.style.getPropertyValue("--hl-fixed-height")) ||
            tip.clientHeight ||
            (slot ? Math.max(120, slot.maxHeight - getDesktopHeadlinesTipBorderY(tip)) : 0);
        const headingHeight = heading ? heading.offsetHeight : 0;
        const tipBorderY = getDesktopHeadlinesTipBorderY(tip);
        const scrollHeight = Math.max(80, tipHeight - headingHeight - tipBorderY);

        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("overflow", "hidden", "important");
        scroll.style.setProperty("flex", "1 1 auto", "important");
        scroll.style.setProperty("min-height", "0", "important");
        scroll.style.setProperty("overflow-x", "hidden", "important");
        scroll.style.setProperty("overflow-y", "auto", "important");
        scroll.style.setProperty("-webkit-overflow-scrolling", "touch", "important");
        scroll.style.setProperty("scrollbar-width", "none", "important");
        scroll.style.setProperty("pointer-events", "auto", "important");
        scroll.style.setProperty("touch-action", "pan-y", "important");
        scroll.style.setProperty("--hl-scroll-max-height", `${scrollHeight}px`);
        scroll.style.setProperty("height", `${scrollHeight}px`, "important");
        scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
    };

    const hideTooltips = (event) => {
        if (isDesktopHeadlinesSessionOpen() || isPhoneMobileHeadlinesOpen()) {
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
            scroll.style.removeProperty("margin-top");
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
        restoreHeadlinesHeading(wrap);
    };

    const getHeadlinesHeadingBaseLabel = (heading) => {
        if (!heading) {
            return "Headlines";
        }
        if (!heading.dataset.hlBaseLabel) {
            const current = (heading.textContent || "Headlines").trim();
            heading.dataset.hlBaseLabel = current.split(" - ")[0].trim() || "Headlines";
        }
        return heading.dataset.hlBaseLabel;
    };

    const getCompanyNameFromHeadlinesRow = (wrap) => {
        const row = wrap?.closest("tr");
        if (!row) {
            return "";
        }

        const inCommodityResults = !!wrap.closest(".commodity-results");
        const valueCell =
            row.querySelector('td[data-label="Company"] .fr-val') ||
            row.querySelector('td[data-label="Name"] .fr-val') ||
            (inCommodityResults
                ? row.querySelector('td[data-label="Commodity"] .fr-val')
                : null);
        if (!valueCell) {
            return "";
        }

        const tipWrap = valueCell.querySelector(".tip-wrap");
        if (tipWrap) {
            const clone = tipWrap.cloneNode(true);
            clone.querySelectorAll(".tip-text").forEach((node) => node.remove());
            return (clone.textContent || "").replace(/\\s+/g, " ").trim();
        }

        return (valueCell.textContent || "").replace(/\\s+/g, " ").trim();
    };

    const updateHeadlinesHeading = (wrap) => {
        if (!wrap) {
            return;
        }
        const heading = wrap.querySelector(".hl-tip-heading");
        if (!heading) {
            return;
        }

        const baseLabel = getHeadlinesHeadingBaseLabel(heading);
        const company = getCompanyNameFromHeadlinesRow(wrap);
        heading.textContent = company ? `${baseLabel} - ${company}` : baseLabel;
    };

    const restoreHeadlinesHeading = (wrap) => {
        const heading = wrap?.querySelector(".hl-tip-heading");
        if (!heading) {
            return;
        }
        heading.textContent = getHeadlinesHeadingBaseLabel(heading);
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
        const tipBorderY = getDesktopHeadlinesTipBorderY(tip);
        const usableMaxHeight = Math.max(120, maxHeight - tipBorderY);
        const needsScroll = contentHeight > usableMaxHeight + 1;
        const tipHeight = needsScroll ? usableMaxHeight : contentHeight;

        tip.style.setProperty("--hl-fixed-height", `${tipHeight}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${maxHeight}px`);
        tip.style.setProperty("height", `${tipHeight}px`);
        tip.style.height = `${tipHeight}px`;

        if (scroll) {
            const heading = tip.querySelector(".hl-tip-heading");
            const headingHeight = heading ? heading.offsetHeight : 0;
            const scrollHeight = Math.max(80, tipHeight - headingHeight - tipBorderY);
            scroll.style.setProperty("--hl-scroll-max-height", `${scrollHeight}px`);
            scroll.style.setProperty("overflow-y", needsScroll ? "auto" : "visible", "important");
            if (needsScroll) {
                scroll.style.setProperty("height", `${scrollHeight}px`, "important");
                scroll.style.setProperty("max-height", `${scrollHeight}px`, "important");
            } else {
                scroll.style.removeProperty("height");
                scroll.style.removeProperty("max-height");
            }
        }
    };

    const bindDesktopHeadlinesScrollWheel = (wrap) => {
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        if (!scroll) {
            return;
        }
        const bindTarget = (node) => {
            if (!node) {
                return;
            }
            if (node.__hlWheelHandler) {
                node.removeEventListener("wheel", node.__hlWheelHandler, true);
            }
            node.__hlWheelHandler = (event) => {
                scrollDesktopHeadlinesFromWheel(event, scroll);
            };
            node.addEventListener("wheel", node.__hlWheelHandler, { passive: false, capture: true });
        };
        bindTarget(scroll);
        bindTarget(tip);
    };

    const unbindDesktopHeadlinesScrollWheel = (wrap) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        [scroll, tip].forEach((node) => {
            if (node?.__hlWheelHandler) {
                node.removeEventListener("wheel", node.__hlWheelHandler, true);
                delete node.__hlWheelHandler;
            }
        });
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

    const getPageScrollEl = () =>
        document.querySelector('[data-testid="stAppViewContainer"]') ||
        document.scrollingElement ||
        document.documentElement;

    const restorePageScroll = (scrollTop) => {
        const scrollEl = getPageScrollEl();
        scrollEl.scrollTop = scrollTop;
        window.scrollTo(0, scrollTop);
    };

    const getThirdTopPickNearLowBadge = () => {
        const topPickHeading = [...document.querySelectorAll("h3")].find((heading) =>
            /Top Picks/i.test((heading.textContent || "").trim())
        );
        if (!topPickHeading) {
            return null;
        }

        const mainBlock =
            topPickHeading.closest('[data-testid="stMainBlockContainer"]') ||
            topPickHeading.closest('[data-testid="stAppViewContainer"]');
        if (!mainBlock) {
            return null;
        }

        for (const block of mainBlock.querySelectorAll('[data-testid="stHorizontalBlock"]')) {
            const columns = [...block.children].filter(
                (node) => node.getAttribute("data-testid") === "stColumn"
            );
            if (columns.length < 3) {
                continue;
            }

            const thirdColumn = columns[2];
            const metric = thirdColumn.querySelector('[data-testid="stMetric"]');
            if (!metric || !/#3\\b/i.test(metric.textContent || "")) {
                continue;
            }

            const badge = [...thirdColumn.querySelectorAll("b")].find((node) =>
                /52W LOW/i.test((node.textContent || "").trim())
            );
            if (badge) {
                return badge;
            }
        }

        return null;
    };

    const getThirdTopPickNearLowAnchorRect = () => {
        const badge = getThirdTopPickNearLowBadge();
        return badge ? badge.getBoundingClientRect() : null;
    };

    const getNearLowBadgeFloorTop = () => {
        const anchorRect = getThirdTopPickNearLowAnchorRect();
        if (!anchorRect) {
            return null;
        }
        if (anchorRect.bottom <= VIEWPORT_PAD || anchorRect.top >= window.innerHeight) {
            return null;
        }
        return Math.round(anchorRect.bottom + DESKTOP_HEADLINES_ANCHOR_GAP);
    };

    const getDesktopHeadlinesAnchorTop = (tipHeight = 0) => {
        let top = DESKTOP_HEADLINES_TOP;
        const floorTop = getNearLowBadgeFloorTop();
        if (floorTop !== null) {
            top = Math.max(top, floorTop);
        }

        if (tipHeight > 0) {
            const viewBottom = window.innerHeight - VIEWPORT_PAD;
            const minTop = floorTop !== null ? floorTop : VIEWPORT_PAD;
            if (top + tipHeight > viewBottom) {
                top = Math.max(minTop, viewBottom - tipHeight);
            }
        }

        return top;
    };

    const getDesktopHeadlinesSlot = (tipHeight = 0) => {
        const viewLeft = VIEWPORT_PAD;
        const viewRight = window.innerWidth - VIEWPORT_PAD;
        const rootSize = parseFloat(getComputedStyle(document.documentElement).fontSize) || 16;

        const tableRect = getFullResultsTableRect();
        const top = getDesktopHeadlinesAnchorTop(tipHeight);
        const maxHeight = Math.max(200, window.innerHeight - top - VIEWPORT_PAD);

        let left = viewLeft;
        let width = Math.round(
            Math.min(viewRight - viewLeft, Math.max(280, Math.min(21 * rootSize, window.innerWidth * 0.36)))
        );

        const panelRect = getDesktopHeadlinesPanelRect();
        if (panelRect && panelRect.width > 0) {
            left = Math.round(panelRect.left);
            width = Math.round(panelRect.width);
        }

        width = Math.max(DESKTOP_HEADLINES_MIN_WIDTH, width - DESKTOP_HEADLINES_WIDTH_TRIM);

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
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        const scroll = getDesktopHeadlinesScrollContainer(wrap);
        const prevScrollTop = preserveScroll && scroll ? scroll.scrollTop : 0;

        tip.style.setProperty("position-anchor", "none");
        updateHeadlinesHeading(wrap);

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
        applyDesktopHeadlinesScrollStyles(wrap, slot);
        if (preserveScroll && scroll) {
            scroll.scrollTop = prevScrollTop;
        }

        const tipHeight =
            parseFloat(tip.style.getPropertyValue("--hl-fixed-height")) ||
            tip.clientHeight ||
            0;
        const adjustedTop = getDesktopHeadlinesAnchorTop(tipHeight);
        if (adjustedTop !== slot.top) {
            slot = getDesktopHeadlinesSlot(tipHeight);
            tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
            tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
            fitDesktopHeadlinesTip(tip, slot);
            applyDesktopHeadlinesScrollStyles(wrap, slot);
            if (preserveScroll && scroll) {
                scroll.scrollTop = prevScrollTop;
            }
        }

        if (isDesktopHeadlinesOpenWrap(wrap)) {
            ensureDesktopHeadlinesVisible(wrap);
            bindDesktopHeadlinesScrollWheel(wrap);
        }
    };

    const scheduleDesktopHeadlinesPosition = (wrap, preserveScroll = false) => {
        positionDesktopHeadlinesTip(wrap, preserveScroll);
        window.requestAnimationFrame(() => {
            positionDesktopHeadlinesTip(wrap, preserveScroll);
        });
    };

    const resolveDesktopHeadlinesWrap = (node) => {
        if (!node || !node.closest) {
            return null;
        }
        return node.closest(".full-results-wrap .tip-wrap.headlines-tip");
    };

    const getDesktopHeadlinesScrollEl = (node, event) => {
        if (!isDesktopLayoutViewport()) {
            return null;
        }

        let target = node && node.nodeType === Node.ELEMENT_NODE ? node : null;
        if (event && Number.isFinite(event.clientX) && Number.isFinite(event.clientY)) {
            const hit = document.elementFromPoint(event.clientX, event.clientY);
            if (hit && hit.nodeType === Node.ELEMENT_NODE) {
                target = hit;
            }
        }
        if (!target || !target.closest) {
            return null;
        }

        const resolvedWrap = target.closest(
            ".full-results-wrap .tip-wrap.headlines-tip.hl-tip-desktop-open, .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked)"
        );
        if (!resolvedWrap) {
            return null;
        }
        const scroll = getDesktopHeadlinesScrollContainer(resolvedWrap);
        if (!scroll) {
            return null;
        }
        if (scroll.contains(target) || target.closest(".headlines-tip-scroll") === scroll) {
            return scroll;
        }
        if (target.closest(".tip-text") && resolvedWrap.contains(target.closest(".tip-text"))) {
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
        if (!isDesktopLayoutViewport() || !wrap) {
            return;
        }
        cancelDesktopHeadlinesHide(wrap);
        wrap.classList.add("hl-tip-desktop-open");
        root.classList.remove(className);
        document.body.classList.remove(className);
        ensureDesktopHeadlinesVisible(wrap);

        const savedScrollTop = getPageScrollEl().scrollTop;
        scheduleDesktopHeadlinesPosition(wrap, false);
        window.requestAnimationFrame(() => {
            restorePageScroll(savedScrollTop);
            scheduleDesktopHeadlinesPosition(wrap, false);
            window.requestAnimationFrame(() => {
                restorePageScroll(savedScrollTop);
                scheduleDesktopHeadlinesPosition(wrap, false);
            });
        });
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
        if (!isDesktopLayoutViewport() || !checkbox) {
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
        if (isDesktopLayoutViewport()) {
            handleDesktopHeadlinesChange(checkbox);
            return;
        }
        if (checkbox.checked) {
            if (usesTabletProHeadlinesPopup()) {
                scheduleResponsiveHeadlinesPosition(wrap);
            } else if (isPhoneMobileHeadlinesViewport()) {
                const savedScrollTop = getPageScrollEl().scrollTop;
                schedulePhoneMobileHeadlinesPosition(wrap);
                window.requestAnimationFrame(() => {
                    restorePageScroll(savedScrollTop);
                    schedulePhoneMobileHeadlinesPosition(wrap);
                    window.requestAnimationFrame(() => {
                        restorePageScroll(savedScrollTop);
                        schedulePhoneMobileHeadlinesPosition(wrap);
                    });
                });
            }
            updateHeadlinesHeading(wrap);
            window.requestAnimationFrame(() => {
                if (usesTabletProHeadlinesPopup()) {
                    scheduleResponsiveHeadlinesPosition(wrap);
                } else if (isPhoneMobileHeadlinesViewport()) {
                    schedulePhoneMobileHeadlinesPosition(wrap);
                }
                updateHeadlinesHeading(wrap);
            });
        } else {
            clearHeadlinesPosition(wrap);
        }
    };

    const scrollDesktopHeadlinesFromWheel = (event, scrollEl) => {
        if (!isDesktopLayoutViewport() || !scrollEl || !event) {
            return false;
        }
        const delta = event.deltaY;
        if (!delta) {
            return false;
        }
        const maxScroll = scrollEl.scrollHeight - scrollEl.clientHeight;
        event.preventDefault();
        event.stopPropagation();
        if (maxScroll <= 0) {
            return true;
        }
        scrollEl.scrollTop = Math.max(0, Math.min(maxScroll, scrollEl.scrollTop + delta));
        return true;
    };

    const handleDesktopHeadlinesWheel = (event) => {
        if (!isDesktopLayoutViewport()) {
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
        if (!isDesktopLayoutViewport()) {
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
        getThirdTopPickNearLowAnchorRect,
        getThirdTopPickNearLowBadge,
        getNearLowBadgeFloorTop,
        getDesktopHeadlinesAnchorTop,
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

        const centerHorizontally = isResponsiveHeadlinesViewport();

        let widthBasisLeft = viewLeft;
        if (!centerHorizontally && content) {
            widthBasisLeft = Math.max(viewLeft, Math.round(content.getBoundingClientRect().left));
        }

        const availableWidth = viewRight - (centerHorizontally ? viewLeft : widthBasisLeft);
        const width = Math.round(
            Math.min(availableWidth, Math.max(280, window.innerWidth * 0.4))
        );

        let left = centerHorizontally
            ? Math.round(viewLeft + (viewRight - viewLeft - width) / 2)
            : widthBasisLeft;

        if (left + width > viewRight) {
            left = Math.max(viewLeft, viewRight - width);
        }
        if (left < viewLeft) {
            left = viewLeft;
        }

        if (isIpadMiniOrAirHeadlinesViewport()) {
            left = Math.round((window.innerWidth - width) / 2);
            left = Math.max(VIEWPORT_PAD, Math.min(left, viewRight - width));
        }

        if (isSurfaceDuoViewport()) {
            left = Math.round((window.innerWidth - width) / 2);
            left = Math.max(VIEWPORT_PAD, Math.min(left, viewRight - width));
        }

        return {
            top,
            left: Math.round(left),
            width,
            maxHeight: Math.round(maxHeight),
        };
    };

    const getPhoneMobileHeadlinesSlot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        const viewRight = window.innerWidth - VIEWPORT_PAD;
        const viewLeft = VIEWPORT_PAD;
        const top = Math.round(headerBottom + VIEWPORT_PAD);
        const maxHeight = Math.max(
            200,
            window.innerHeight - top - MOBILE_HEADLINES_BOTTOM_TAP_PAD
        );
        const width = Math.round(
            Math.min(viewRight - viewLeft, Math.max(280, window.innerWidth - 2 * VIEWPORT_PAD))
        );
        return {
            top,
            left: viewLeft,
            width,
            maxHeight,
        };
    };

    const applyPhoneMobileHeadlinesSlot = (wrap, slot, resetScroll = true) => {
        const tip = wrap?.querySelector(":scope > .tip-text");
        if (!tip || !slot) {
            return;
        }

        tip.style.setProperty("--hl-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--hl-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--hl-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--hl-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("position-anchor", "none");
        tip.style.setProperty("height", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("display", "flex", "important");
        tip.style.setProperty("flex-direction", "column", "important");
        tip.style.setProperty("overflow", "hidden", "important");

        if (resetScroll) {
            const scroll = tip.querySelector(".headlines-tip-scroll");
            if (scroll) {
                scroll.scrollTop = 0;
            }
        }
    };

    const syncPhoneMobileHeadlinesHeadingInset = (wrap) => {
        if (!isPhoneMobileHeadlinesViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        const heading = tip?.querySelector(".hl-tip-heading");
        const scroll = tip?.querySelector(".headlines-tip-scroll");
        if (!heading || !scroll) {
            return;
        }
        const headingHeight = Math.max(0, Math.ceil(heading.getBoundingClientRect().height));
        scroll.style.setProperty("margin-top", `${headingHeight}px`, "important");
    };

    const positionPhoneMobileHeadlinesTip = (wrap, preserveScroll = false) => {
        if (!isPhoneMobileHeadlinesViewport() || !wrap) {
            return;
        }
        const checkbox = wrap.querySelector(".hl-tip-cb");
        if (!checkbox || !checkbox.checked) {
            return;
        }

        applyPhoneMobileHeadlinesSlot(wrap, getPhoneMobileHeadlinesSlot(), !preserveScroll);
        updateHeadlinesHeading(wrap);
        syncPhoneMobileHeadlinesHeadingInset(wrap);
    };

    const schedulePhoneMobileHeadlinesPosition = (wrap, preserveScroll = false) => {
        positionPhoneMobileHeadlinesTip(wrap, preserveScroll);
        window.requestAnimationFrame(() => positionPhoneMobileHeadlinesTip(wrap, preserveScroll));
    };

    const repositionOpenPhoneMobileHeadlines = () => {
        if (!isPhoneMobileHeadlinesViewport()) {
            return;
        }
        document
            .querySelectorAll(".full-results-wrap .tip-wrap.headlines-tip .hl-tip-cb:checked")
            .forEach((checkbox) => {
                const wrap = checkbox.closest(".tip-wrap.headlines-tip");
                if (wrap) {
                    schedulePhoneMobileHeadlinesPosition(wrap, true);
                }
            });
    };

    const positionResponsiveHeadlinesTip = (wrap) => {
        if (!usesTabletProHeadlinesPopup() || !wrap) {
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
        updateHeadlinesHeading(wrap);

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
        if (!usesTabletProHeadlinesPopup()) {
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

    const getGenericTooltipSlot = () => {
        const header = document.querySelector('[data-testid="stHeader"]');
        const headerBottom = header ? header.getBoundingClientRect().bottom : 0;
        let viewLeft = VIEWPORT_PAD;
        const viewRight = window.innerWidth - VIEWPORT_PAD;
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && sidebar.getAttribute("aria-expanded") === "true") {
            const sidebarRight = sidebar.getBoundingClientRect().right;
            viewLeft = Math.max(viewLeft, Math.round(sidebarRight + VIEWPORT_PAD));
        }
        const viewTop = Math.max(VIEWPORT_PAD, Math.round(headerBottom + VIEWPORT_PAD));
        const bottomPad =
            window.innerWidth <= MOBILE_MAX ? MOBILE_HEADLINES_BOTTOM_TAP_PAD : VIEWPORT_PAD;
        const viewBottom = window.innerHeight - bottomPad;
        const width = Math.round(
            Math.min(viewRight - viewLeft, Math.max(280, window.innerWidth - 2 * VIEWPORT_PAD))
        );
        const left = Math.round(viewLeft + Math.max(0, (viewRight - viewLeft - width) / 2));
        const top = viewTop;
        const maxHeight = Math.max(120, viewBottom - top);
        return { top, left, width, maxHeight };
    };

    const positionGenericTooltip = (wrap) => {
        if (isDesktopLayoutViewport() || !wrap) {
            return;
        }
        const tip = wrap.querySelector(":scope > .tip-text");
        if (!tip) {
            return;
        }
        const slot = getGenericTooltipSlot();
        tip.style.setProperty("--tip-fixed-top", `${slot.top}px`);
        tip.style.setProperty("--tip-fixed-left", `${slot.left}px`);
        tip.style.setProperty("--tip-fixed-width", `${slot.width}px`);
        tip.style.setProperty("--tip-fixed-max-height", `${slot.maxHeight}px`);
        tip.style.setProperty("right", "auto", "important");
        tip.style.setProperty("bottom", "auto", "important");
        tip.style.setProperty("transform", "none", "important");
    };

    const scheduleGenericTooltipPosition = (wrap) => {
        positionGenericTooltip(wrap);
        window.requestAnimationFrame(() => positionGenericTooltip(wrap));
    };

    const repositionVisibleGenericTooltips = () => {
        if (isDesktopLayoutViewport()) {
            return;
        }
        document.querySelectorAll(".tip-wrap:not(.headlines-tip)").forEach((wrap) => {
            const tip = wrap.querySelector(":scope > .tip-text");
            if (!tip) {
                return;
            }
            const styles = getComputedStyle(tip);
            if (styles.visibility !== "hidden" && styles.opacity !== "0") {
                scheduleGenericTooltipPosition(wrap);
            }
        });
    };

    const handleGenericTooltipInteraction = (event) => {
        if (isDesktopLayoutViewport()) {
            return;
        }
        const wrap = event.target?.closest?.(".tip-wrap:not(.headlines-tip)");
        if (!wrap) {
            return;
        }
        scheduleGenericTooltipPosition(wrap);
    };

    if (!window.__scoopGenericTooltipBound) {
        window.__scoopGenericTooltipBound = true;
        document.addEventListener("mouseover", handleGenericTooltipInteraction, true);
        document.addEventListener("touchstart", handleGenericTooltipInteraction, {
            passive: true,
            capture: true,
        });
        window.addEventListener("resize", repositionVisibleGenericTooltips, { passive: true });
        const bindGenericTooltipSidebarObserver = () => {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) {
                return false;
            }
            const genericTooltipSidebarObserver = new MutationObserver(repositionVisibleGenericTooltips);
            genericTooltipSidebarObserver.observe(sidebar, {
                attributes: true,
                attributeFilter: ["aria-expanded", "class"],
            });
            return true;
        };
        if (!bindGenericTooltipSidebarObserver()) {
            let attempts = 0;
            const retry = window.setInterval(() => {
                attempts += 1;
                if (bindGenericTooltipSidebarObserver() || attempts >= 12) {
                    window.clearInterval(retry);
                }
            }, 250);
        }
    }

    if (!window.__scoopTooltipScrollBound) {
        window.__scoopTooltipScrollBound = true;

        window.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
        document.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
        document.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
        document.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
        document.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
    }

    if (window.__scoopDesktopHeadlinesBindVersion !== 32) {
        window.__scoopDesktopHeadlinesBindVersion = 32;

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
            repositionOpenPhoneMobileHeadlines();
            repositionOpenResponsiveHeadlines();
            repositionVisibleGenericTooltips();
        };

        window.__scoopDesktopHeadlinesWindowScroll = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            repositionOpenPhoneMobileHeadlines();
        };

        window.__scoopDesktopHeadlinesDocScroll = () => {
            window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            repositionOpenPhoneMobileHeadlines();
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

        window.__scoopDesktopHeadlinesLabelClick = (event) => {
            if (!isDesktopLayoutViewport()) {
                return;
            }
            if (!event.target.closest(".hl-tip-count")) {
                return;
            }
            const scrollEl =
                document.querySelector('[data-testid="stAppViewContainer"]') ||
                document.scrollingElement ||
                document.documentElement;
            const savedScrollTop = scrollEl.scrollTop;
            window.requestAnimationFrame(() => {
                scrollEl.scrollTop = savedScrollTop;
                window.scrollTo(0, savedScrollTop);
                window.__scoopDesktopHeadlinesApi?.repositionOpenDesktopHeadlines();
            });
        };
        document.addEventListener("click", window.__scoopDesktopHeadlinesLabelClick, true);
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

        const bindResponsiveHeadlinesObserver = () => {
            const sidebar = document.querySelector('section[data-testid="stSidebar"]');
            if (!sidebar) {
                return false;
            }
            const sidebarHeadlinesObserver = new MutationObserver(repositionOpenResponsiveHeadlines);
            sidebarHeadlinesObserver.observe(sidebar, {
                attributes: true,
                attributeFilter: ["aria-expanded", "class"],
            });
            return true;
        };
        if (!bindResponsiveHeadlinesObserver()) {
            let attempts = 0;
            const retry = window.setInterval(() => {
                attempts += 1;
                if (bindResponsiveHeadlinesObserver() || attempts >= 12) {
                    window.clearInterval(retry);
                }
            }, 250);
        }
    }
})();
"""


_DESKTOP_SIDEBAR_JS = (
    """
(() => {
"""
    + _RESPONSIVE_DOC_HELPER_JS
    + """
    const doc = __scoopGetAppDoc();
    const appWin = __scoopGetAppWin();
    const layout = () => appWin.__scoopLayout;

    const expandSidebarIfNeeded = () => {
        const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (!sidebar || sidebar.getAttribute("aria-expanded") !== "false") {
            return;
        }
        const expand =
            doc.querySelector('[data-testid="stExpandSidebarButton"]') ||
            doc.querySelector('[data-testid="collapsedControl"] button') ||
            doc.querySelector('[data-testid="collapsedControl"]');
        if (expand) {
            expand.click();
        }
    };

    const ensureDesktopSidebarOpen = () => {
        if (!layout()?.isDesktopViewport()) {
            layout()?.syncSidebarLayout();
            return;
        }
        expandSidebarIfNeeded();
        layout()?.syncSidebarLayout();
    };

    if (appWin.__scoopDesktopSidebarBound) {
        return;
    }
    appWin.__scoopDesktopSidebarBound = true;

    ensureDesktopSidebarOpen();

    doc.addEventListener(
        "click",
        (event) => {
            if (!layout()?.isDesktopViewport()) {
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
})();
"""
)

_COMBINED_PAGE_JS = (
    _TOOLTIP_SCROLL_JS
    + _RESPONSIVE_LAYOUT_CORE_JS
    + _RESPONSIVE_LAYOUT_SYNC_JS
    + _RESPONSIVE_SIDEBAR_JS
    + _ANALYZE_RETURN_NAV_JS
    + _DESKTOP_SIDEBAR_JS
)

_RESPONSIVE_LAYOUT_SCRIPTS = (
    f"<script>{_RESPONSIVE_LAYOUT_CORE_JS}</script>"
    f"<script>{_RESPONSIVE_LAYOUT_SYNC_JS}</script>"
    f"<script>{_RESPONSIVE_SIDEBAR_JS}</script>"
    f"<script>{_ANALYZE_RETURN_NAV_JS}</script>"
    f"<script>{_DESKTOP_SIDEBAR_JS}</script>"
)


def _inject_responsive_bootstrap_css() -> str:
    css_json = json.dumps(RESPONSIVE_SIDEBAR_BOOTSTRAP)
    return f"""
<script>
(function() {{
    const css = {css_json};
    const id = "scoop-responsive-sidebar-bootstrap-css";
    function apply(targetDoc) {{
        if (!targetDoc || !targetDoc.documentElement) {{
            return;
        }}
        let el = targetDoc.getElementById(id);
        if (!el) {{
            el = targetDoc.createElement("style");
            el.id = id;
            (targetDoc.head || targetDoc.documentElement).appendChild(el);
        }}
        el.textContent = css;
    }}
    const parentDoc = window.parent && window.parent.document ? window.parent.document : null;
    const appDoc = parentDoc || document;
    apply(appDoc);
    if (parentDoc && parentDoc !== document) {{
        apply(document);
    }}

    const appWin = appDoc.defaultView || window;
    if (/Analyze/i.test(appWin.location.pathname || "")) {{
        appWin.__scoopAnalyzeSidebarUserOpened = false;
    }}
    if (!appWin.__scoopAnalyzeLinksBound) {{
        appWin.__scoopAnalyzeLinksBound = true;
        appDoc.addEventListener(
            "click",
            (event) => {{
                const link = event.target.closest("a.fr-analyze-link");
                if (!link) {{
                    return;
                }}
                const ticker = (link.getAttribute("data-ticker") || "").trim();
                if (!ticker) {{
                    return;
                }}
                event.preventDefault();
                event.stopImmediatePropagation();
                let theme = "light";
                try {{
                    localStorage.removeItem("scoop-theme");
                    const stored = sessionStorage.getItem("scoop-theme");
                    if (stored === "dark") {{
                        theme = "dark";
                    }}
                }} catch (e) {{}}
                try {{
                    appWin.__scoopAnalyzeSidebarUserOpened = false;
                    appWin.__scoopSuppressSidebarExpand = Date.now() + 15000;
                    if (typeof appWin.__scoopClearResponsiveExpandTimers === "function") {{
                        appWin.__scoopClearResponsiveExpandTimers();
                    }}
                    const sidebar = doc.querySelector('section[data-testid="stSidebar"]');
                    if (sidebar) {{
                        sidebar.setAttribute("aria-expanded", "false");
                    }}
                    appWin.__scoopLayout?.syncSidebarLayout?.();
                    appWin.__scoopLayout?.collapseSidebar?.();
                }} catch (e) {{}}
                appWin.location.href =
                    "/Analyze?ticker="
                    + encodeURIComponent(ticker)
                    + "&theme="
                    + encodeURIComponent(theme)
                    + "&from="
                    + encodeURIComponent(appWin.location.pathname || "/NYSE_Top_10");
            }},
            true
        );
    }}
}})();
</script>
"""


def install_responsive_layout_bootstrap() -> None:
    """Early CSS + layout sync so mobile/tablet first paint uses overlay sidebar."""
    st.html(
        _inject_responsive_bootstrap_css()
        + f"<script>{_RESPONSIVE_LAYOUT_CORE_JS}</script>"
        + f"<script>{_RESPONSIVE_LAYOUT_SYNC_JS}</script>",
        unsafe_allow_javascript=True,
    )


def install_responsive_sidebar_handler() -> None:
    """Responsive sidebar close (tablet) + always-open sidebar (desktop)."""
    st.html(
        _inject_responsive_bootstrap_css()
        + f"<style id='scoop-desktop-sidebar-layout-css'>{DESKTOP_SIDEBAR_LAYOUT}</style>"
        + f"<style id='scoop-desktop-zoom-layout-css'>{DESKTOP_ZOOM_LAYOUT}</style>"
        + f"<style id='scoop-sidebar-nav-compact-css'>{SIDEBAR_NAV_COMPACT}</style>"
        + _RESPONSIVE_LAYOUT_SCRIPTS,
        unsafe_allow_javascript=True,
    )


def install_tooltip_scroll_handler() -> None:
    """Inject mobile headline CSS; HTML backdrop label closes panel on outside tap."""
    st.html(
        f"<style id='scoop-mobile-headlines-css'>{_MOBILE_HEADLINES_CSS}</style>"
        f"<style id='scoop-mobile-tablet-card-order-css'>{_MOBILE_TABLET_CARD_ORDER_CSS}</style>"
        f"<style id='scoop-tablet-headlines-css'>{_TABLET_HEADLINES_POPUP_CSS}</style>"
        f"<style id='scoop-desktop-headlines-css'>{_DESKTOP_HEADLINES_CSS}</style>"
        f"<style id='scoop-ipad-mini-surface-duo-headlines-css'>{_IPAD_MINI_SURFACE_DUO_HEADLINES_CSS}</style>"
        f"<style id='scoop-asus-zenbook-fold-headlines-css'>{_ASUS_ZENBOOK_FOLD_HEADLINES_CSS}</style>"
        f"<style id='scoop-mobile-phone-headlines-fixed-css'>{_MOBILE_PHONE_HEADLINES_FIXED_CSS}</style>"
        f"<style id='scoop-responsive-generic-tooltip-css'>{_RESPONSIVE_GENERIC_TOOLTIP_CSS}</style>"
        f"<style id='scoop-dark-responsive-tip-underline-css'>{_DARK_RESPONSIVE_TIP_UNDERLINE_CSS}</style>"
        f"<style id='scoop-dark-popup-outline-css'>{_DARK_POPUP_OUTLINE_CSS}</style>"
        + _inject_responsive_bootstrap_css()
        + f"<style id='scoop-desktop-sidebar-layout-css'>{DESKTOP_SIDEBAR_LAYOUT}</style>"
        + f"<style id='scoop-desktop-zoom-layout-css'>{DESKTOP_ZOOM_LAYOUT}</style>"
        + f"<style id='scoop-sidebar-nav-compact-css'>{SIDEBAR_NAV_COMPACT}</style>"
        + f"<script>{_COMBINED_PAGE_JS}</script>",
        unsafe_allow_javascript=True,
    )
    from theme_mode import inject_dark_mode_styles

    inject_dark_mode_styles()
