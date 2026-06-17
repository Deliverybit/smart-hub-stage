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

            if (root.dataset.scoopTooltipScrollHandler === "1") {
                return;
            }
            root.dataset.scoopTooltipScrollHandler = "1";

            const hideTooltips = () => {
                root.classList.add(className);
                doc.body.classList.add(className);

                if (doc.activeElement && typeof doc.activeElement.blur === "function") {
                    doc.activeElement.blur();
                }
            };

            const allowTooltip = (event) => {
                const target = event.target;
                if (target && target.closest && target.closest(".tip-wrap")) {
                    root.classList.remove(className);
                    doc.body.classList.remove(className);
                }
            };

            parentWindow.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("scroll", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("wheel", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("touchmove", hideTooltips, { passive: true, capture: true });
            doc.addEventListener("pointerdown", allowTooltip, { passive: true, capture: true });
            doc.addEventListener("touchstart", allowTooltip, { passive: true, capture: true });
            doc.addEventListener("mousemove", allowTooltip, { passive: true, capture: true });
        })();
        </script>
        """,
        height=0,
        width=0,
    )
