import streamlit.components.v1 as components


def install_tooltip_scroll_handler() -> None:
    """Hide sticky mobile hover tooltips once the user scrolls the page."""
    components.html(
        """
        <script>
        (() => {
            const parentWindow = window.parent;
            const doc = parentWindow.document;
            const root = doc.documentElement;
            const className = "scoop-tooltip-scrolling";
            const headlineScrollClassName = "scoop-headline-panel-scrolling";
            let headlinePanelScrollTimer = null;

            if (root.dataset.scoopTooltipScrollHandler === "3") {
                return;
            }
            root.dataset.scoopTooltipScrollHandler = "3";

            const elementFromEvent = (event) => {
                const target = event.target;
                if (target && target.nodeType === Node.ELEMENT_NODE) {
                    return target;
                }
                if (target && target.parentElement) {
                    return target.parentElement;
                }
                if (event.composedPath) {
                    return event.composedPath().find(
                        (node) => node && node.nodeType === Node.ELEMENT_NODE
                    );
                }
                return null;
            };

            const isHeadlinePanelScroll = (event) => {
                const element = elementFromEvent(event);
                return Boolean(element && element.closest(".headlines-tip .tip-text"));
            };

            const keepHeadlinePanelOpen = (event) => {
                if (!isHeadlinePanelScroll(event)) {
                    return;
                }
                root.classList.add(headlineScrollClassName);
                doc.body.classList.add(headlineScrollClassName);
                root.classList.remove(className);
                doc.body.classList.remove(className);
                parentWindow.clearTimeout(headlinePanelScrollTimer);
                headlinePanelScrollTimer = parentWindow.setTimeout(() => {
                    root.classList.remove(headlineScrollClassName);
                    doc.body.classList.remove(headlineScrollClassName);
                }, 400);
                event.stopPropagation();
            };

            const hideTooltips = (event) => {
                if (event && isHeadlinePanelScroll(event)) {
                    return;
                }

                root.classList.add(className);
                doc.body.classList.add(className);

                if (doc.activeElement && typeof doc.activeElement.blur === "function") {
                    doc.activeElement.blur();
                }
            };

            const allowTooltip = (event) => {
                const element = elementFromEvent(event);
                if (element && element.closest(".tip-wrap")) {
                    root.classList.remove(className);
                    doc.body.classList.remove(className);
                }
            };

            parentWindow.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
            parentWindow.addEventListener("wheel", keepHeadlinePanelOpen, { passive: true, capture: true });
            parentWindow.addEventListener("touchmove", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("scroll", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("wheel", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("touchmove", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("touchmove", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
            doc.addEventListener("pointerdown", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
            doc.addEventListener("touchstart", keepHeadlinePanelOpen, { passive: true, capture: true });
            doc.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
        })();
        </script>
        """,
        height=0,
        width=0,
    )
