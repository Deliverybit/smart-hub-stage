import streamlit as st

_MOBILE_HEADLINES_CSS = """
@media (max-width: 768px) {
    .stMarkdown .tip-wrap.headlines-tip {
        cursor: default !important;
    }
    .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
        position: absolute !important;
        opacity: 0 !important;
        width: 0 !important;
        height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        pointer-events: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
        cursor: pointer !important;
        pointer-events: auto !important;
        -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
        text-decoration: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop {
        display: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop {
        display: block !important;
        position: fixed !important;
        inset: 0 !important;
        z-index: 100001 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        background: rgba(15, 23, 42, 0.12) !important;
        cursor: default !important;
        pointer-events: auto !important;
        touch-action: manipulation !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .hl-tip-backdrop span {
        display: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:not(:has(.hl-tip-cb:checked)) .tip-text {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {
        display: flex !important;
        flex-direction: column !important;
        position: fixed !important;
        left: max(0.75rem, env(safe-area-inset-left, 0px)) !important;
        right: max(0.75rem, env(safe-area-inset-right, 0px)) !important;
        top: max(4rem, calc(env(safe-area-inset-top, 0px) + 0.65rem)) !important;
        bottom: auto !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: none !important;
        height: auto !important;
        max-height: min(calc(10.5rem + 300px), calc(100dvh - 5rem)) !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        touch-action: auto !important;
        text-align: left !important;
        transform: none !important;
        z-index: 100002 !important;
        background: #111827 !important;
        border: 1px solid #334155 !important;
        border-radius: 8px !important;
        box-sizing: border-box !important;
        box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
        flex: 0 0 auto !important;
        position: relative !important;
        top: auto !important;
        margin: 0 !important;
        padding: 0.45rem 0.6rem !important;
        background: #1e1e2f !important;
        color: #ffffff !important;
        font-weight: 700 !important;
        font-size: calc(0.82rem + 4pt) !important;
        line-height: 1.15 !important;
        text-align: left !important;
        border-bottom: 1px solid #334155 !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
        flex: 1 1 auto !important;
        min-height: 0 !important;
        height: calc(7.25rem + 300px) !important;
        max-height: calc(7.25rem + 300px) !important;
        overflow-x: hidden !important;
        overflow-y: scroll !important;
        -webkit-overflow-scrolling: touch !important;
        touch-action: pan-y !important;
        overscroll-behavior-y: contain !important;
        scrollbar-gutter: stable !important;
        scrollbar-width: thin !important;
        scrollbar-color: #94a3b8 #1e293b !important;
        padding: 0.28rem 0.35rem 0.35rem 0.55rem !important;
        text-align: left !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar {
        width: 8px !important;
        -webkit-appearance: none !important;
        display: block !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-track {
        background: #1e293b !important;
        border-radius: 4px !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll::-webkit-scrollbar-thumb {
        background: #94a3b8 !important;
        border-radius: 4px !important;
        min-height: 28px !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-list {
        display: flex !important;
        flex-direction: column !important;
        gap: 0.28rem !important;
        min-width: 0 !important;
        text-align: left !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
        display: block !important;
        padding: 0.32rem 0.38rem !important;
        margin: 0 !important;
        border: 1px solid rgba(148, 163, 184, 0.28) !important;
        border-radius: 5px !important;
        background: rgba(15, 23, 42, 0.45) !important;
        line-height: 1.28 !important;
        font-size: calc(0.72rem + 4pt) !important;
        min-width: 0 !important;
        text-align: left !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }
    .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
        display: block !important;
        color: #93c5fd !important;
        font-size: calc(0.72rem + 4pt) !important;
        text-align: left !important;
        text-decoration: underline !important;
        text-underline-offset: 0.12em !important;
        word-break: break-word !important;
        overflow-wrap: anywhere !important;
        touch-action: manipulation !important;
    }
}
"""

_TOOLTIP_SCROLL_JS = """
(() => {
    const root = document.documentElement;
    const className = "scoop-tooltip-scrolling";
    if (window.__scoopTooltipScrollBound) {
        return;
    }
    window.__scoopTooltipScrollBound = true;

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

    window.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
    document.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
    document.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
    document.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
    document.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
    document.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
})();
"""


def install_tooltip_scroll_handler() -> None:
    """Inject mobile headline CSS; HTML backdrop label closes panel on outside tap."""
    st.html(
        f"<style id='scoop-mobile-headlines-css'>{_MOBILE_HEADLINES_CSS}</style>"
        f"<script>{_TOOLTIP_SCROLL_JS}</script>",
        unsafe_allow_javascript=True,
    )
