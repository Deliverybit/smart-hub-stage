"""Mobile card-layout CSS reused inside the tablet-only breakpoint (769px–1366px)."""

# Tablet-readable type scale (larger than phone, still card layout).
TABLET_TYPE = """
        html, body, [class*="css"] {
            font-size: clamp(21px, 2.35vw, 24px) !important;
            line-height: 1.62 !important;
        }
        h1 { font-size: clamp(2.2rem, 5vw, 3.1rem) !important; line-height: 1.12 !important; }
        h2 { font-size: clamp(1.85rem, 4.2vw, 2.6rem) !important; line-height: 1.18 !important; }
        h3 { font-size: clamp(1.6rem, 3.6vw, 2.15rem) !important; line-height: 1.22 !important; }
        h4 { font-size: clamp(1.4rem, 3.2vw, 1.85rem) !important; line-height: 1.28 !important; }

        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] span,
        [data-testid="stMarkdownContainer"] div,
        .stMarkdown p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        .stAlert p, [data-testid="stAlert"] p,
        .stSuccess p, .stWarning p, .stInfo p, .stError p {
            font-size: clamp(1.2rem, 2.6vw, 1.45rem) !important;
            line-height: 1.65 !important;
        }

        [data-testid="stMetricValue"] > div {
            font-size: clamp(2.35rem, 5.2vw, 3.25rem) !important;
        }
        [data-testid="stMetricLabel"] > div > div > p,
        [data-testid="stMetricLabel"] label {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
        }
        [data-testid="stMetricDelta"] > div {
            font-size: clamp(1.1rem, 2.3vw, 1.3rem) !important;
        }

        .stButton button {
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            padding: 0.95rem 1.35rem !important;
            min-height: 3.1rem !important;
        }
        .stCaption p {
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }

        .disclaimer-footer {
            font-size: clamp(0.88rem, 2vw, 1.02rem) !important;
            line-height: 1.45 !important;
        }
        .disclaimer-footer strong {
            font-size: clamp(0.9rem, 2.05vw, 1.04rem) !important;
        }

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-left: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-right: var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) !important;
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 2.75rem) !important;
            padding-bottom: 2.5rem !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stMarkdownContainer"],
        [data-testid="stMarkdownContainer"] > div {
            max-width: 100% !important;
        }

        div[data-testid="stCheckbox"] {
            margin-bottom: 1.25rem !important;
        }
"""

# Card-overlay headlines panel — shared behavior for mobile (≤768px) and tablet (769–1366px).
MOBILE_HEADLINES_CARD_OVERLAY = """
        /* Headlines: tap count toggles checkbox; card overlay at top of row (same as tablet). */
        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
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
            position: absolute !important;
            left: 0 !important;
            right: 0 !important;
            top: 0 !important;
            bottom: auto !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
            height: auto !important;
            max-height: 100% !important;
            margin: 0 !important;
            padding: 0 !important;
            overflow: hidden !important;
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            text-align: left !important;
            color: #93c5fd !important;
            padding: 0.45rem 0.6rem !important;
            font-size: calc(0.82rem + 4pt) !important;
            font-weight: 700 !important;
            line-height: 1.15 !important;
            background: #1e1e2f !important;
            border-bottom: 1px solid #334155 !important;
        }
        .stMarkdown .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {
            flex: 1 1 auto !important;
            min-width: 0 !important;
            max-width: 100% !important;
            min-height: 0 !important;
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
            max-width: 100% !important;
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
"""

# Mobile/tablet only — match desktop Headlines title color (light blue).
MOBILE_TABLET_HL_HEADING_COLOR_CSS = """
@media (max-width: 1366px) {
    .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading,
    html[data-scoop-theme="dark"] .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-heading {
        color: #93c5fd !important;
    }
    html:not([data-scoop-theme="dark"]) .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    html:not([data-scoop-theme="dark"]) .stMarkdown .tip-wrap.headlines-tip .tip-text .hl-tip-line a,
    html:not([data-scoop-theme="dark"]) .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    html:not([data-scoop-theme="dark"]) .stMarkdown .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line a,
    html:not([data-scoop-theme="dark"]) .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line,
    html:not([data-scoop-theme="dark"]) .full-results-wrap .tip-wrap.headlines-tip .tip-text .hl-tip-line a {
        color: #ffffff !important;
    }
}
"""

# Mobile/tablet card field order (desktop table unchanged).
# Order: #, Name, Ticker, Price, 52W Low, % Above Low, 52W High, Exchanges, Headlines, Market Mood, Headline Sentiment
MOBILE_CARD_FIELD_ORDER = """
        /* Full Results card — reorder fields without changing card format/size */
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: flex !important;
            flex-direction: column !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="#"] {
            order: 0 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"],
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] {
            order: 1 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Ticker"] {
            order: 2 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Price"] {
            order: 3 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W Low"] {
            order: 4 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="% Above Low"] {
            order: 5 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="52W High"] {
            order: 6 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Exchanges"] {
            order: 7 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headlines"] {
            order: 8 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Market Mood"] {
            order: 9 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Headline Sentiment"] {
            order: 10 !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Analyze"] {
            order: 11 !important;
        }
"""

_TABLET_ANALYZE_SCOPE = (
    'html body .stApp [data-testid="stAppViewContainer"] .stMarkdown'
)

# Tablet (744–1366px): blue underlined Analyze link, right-aligned in a white card row.
TABLET_ANALYZE_LINK_CSS = f"""
@media (min-width: 744px) and (max-width: 1366px) {{
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table tbody td[data-label="Analyze"] {{
            display: block !important;
            grid-template-columns: minmax(0, 1fr) !important;
            gap: 0 !important;
            margin-top: 0.55rem !important;
            padding: 0.62rem 0.85rem !important;
            border: 1px solid #e5e7eb !important;
            border-radius: 10px !important;
            background: #ffffff !important;
        }}
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table tbody td[data-label="Analyze"] .fr-label {{
            display: none !important;
        }}
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table tbody td[data-label="Analyze"] .fr-val {{
            display: block !important;
            text-align: right !important;
            width: 100% !important;
            min-width: 0 !important;
        }}
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table tbody td[data-label="Analyze"] .fr-analyze-cell {{
            display: flex !important;
            justify-content: space-between !important;
            align-items: center !important;
            width: 100% !important;
            gap: 0.75rem !important;
        }}
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {{
            display: inline-block !important;
            flex: 0 1 auto !important;
            order: 1 !important;
            cursor: help !important;
            border-bottom: 1px dashed #888 !important;
            color: inherit !important;
            font-weight: 600 !important;
            text-decoration: none !important;
        }}
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link,
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:link,
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:visited,
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:hover,
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:active,
        {_TABLET_ANALYZE_SCOPE} .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:focus {{
            display: inline !important;
            visibility: visible !important;
            color: #93c5fd !important;
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            border-bottom: none !important;
            border-radius: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            text-decoration: underline !important;
            text-underline-offset: 0.14em !important;
            font-weight: 600 !important;
            font-size: inherit !important;
            line-height: inherit !important;
            white-space: nowrap !important;
            box-shadow: none !important;
            outline: none !important;
            cursor: pointer !important;
            flex: 0 0 auto !important;
            order: 2 !important;
            margin-left: auto !important;
        }}
}}
"""

# Phone (≤743px): same Analyze link as tablet (headlines-heading blue, asset URL).
PHONE_ANALYZE_MOBILE_TIP_CSS = """
@media (max-width: 743px) {
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link,
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:link,
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:visited,
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:hover,
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:active,
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:focus {
            display: inline !important;
            visibility: visible !important;
            color: #93c5fd !important;
            background: transparent !important;
            border: none !important;
            border-bottom: none !important;
            padding: 0 !important;
            margin: 0 !important;
            text-decoration: underline !important;
            text-underline-offset: 0.14em !important;
            font-weight: 600 !important;
            cursor: pointer !important;
            pointer-events: auto !important;
        }
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {
            display: none !important;
        }
}
"""

# Last-wins mobile/tablet Analyze control: headlines-heading blue + real Analyze URL.
_MOBILE_TABLET_ANALYZE_LINK_FINAL = """
@media (max-width: 1366px) {
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:link,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:visited,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:hover,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:active,
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell a.fr-analyze-link:focus {
        display: inline !important;
        visibility: visible !important;
        opacity: 1 !important;
        color: #93c5fd !important;
        background: transparent !important;
        border: none !important;
        text-decoration: underline !important;
        text-underline-offset: 0.14em !important;
        font-weight: 600 !important;
        cursor: pointer !important;
        pointer-events: auto !important;
    }
    html body .stApp [data-testid="stAppViewContainer"] .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {
        display: none !important;
    }
}
"""

# Mobile/tablet: generic info tooltips mirror desktop (above trigger, CSS :hover only).
# Company/name/commodity values use the same popup positioning as other field tooltips.
_RESPONSIVE_TIP_SCOPE = (
    "html body .stApp [data-testid=\"stAppViewContainer\"] .stMarkdown"
)
_NAME_VALUE_LABELS = ("Company", "Name", "Commodity")
_NAME_VALUE_TIP_SELECTOR = (
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip), '
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip), '
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip)'
)


def _name_value_tip_selectors(scope: str, suffix: str = "") -> str:
    """Build comma-separated selectors; each label gets its own full path + suffix."""
    parts = []
    for label in _NAME_VALUE_LABELS:
        parts.append(
            f'{scope} .full-results-wrap .full-results-table tbody '
            f'td[data-label="{label}"] .fr-val .tip-wrap:not(.headlines-tip){suffix}'
        )
    return ",\n        ".join(parts)


_GENERIC_TIP_ACTIVE = (
    ".tip-wrap:not(.headlines-tip):hover, "
    ".tip-wrap:not(.headlines-tip):active, "
    ".tip-wrap:not(.headlines-tip):focus-within"
)
RESPONSIVE_GENERIC_TOOLTIP_LAYOUT = f"""
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) {{
            position: relative !important;
            cursor: help !important;
            border-bottom: 1px dashed #888 !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip) .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
        {_RESPONSIVE_TIP_SCOPE} [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip) .tip-text {{
            visibility: hidden !important;
            opacity: 0 !important;
            position: absolute !important;
            bottom: calc(100% + 12px) !important;
            left: 50% !important;
            right: auto !important;
            top: auto !important;
            transform: translateX(-50%) !important;
            width: max-content !important;
            min-width: min(360px, calc(100vw - 2rem)) !important;
            max-width: min(700px, calc(100vw - 2rem)) !important;
            background: #1e1e2f !important;
            color: #e2e8f0 !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 16px 20px !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            font-weight: 400 !important;
            white-space: normal !important;
            z-index: 100001 !important;
            box-shadow: 0 4px 16px rgba(0,0,0,0.45) !important;
            pointer-events: auto !important;
            transition: opacity 0.15s ease-in-out, visibility 0.15s ease-in-out !important;
            max-height: min(45vh, 22rem) !important;
            overflow-y: auto !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text::before {{
            content: "" !important;
            display: block !important;
            position: absolute !important;
            bottom: -14px !important;
            left: 0 !important;
            width: 100% !important;
            height: 14px !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text::after {{
            content: "" !important;
            display: block !important;
            position: absolute !important;
            top: 100% !important;
            left: 50% !important;
            transform: translateX(-50%) !important;
            border-width: 8px !important;
            border-style: solid !important;
            border-color: #1e1e2f transparent transparent transparent !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):hover .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):active .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):focus-within .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text:hover,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):hover .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):active .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):hover .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):active .tip-text,
        {_RESPONSIVE_TIP_SCOPE} [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):hover .tip-text,
        {_RESPONSIVE_TIP_SCOPE} [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):active .tip-text {{
            visibility: visible !important;
            opacity: 1 !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody tr:has({_GENERIC_TIP_ACTIVE}) {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100003 !important;
        }}
        .stMarkdown .full-results-wrap:has({_GENERIC_TIP_ACTIVE}) {{
            overflow: visible !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody td:has({_GENERIC_TIP_ACTIVE}) {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100004 !important;
        }}
        [data-testid="stMarkdownContainer"]:has({_GENERIC_TIP_ACTIVE}) {{
            overflow: visible !important;
        }}
"""

NAME_VALUE_TOOLTIP_PAGE_MARKER = (
    "/* Name/Company/Commodity: same above-trigger popup as other mobile/tablet tooltips. */"
)
NAME_VALUE_TOOLTIP_PAGE_SNIPPET = ""

# Dark mobile/tablet: company/name/commodity popup + underline beat stale page CSS.
_DARK_RESPONSIVE_TIP_SCOPE = (
    'body .stApp [data-testid="stAppViewContainer"] .stMarkdown'
)
DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS = f"""
@media (max-width: 1366px) {{
html[data-scoop-theme="dark"] {_DARK_RESPONSIVE_TIP_SCOPE} {_NAME_VALUE_TIP_SELECTOR} {{
    border-bottom: 2px dashed #ffffff !important;
}}
html[data-scoop-theme="dark"] {_name_value_tip_selectors(_DARK_RESPONSIVE_TIP_SCOPE, " .tip-text")} {{
    background: #0f172a !important;
    background-color: #0f172a !important;
    color: #e5e7eb !important;
    border: 2px solid #ffffff !important;
}}
html[data-scoop-theme="dark"] {_name_value_tip_selectors(_DARK_RESPONSIVE_TIP_SCOPE, " .tip-text::after")} {{
    border-color: #0f172a transparent transparent transparent !important;
}}
}}
"""

# Phone mobile (≤768px): viewport-centered popup above tap/hover for all generic tooltips.
_MOBILE_FIXED_GENERIC_TIP_TEXT = f"""
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text {{
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            top: var(--scoop-mobile-tip-top, -10000px) !important;
            width: min(18rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(18rem, calc(100vw - 2rem)) !important;
            margin: 0 !important;
            z-index: 100002 !important;
            background: #1e1e2f !important;
            background-color: #1e1e2f !important;
            color: #e2e8f0 !important;
            border: 1px solid #555 !important;
            border-radius: 8px !important;
            padding: 16px 20px !important;
            font-size: 0.95rem !important;
            line-height: 1.5 !important;
            font-weight: 400 !important;
            white-space: normal !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.45) !important;
            pointer-events: none !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
        }}
"""

# iPhone SE (≤375px): reinforce viewport centering — measureMobileGenericTipHeight must
# not set inline left on this width (Safari can keep it and shift the popup off-screen).
_IPHONE_SE_FIXED_GENERIC_TIP_TEXT = f"""
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text {{
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            transform: translateX(-50%) !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }}
"""

# Other mobile (376px–768px): same viewport centering reinforcement as iPhone SE.
_OTHER_MOBILE_FIXED_GENERIC_TIP_TEXT = f"""
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text {{
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            transform: translateX(-50%) !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }}
"""

# Mobile (≤768px): JS-controlled open/close — suppress sticky :hover/:active show.
_MOBILE_GENERIC_TIP_OPEN_CLOSE_CSS = f"""
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):focus-within .tip-text {{
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open .tip-text {{
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }}
"""

# Tablet (769–1366px): beat page-level hover/scroll rules so JS tap-open stays visible.
_TABLET_PAGE_TIP_SCOPE = (
    'html body .stApp [data-testid="stAppViewContainer"] .stMarkdown'
)
_TABLET_GENERIC_TIP_RELIABILITY_CSS = f"""
        {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):focus-within .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open) .tip-text:hover,
        {_TABLET_PAGE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):hover .tip-text,
        {_TABLET_PAGE_TIP_SCOPE} [data-testid="stHorizontalBlock"] .tip-wrap:not(.headlines-tip):not(.scoop-mobile-tip-open):active .tip-text {{
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }}
        html.scoop-tooltip-scrolling {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open .tip-text,
        body.scoop-tooltip-scrolling {_TABLET_PAGE_TIP_SCOPE} .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open .tip-text {{
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }}
"""

RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS = f"""
@media (max-width: 768px) {{
{_MOBILE_FIXED_GENERIC_TIP_TEXT}
{_MOBILE_GENERIC_TIP_OPEN_CLOSE_CSS}
}}
@media (max-width: 375px) {{
{_IPHONE_SE_FIXED_GENERIC_TIP_TEXT}
}}
@media (min-width: 376px) and (max-width: 768px) {{
{_OTHER_MOBILE_FIXED_GENERIC_TIP_TEXT}
}}
@media (min-width: 769px) and (max-width: 1366px) {{
{_MOBILE_FIXED_GENERIC_TIP_TEXT}
{_MOBILE_GENERIC_TIP_OPEN_CLOSE_CSS}
{_OTHER_MOBILE_FIXED_GENERIC_TIP_TEXT}
{_TABLET_GENERIC_TIP_RELIABILITY_CSS}
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text::before,
        {_RESPONSIVE_TIP_SCOPE} .tip-wrap:not(.headlines-tip) .tip-text::after {{
            content: none !important;
            display: none !important;
            border: 0 !important;
        }}
}}
""" + DARK_RESPONSIVE_NAME_VALUE_TIP_UNDERLINE_CSS

# Shared mobile card layout for screener Full Results + Top Picks + tooltips/headlines.
TABLET_SCREENER_MOBILE_LAYOUT = (
    """
        .stApp { overflow-x: hidden !important; }
"""
    + TABLET_TYPE
    + RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
    + """

        .stMarkdown .full-results-wrap .full-results-table .fr-label {
            display: inline-block !important;
            font-weight: 800 !important;
            color: #334155 !important;
            font-size: clamp(1.1rem, 2.4vw, 1.32rem) !important;
        }

        [data-testid="stMarkdownContainer"] table th,
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stTable"] th,
        [data-testid="stTable"] td {
            padding-top: clamp(0.72rem, 1.8vw, 1rem) !important;
            padding-bottom: clamp(0.72rem, 1.8vw, 1rem) !important;
            line-height: 1.55 !important;
            vertical-align: top !important;
        }
        [data-testid="stMarkdownContainer"] table td,
        [data-testid="stMarkdownContainer"] table th {
            font-size: clamp(1.08rem, 2.4vw, 1.28rem) !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        [data-testid="stHorizontalBlock"] > div:has([data-testid="stMetric"]) {
            background: #ffffff !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            padding: 1rem 1.05rem 1.1rem 1.05rem !important;
            margin: 0 0 1.15rem 0 !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
        }
        .stApp div[data-testid="metric-container"] {
            margin: 0 !important;
            padding: 0.85rem 0.95rem 0.75rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-bottom: none !important;
            border-radius: 14px 14px 0 0 !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
            font-size: 1.35rem !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricValue"] > div {
            font-size: 2.35rem !important;
            line-height: 1.1 !important;
        }
        .stApp div[data-testid="metric-container"] [data-testid="stMetricDelta"] > div {
            font-size: 1.25rem !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] {
            margin: 0 0 1.2rem 0 !important;
            padding: 0.7rem 0.95rem 0.95rem 0.95rem !important;
            border: 1px solid #e2e8f0 !important;
            border-top: none !important;
            border-radius: 0 0 14px 14px !important;
            background: #ffffff !important;
        }
        .stApp div[data-testid="metric-container"] + div[data-testid="stMarkdownContainer"] div {
            font-size: 1.3rem !important;
            line-height: 1.58 !important;
        }

        .stMarkdown .full-results-mobile-legend {
            display: block !important;
            margin: 0 0 1.1rem 0 !important;
            padding: 0.8rem 0.9rem !important;
            border: 1px solid #e2e8f0 !important;
            border-radius: 10px !important;
            background: #f8fafc !important;
            font-size: clamp(1.05rem, 2.2vw, 1.22rem) !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row {
            margin-bottom: 0.72rem !important;
            padding-bottom: 0.72rem !important;
            border-bottom: 1px solid #e5e7eb !important;
        }
        .stMarkdown .full-results-mobile-legend .fr-mobile-tip-row:last-child {
            border-bottom: none !important;
            margin-bottom: 0 !important;
            padding-bottom: 0 !important;
        }
        .stMarkdown .full-results-mobile-legend p {
            margin: 0.4rem 0 0 0 !important;
            color: #334155 !important;
            line-height: 1.5 !important;
            font-size: clamp(1.02rem, 2.1vw, 1.18rem) !important;
        }
        .stMarkdown .full-results-mobile-legend strong {
            color: #1e293b !important;
            font-size: clamp(1.08rem, 2.25vw, 1.24rem) !important;
        }

        .stMarkdown .full-results-wrap {
            margin-left: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            margin-right: calc(-1 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            width: calc(100% + 2 * var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem))) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 var(--scoop-tablet-gutter, clamp(0.85rem, 2.5vw, 1.1rem)) max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
        }

        /* Index banner cards: use full content width on tablet (desktop keeps inline 50%). */
        [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"] {
            max-width: 100% !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        .stMarkdown .full-results-wrap .full-results-table {
            display: block !important;
            width: 100% !important;
            border-collapse: separate !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody {
            display: block !important;
        }
        .stMarkdown .full-results-wrap .full-results-table thead {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr {
            display: block !important;
            width: 100% !important;
            margin: 0 0 1.2rem 0 !important;
            padding: 0.85rem 1rem 0.95rem 1rem !important;
            border: 2px solid #cbd5e1 !important;
            border-left: 6px solid #22c55e !important;
            border-radius: 14px !important;
            background: #ffffff !important;
            box-shadow: 0 6px 18px rgba(15, 23, 42, 0.10) !important;
            box-sizing: border-box !important;
            overflow: hidden !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td {
            position: relative !important;
            display: grid !important;
            grid-template-columns: minmax(0, 42%) minmax(0, 58%) !important;
            gap: 0.45rem 0.75rem !important;
            align-items: start !important;
            padding: 0.58rem 0 !important;
            border: none !important;
            border-bottom: 1px solid #e5e7eb !important;
            font-size: clamp(1.12rem, 2.5vw, 1.38rem) !important;
            line-height: 1.5 !important;
            width: 100% !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody tr td:last-child {
            border-bottom: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td::before {
            content: "" !important;
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label {
            font-weight: 700 !important;
            color: #475569 !important;
            min-width: 0 !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-label .tip-wrap {
            display: inline-block !important;
            max-width: 100% !important;
            white-space: normal !important;
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap {
            position: relative !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val {
            min-width: 0 !important;
            text-align: right !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }

        .stMarkdown .tip-wrap.headlines-tip { cursor: default !important; }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-cb {
            position: absolute !important;
            opacity: 0 !important;
            width: 0 !important;
            height: 0 !important;
            margin: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-count {
            cursor: pointer !important;
            pointer-events: auto !important;
            -webkit-tap-highlight-color: rgba(34, 197, 94, 0.2) !important;
            text-decoration: none !important;
            font-size: clamp(1.08rem, 2.3vw, 1.28rem) !important;
        }
        .stMarkdown .tip-wrap.headlines-tip .hl-tip-backdrop { display: none !important; }
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
            text-align: left !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            touch-action: auto !important;
            transform: none !important;
            position-anchor: none !important;
            anchor-name: none !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            background: #111827 !important;
            border: 1px solid #334155 !important;
            border-radius: 14px !important;
            box-sizing: border-box !important;
            box-shadow: 0 10px 28px rgba(15, 23, 42, 0.35) !important;
            z-index: 100002 !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-heading {
            flex: 0 0 auto !important;
            flex-shrink: 0 !important;
            display: block !important;
            visibility: visible !important;
            position: relative !important;
            z-index: 2 !important;
            text-align: left !important;
            color: #93c5fd !important;
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
            max-width: 100% !important;
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            touch-action: pan-y !important;
            overscroll-behavior-y: contain !important;
            scrollbar-gutter: stable !important;
            scrollbar-width: thin !important;
            scrollbar-color: #94a3b8 #1e293b !important;
            padding: 0.35rem 0.45rem 0.45rem 0.65rem !important;
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
            gap: 0.35rem !important;
            min-width: 0 !important;
            max-width: 100% !important;
            text-align: left !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line {
            display: block !important;
            padding: 0.42rem 0.48rem !important;
            margin: 0 !important;
            border: 1px solid rgba(148, 163, 184, 0.28) !important;
            border-radius: 5px !important;
            background: rgba(15, 23, 42, 0.45) !important;
            line-height: 1.35 !important;
            font-size: calc(0.95rem + 4pt) !important;
            min-width: 0 !important;
            text-align: left !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
        .stMarkdown .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .hl-tip-line a {
            display: block !important;
            color: #93c5fd !important;
            font-size: calc(0.95rem + 4pt) !important;
            text-align: left !important;
            text-decoration: underline !important;
            text-underline-offset: 0.12em !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            touch-action: manipulation !important;
        }
        .stMarkdown .tip-wrap:not(.headlines-tip):hover .tip-text,
        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text:hover {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
"""
    + MOBILE_CARD_FIELD_ORDER
)

TABLET_SIDEBAR = """
        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
            --scoop-tablet-gutter: clamp(0.85rem, 2.5vw, 1.1rem);
            --scoop-sidebar-arrow-size: 32px;
            --scoop-sidebar-arrow-top: 14px;
            --scoop-sidebar-arrow-left: 12px;
        }

        html, body {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
            overflow-x: hidden !important;
        }

        .stApp {
            overflow-x: hidden !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }

        /* Main content uses full viewport width (sidebar overlays when open). */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main {
            width: 100% !important;
            max-width: 100vw !important;
            min-height: 100dvh !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Slide-out sidebar overlays the page (mobile-style). */
        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100%) !important;
            transition: transform 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            top: auto !important;
            left: auto !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            transform: none !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }
        /* Plain Streamlit arrows (Surface Pro 7 / Duo style) — no boxed chrome. */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
            z-index: 1000006 !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button,
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"],
        section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }

        [data-testid="stSidebar"] p,
        [data-testid="stSidebar"] label,
        [data-testid="stSidebar"] span,
        [data-testid="stSidebar"] div {
            font-size: clamp(1.1rem, 2.2vw, 1.32rem) !important;
        }

        .sidebar-brand-text,
        [data-testid="stSidebar"] #scoop-title {
            font-size: clamp(2.4rem, 5.5vw, 3.25rem) !important;
            line-height: 1.05 !important;
        }
        .sidebar-brand {
            margin: 0.15rem -1rem 0.35rem -1rem !important;
            padding: 0.65rem 1rem !important;
            white-space: normal !important;
        }

        [data-testid="stSidebar"] [data-testid="stPageLink"] a,
        [data-testid="stSidebar"] [data-testid="stPageLink"] span,
        [data-testid="stSidebar"] [data-testid="stPageLink"] p {
            font-size: clamp(1.15rem, 2.2vw, 1.42rem) !important;
            line-height: 1.3 !important;
            white-space: normal !important;
            overflow-wrap: anywhere !important;
            word-break: break-word !important;
        }
"""

# iPad / Surface Pro / Nest Hub / Surface Duo: open sidebar sits above Streamlit top bar
# (covers Deploy); collapse toggle stays on top; fully off-screen when closed.
OVERLAY_SIDEBAR_TOPBAR_LAYER = """
        section[data-testid="stSidebar"] {
            top: 0 !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            z-index: 1000010 !important;
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            z-index: 1000009 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            z-index: 1000008 !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stToolbar"] {
            visibility: hidden !important;
            pointer-events: none !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            z-index: 1000012 !important;
        }
"""

# iPad 14 Pro Max (1032×1376 portrait / 1376×1032 landscape): landscape width exceeds
# the 1366px tablet cap and hits desktop split-sidebar; force full off-screen retract.
IPAD_14_PRO_MAX_PORTRAIT_RETRACT = """
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(calc(-100vw - 4px)) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]),
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(calc(-100vw - 4px)) !important;
            visibility: hidden !important;
            pointer-events: none !important;
            opacity: 0 !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            visibility: visible !important;
            opacity: 1 !important;
        }
"""

IPAD_14_PRO_MAX_LANDSCAPE_OVERRIDE = """
        /* Beat desktop (1367px) split-sidebar rules — same specificity, later cascade. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            margin-left: 0 !important;
            display: block !important;
            opacity: 1 !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
        }
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"] {
            transform: translateX(-100vw) !important;
            visibility: hidden !important;
            pointer-events: none !important;
            z-index: 999999 !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            visibility: visible !important;
            pointer-events: auto !important;
            z-index: 1000010 !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            height: auto !important;
            min-height: 100% !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: block !important;
            position: fixed !important;
            inset: 0 !important;
            z-index: 1000009 !important;
            cursor: pointer !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"] {
            display: flex !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
"""

IPAD_14_PRO_MAX_LAYOUT = f"""
    /* ===== iPad 14 Pro Max only — full slide-in retract ===== */
    @media (min-width: 1028px) and (max-width: 1036px) and (min-height: 1370px) {{
{IPAD_14_PRO_MAX_PORTRAIT_RETRACT}
    }}
    @media (min-width: 1370px) and (max-width: 1382px) and (max-height: 1040px) {{
{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
{IPAD_14_PRO_MAX_LANDSCAPE_OVERRIDE}
    }}
"""

# Surface Duo (540 / 720 / ~1114 span): overlay sidebar, full off-screen hide, mobile arrows.
SURFACE_DUO_SIDEBAR = """
        :root {
            --scoop-sidebar-width: min(92vw, 36rem);
            --footer-sidebar-width: 0px;
        }

        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div,
        .block-container {
            width: 100% !important;
            max-width: 100% !important;
        }

        section[data-testid="stSidebar"] {
            position: fixed !important;
            top: 0 !important;
            left: 0 !important;
            height: 100dvh !important;
            min-height: 100dvh !important;
            z-index: 999999 !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-100vw) !important;
            transition: transform 0.28s ease, visibility 0.28s ease !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
            visibility: visible !important;
        }
        section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
            transform: translateX(-100vw) !important;
            pointer-events: none !important;
            visibility: hidden !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: 0 !important;
            max-width: 100% !important;
            box-shadow: none !important;
            pointer-events: auto !important;
        }
        [data-testid="stSidebarBackdrop"] {
            position: fixed !important;
            inset: 0 !important;
            z-index: 999998 !important;
            cursor: pointer !important;
        }
        [data-testid="stHeader"] {
            z-index: 1000005 !important;
        }

        /* Mobile-style toggle: plain Streamlit arrows (no boxed chrome). */
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="collapsedControl"],
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] {
            position: static !important;
            top: auto !important;
            left: auto !important;
            right: auto !important;
            bottom: auto !important;
            width: auto !important;
            height: auto !important;
            min-width: 0 !important;
            min-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
            transform: none !important;
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"] button {
            width: auto !important;
            height: auto !important;
            min-width: 31.5px !important;
            min-height: 31.5px !important;
            padding: 0 !important;
            margin: 0 !important;
            font-size: 15.75px !important;
            line-height: 1 !important;
            color: #31333f !important;
            border: none !important;
            border-radius: 0 !important;
            background: transparent !important;
            box-shadow: none !important;
        }
        .scoop-responsive-sidebar-close {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stAppViewContainer"]::before {
            content: "" !important;
            position: fixed !important;
            inset: 0 !important;
            background: rgba(15, 23, 42, 0.38) !important;
            z-index: 999997 !important;
            pointer-events: none !important;
        }
""" + OVERLAY_SIDEBAR_TOPBAR_LAYER

SURFACE_DUO_LAYOUT = f"""
    /* ===== Surface Duo only — full slide-in, mobile-style arrows ===== */
    @media (width: 540px),
           ((width: 720px) and (max-height: 541px)),
           ((min-width: 1110px) and (max-width: 1118px) and (max-height: 741px)) {{
{SURFACE_DUO_SIDEBAR}
    }}
"""

DESKTOP_SIDEBAR = """
        :root {
            --footer-sidebar-width: clamp(12rem, 20vw, 36rem);
        }

        /* Desktop: sidebar always visible — no slide-out overlay. */
        section[data-testid="stSidebar"],
        section[data-testid="stSidebar"][aria-expanded="false"],
        section[data-testid="stSidebar"][aria-expanded="true"] {
            position: relative !important;
            transform: none !important;
            translate: none !important;
            transition: none !important;
            pointer-events: auto !important;
            visibility: visible !important;
            opacity: 1 !important;
            display: block !important;
            height: auto !important;
            min-height: 100% !important;
            z-index: auto !important;
            box-shadow: none !important;
            min-width: var(--scoop-sidebar-width) !important;
            width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            margin-left: 0 !important;
            left: auto !important;
            top: auto !important;
        }
        [data-testid="stSidebar"] > div,
        [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
            position: relative !important;
            transform: none !important;
            width: 100% !important;
            min-width: var(--scoop-sidebar-width) !important;
            max-width: min(92vw, 36rem) !important;
            height: auto !important;
            min-height: auto !important;
            pointer-events: auto !important;
            box-shadow: none !important;
        }
        [data-testid="stSidebarBackdrop"] {
            display: none !important;
        }
        [data-testid="stExpandSidebarButton"],
        [data-testid="stSidebarCollapseButton"],
        [data-testid="collapsedControl"] {
            display: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
        .stApp:has(section[data-testid="stSidebar"]) [data-testid="stAppViewContainer"]::before {
            display: none !important;
            content: none !important;
        }
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: auto !important;
            max-width: none !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div {
            width: auto !important;
            max-width: none !important;
        }
"""

# Shared desktop flex rules — used for min-width media query and zoom (data-attribute) selectors.
_DESKTOP_FLEX_SPLIT_RULES = """
    /* Desktop: flex split sidebar + main; scales with browser zoom without clipping main. */
    :root {
        --scoop-desktop-sidebar-width: clamp(10rem, min(20vw, 28rem), 36rem);
    }
    .stApp {
        overflow-x: auto !important;
        max-width: 100vw !important;
    }
    [data-testid="stAppViewContainer"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: stretch !important;
        position: relative !important;
        width: 100% !important;
        max-width: 100vw !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }
    section[data-testid="stSidebar"],
    section[data-testid="stSidebar"][aria-expanded="false"],
    section[data-testid="stSidebar"][aria-expanded="true"] {
        flex: 0 1 auto !important;
        align-self: flex-start !important;
        position: relative !important;
        transform: none !important;
        translate: none !important;
        transition: none !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        overflow: visible !important;
        z-index: 2 !important;
        min-width: min(10rem, 28vw) !important;
        width: var(--scoop-desktop-sidebar-width) !important;
        max-width: min(32vw, 36rem) !important;
        box-shadow: none !important;
        left: auto !important;
        top: auto !important;
        height: 100vh !important;
        min-height: 100vh !important;
        max-height: 100vh !important;
    }
    [data-testid="stSidebar"] > div,
    [data-testid="stSidebar"] [data-testid="stSidebarContent"] {
        overflow-x: visible !important;
        overflow-y: auto !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        height: 100vh !important;
        max-height: 100vh !important;
        box-sizing: border-box !important;
    }
    [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]) {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        width: auto !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        box-sizing: border-box !important;
    }
    [data-testid="stAppViewContainer"] > section.main,
    [data-testid="stMainBlockContainer"],
    section.main > div {
        min-width: 0 !important;
        max-width: 100% !important;
        overflow-x: auto !important;
        box-sizing: border-box !important;
        padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 2.75rem) !important;
    }
    [data-testid="stSidebarBackdrop"] {
        display: none !important;
    }
    [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapseButton"],
    [data-testid="collapsedControl"],
    [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
    [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
    [data-testid="stHeader"] [data-testid="collapsedControl"] {
        display: none !important;
    }
    .stApp:has(section[data-testid="stSidebar"]) [data-testid="stAppViewContainer"]::before {
        display: none !important;
        content: none !important;
    }
    .sidebar-brand {
        width: 100% !important;
        margin: 0.15rem 0 0.35rem 0 !important;
        padding: 0.7rem 1rem !important;
        box-sizing: border-box !important;
        white-space: normal !important;
    }
    .sidebar-brand-text,
    [data-testid="stSidebar"] #scoop-title {
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        max-width: 100% !important;
    }
    [data-testid="stSidebar"] [data-testid="stCheckbox"],
    [data-testid="stSidebar"] [data-testid="stTextInput"],
    [data-testid="stSidebar"] [data-testid="stPageLink"],
    [data-testid="stSidebar"] [data-testid="element-container"] {
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
"""

# Injected last on every page — beats tablet overlay rules and fixes desktop clipping.
DESKTOP_SIDEBAR_LAYOUT = f"""
@media (min-width: 1367px) {{
{_DESKTOP_FLEX_SPLIT_RULES}
}}
"""

# When browser zoom shrinks layout viewport below 1367px on a physical desktop screen,
# JS sets data-scoop-desktop-layout="1" so split-sidebar rules still apply.
DESKTOP_ZOOM_LAYOUT = f"""
html[data-scoop-desktop-layout="1"] {{
{_DESKTOP_FLEX_SPLIT_RULES}
}}
"""

# Tighter nav slide-out spacing — all viewports; injected last on every page.
SIDEBAR_NAV_COMPACT = """
    [data-testid="stSidebar"] .sidebar-brand {
        margin-bottom: 0.35rem !important;
    }
    [data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        margin-bottom: 0.35rem !important;
    }
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(hr) {
        margin-top: 0 !important;
        margin-bottom: 0.15rem !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
    [data-testid="stSidebar"] hr {
        margin: 0.15rem 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.4rem !important;
    }
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"]) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }
"""

# Shared sidebar brand ↔ toggle ↔ first nav link spacing.
_SIDEBAR_BRAND_TOGGLE_BUFFER_RULES = """
    html body .stApp [data-testid="stSidebar"] .sidebar-brand {
        margin-bottom: 0.85rem !important;
    }
    html body .stApp [data-testid="stSidebar"] div[data-testid="stCheckbox"] {
        margin-top: 0.25rem !important;
        margin-bottom: 0.1rem !important;
    }
    html body .stApp [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(hr),
    html body .stApp [data-testid="stSidebar"] [data-testid="element-container"]:has(hr),
    html body .stApp [data-testid="stSidebar"] [data-testid="stMarkdownContainer"]:has(hr) {
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        min-height: 0 !important;
    }
    html body .stApp [data-testid="stSidebar"] hr {
        margin: 0.1rem 0 !important;
    }
    html body .stApp [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {
        gap: 0.2rem !important;
    }
    html body .stApp [data-testid="stSidebar"] [data-testid="stElementContainer"]:has(hr) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    html body .stApp [data-testid="stSidebar"] [data-testid="element-container"]:has(hr) + [data-testid="element-container"]:has([data-testid="stPageLink"]) {
        margin-top: 0.15rem !important;
    }
"""

# Mobile/tablet slide-out: brand ↔ toggle spacing; tighten toggle ↔ first nav link.
RESPONSIVE_SIDEBAR_BRAND_TOGGLE_BUFFER = f"""
@media (max-width: 1366px) {{
{_SIDEBAR_BRAND_TOGGLE_BUFFER_RULES}
}}
"""

DESKTOP_SIDEBAR_BRAND_TOGGLE_BUFFER = f"""
@media (min-width: 1367px) {{
{_SIDEBAR_BRAND_TOGGLE_BUFFER_RULES}
}}
html[data-scoop-desktop-layout="1"] {{
{_SIDEBAR_BRAND_TOGGLE_BUFFER_RULES}
}}
"""

# Desktop-only boxed nav items for market screener pages (not Terms of Service).
_DESKTOP_MARKET_NAV_GAP = "12px"

# Fixed gap between market nav buttons — beats page-level stVerticalBlock gap overrides.
_DESKTOP_MARKET_NAV_SPACING_RULES = f"""
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) {{
        margin: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]),
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
"""

_DESKTOP_MARKET_NAV_LIGHT_RULES = """
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) {
        border: 2px solid #334155 !important;
        border-radius: 0.75rem !important;
        background: #ffffff !important;
        padding: 0.15rem 0.35rem !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]):hover {
        border-color: #0f172a !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.1) !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) a {
        display: block !important;
        width: 100% !important;
        border-radius: 0.55rem !important;
        padding: 0.45rem 0.65rem !important;
        box-sizing: border-box !important;
    }
"""

_DESKTOP_MARKET_NAV_DARK_RULES = """
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) {
        border: 2px solid #94a3b8 !important;
        border-radius: 0.75rem !important;
        background: #000000 !important;
        padding: 0.15rem 0.35rem !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]):hover {
        border-color: #e2e8f0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.45) !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) a {
        display: block !important;
        width: 100% !important;
        border-radius: 0.55rem !important;
        padding: 0.45rem 0.65rem !important;
        box-sizing: border-box !important;
        color: #ffffff !important;
        background-color: transparent !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) span,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) div,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) p,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) a:visited,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) a:hover,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) a:active {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active]:has(a[href$="_Top_10"]) {
        background: #333333 !important;
        border-color: #cbd5e1 !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active]:has(a[href$="_Top_10"]) a {
        background-color: rgba(255, 255, 255, 0.1) !important;
    }
"""

_HOME_MAIN_SCOPE = 'html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"]'
_HOME_SIDE_PADDING = "20px"
_HOME_LOGO_MAX = "clamp(240px, 64vw, 340px)"
_HOME_LOGO_TABLET_MAX = "clamp(360px, 50vw, 520px)"
_HOME_HEADER_CLEARANCE = "calc(4.75rem + env(safe-area-inset-top, 0px))"
_MOBILE_TAB_MAIN = 'html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"]'
_MOBILE_TAB_DARK_MODE_SCOPE = f'{_MOBILE_TAB_MAIN} .scoop-mobile-inner-top-toggle'
_MOBILE_TAB_TOGGLE_WRAP = (
    f'{_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="element-container"]:has([data-testid="stToggle"]), '
    f'{_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stToggle"])'
)
# Streamlit renders the inner-top markdown wrappers as siblings — dark mode widget is the next row.
_MOBILE_TAB_DARK_MODE_ROW = (
    f'{_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="stElementContainer"]:has([data-testid="stToggle"]), '
    f'{_MOBILE_TAB_MAIN} [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="element-container"]:has([data-testid="stToggle"]), '
    f'{_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]), '
    f'{_MOBILE_TAB_MAIN} [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) + [data-testid="element-container"]:has([data-testid="stCheckbox"])'
)
_MOBILE_TAB_TERMS_CHECKBOX_ROW = (
    f'{_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):has(+ [data-testid="stElementContainer"] .disclaimer-footer), '
    f'{_MOBILE_TAB_MAIN} [data-testid="element-container"]:has([data-testid="stCheckbox"]):has(+ [data-testid="element-container"] .disclaimer-footer)'
)
_MOBILE_TAB_DARK_MODE_CONTAINER = _MOBILE_TAB_TOGGLE_WRAP

# Mobile/tablet Dark mode control — no pill container (toggle + label only).
_MOBILE_TABLET_DARK_MODE_PILL_FONT = "clamp(0.94rem, 2.6vw, 1.08rem)"
_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME = f"""
        display: inline-flex !important;
        align-items: center !important;
        width: fit-content !important;
        max-width: 100% !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border-radius: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
        overflow: visible !important;
        font-size: {_MOBILE_TABLET_DARK_MODE_PILL_FONT} !important;
        white-space: nowrap !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL = f"""
        color: #111827 !important;
        font-weight: 700 !important;
        font-size: {_MOBILE_TABLET_DARK_MODE_PILL_FONT} !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL_SHELL = f"""
        display: inline-flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 0.2rem !important;
        position: static !important;
        width: auto !important;
        max-width: none !important;
        flex: 0 0 auto !important;
        font-size: {_MOBILE_TABLET_DARK_MODE_PILL_FONT} !important;
        line-height: 1 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: visible !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_TIP = """
        position: static !important;
        display: inline-flex !important;
        align-items: center !important;
        flex-shrink: 0 !important;
        margin: 0 !important;
        transform: none !important;
        inset: auto !important;
        font-size: clamp(0.84rem, 2.2vw, 0.96rem) !important;
        width: auto !important;
        height: auto !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_ROW = """
        display: inline-flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 0.4rem !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH = """
        width: clamp(2.2rem, 6vw, 2.55rem) !important;
        height: clamp(1.18rem, 3.3vw, 1.36rem) !important;
        min-width: clamp(2.2rem, 6vw, 2.55rem) !important;
        min-height: clamp(1.18rem, 3.3vw, 1.36rem) !important;
"""
_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH_KNOB = """
        width: clamp(1rem, 2.85vw, 1.16rem) !important;
        height: clamp(1rem, 2.85vw, 1.16rem) !important;
"""
_MOBILE_SCREENER_INDEX_BANNER_CONTAINER = (
    '[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-banner-compact), '
    '[data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-banner-compact), '
    '[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] div[style*="border-left:4px solid"]), '
    '[data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] div[style*="border-left:4px solid"]), '
    '[data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] div[style*="flex-wrap:wrap"][style*="margin-bottom:1rem"]), '
    '[data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] div[style*="flex-wrap:wrap"][style*="margin-bottom:1rem"])'
)
_HOME_EL = (
    f'{_HOME_MAIN_SCOPE} [data-testid="element-container"], '
    f'{_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]'
)
_HOME_TOGGLE_WRAP = (
    f'{_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stToggle"]), '
    f'{_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stToggle"])'
)

_MOBILE_TABLET_TOGGLE_RULES = f"""
    html[data-scoop-tab-nav="1"] .scoop-mobile-inner-top-toggle {{
        width: 100% !important;
        max-width: 100% !important;
    }}
    {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):not(:has([data-testid="stToggle"])):not(:has([data-testid="stCheckbox"])),
    {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle):not(:has([data-testid="stToggle"])):not(:has([data-testid="stCheckbox"])) {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: transparent !important;
        border: none !important;
    }}
    {_MOBILE_TAB_DARK_MODE_ROW},
    {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stToggle"]),
    {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stCheckbox"]),
    {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stToggle"]),
    {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stCheckbox"]) {{
        display: block !important;
        visibility: visible !important;
        height: auto !important;
        min-height: 2.4rem !important;
        overflow: visible !important;
        opacity: 1 !important;
    }}
    {_MOBILE_TAB_TOGGLE_WRAP} {{
        background: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        width: auto !important;
        max-width: 100% !important;
        min-height: 0 !important;
        box-sizing: border-box !important;
        box-shadow: none !important;
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME}
    }}
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]),
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([aria-label="Dark mode"]) {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] > label {{
        width: auto !important;
        min-height: 0 !important;
        align-items: center !important;
        gap: 0.35rem !important;
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] label p {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-testid="stWidgetLabel"] {{
        min-height: 0 !important;
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] > div {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH_KNOB}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-testid="stTooltipIcon"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_TIP}
    }}
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-baseweb="switch"] {{
        background-color: #334155 !important;
    }}
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] {{
        background-color: #cbd5e1 !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] label p {{
        color: #e2e8f0 !important;
    }}
"""

MOBILE_TABLET_TOGGLE_STYLE = f"""
@media (max-width: 1366px) {{
{_MOBILE_TABLET_TOGGLE_RULES}
}}
"""

# Final cascade — spacing + unboxed toggle on mobile/tablet home and market pages.
_MOBILE_TABLET_TOGGLE_FINAL = f"""
@media (max-width: 1366px) {{
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):not(:has([data-testid="stToggle"])):not(:has([data-testid="stCheckbox"])),
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle):not(:has([data-testid="stToggle"])):not(:has([data-testid="stCheckbox"])) {{
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        background: transparent !important;
        border: none !important;
    }}
    {_MOBILE_TAB_DARK_MODE_ROW},
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stToggle"]),
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle):has([data-testid="stCheckbox"]) {{
        display: block !important;
        visibility: visible !important;
        height: auto !important;
        min-height: 2.4rem !important;
        overflow: visible !important;
        opacity: 1 !important;
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle),
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle),
    html[data-scoop-tab-nav="1"]:not([data-scoop-home-page="1"]) {_MOBILE_TAB_TOGGLE_WRAP} {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        width: auto !important;
        max-width: 100% !important;
        min-height: 0 !important;
        box-sizing: border-box !important;
        box-shadow: none !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-screener-active="1"] {_MOBILE_TAB_DARK_MODE_ROW} {{
        margin-top: 12px !important;
        margin-bottom: 12px !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-screener-active="1"] {_MOBILE_SCREENER_INDEX_BANNER_CONTAINER} {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
}}
"""

_MOBILE_TABLET_DARK_MODE_TOGGLE_WIDGET = f'{_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"]'
_MOBILE_TABLET_DARK_MODE_TOGGLE_WRAP = (
    f'{_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stToggle"]), '
    f'{_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="element-container"]:has([data-testid="stToggle"])'
)

# Mobile/tablet main Dark mode — unboxed toggle (desktop unchanged).
_MOBILE_TABLET_DARK_MODE_TOGGLE_BOXED = f"""
@media (max-width: 1366px) {{
    {_MOBILE_TAB_DARK_MODE_ROW} {{
        margin-top: 12px !important;
        margin-bottom: 12px !important;
        padding: 0 !important;
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: auto !important;
        max-width: 100% !important;
        min-height: 0 !important;
        box-sizing: border-box !important;
        display: flex !important;
        justify-content: flex-end !important;
    }}
    {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stToggle"],
    {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME}
        margin-top: 0 !important;
        margin-bottom: 0 !important;
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"],
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stMarkdownContainer"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL_SHELL}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] label p {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stTooltipIcon"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_TIP}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH}
    }}
    {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] > div {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH_KNOB}
    }}
}}
"""

# Home landing only — unboxed dark mode toggle (mobile/tablet).
_HOME_MOBILE_TABLET_TOGGLE_BOXED = _MOBILE_TABLET_DARK_MODE_TOGGLE_BOXED

# Market screener pages — same unboxed Dark mode as home (desktop unchanged).
_MARKET_MOBILE_TABLET_TOGGLE_BOXED = _MOBILE_TABLET_DARK_MODE_TOGGLE_BOXED

# Late cascade — layout + beat page-level font/width overrides (mobile/tablet dark mode only).
_MOBILE_TABLET_DARK_MODE_PILL_LAYOUT_FINAL = f"""
@media (max-width: 1366px) {{
    html[data-scoop-tab-nav="1"] .scoop-mobile-inner-top-toggle {{
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    html[data-scoop-tab-nav="1"] .scoop-mobile-inner-top [data-testid="stHorizontalBlock"] {{
        justify-content: flex-end !important;
        width: 100% !important;
    }}
    html[data-scoop-tab-nav="1"] .scoop-mobile-inner-top [data-testid="stHorizontalBlock"] > div,
    html[data-scoop-tab-nav="1"] .scoop-mobile-inner-top-toggle [data-testid="stVerticalBlock"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stToggle"]),
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="element-container"]:has([data-testid="stToggle"]) {{
        width: fit-content !important;
        max-width: 100% !important;
        flex: 0 0 auto !important;
        min-width: 0 !important;
        margin-left: auto !important;
        margin-right: 0 !important;
    }}
    {_MOBILE_TAB_MAIN} [data-testid="stToggle"],
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]),
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([aria-label="Dark mode"]),
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stToggle"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME}
    }}
    {_MOBILE_TAB_MAIN} [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    {_MOBILE_TAB_MAIN} [data-testid="stToggle"] label p,
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]) [data-testid="stWidgetLabel"] p,
    {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]) label p {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL}
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] > label {{
        width: auto !important;
        min-height: 0 !important;
        align-items: center !important;
        gap: 0.35rem !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stMarkdownContainer"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL_SHELL}
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] label p {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL}
    }}
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] {{
        background-color: #334155 !important;
    }}
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} [data-testid="stToggle"] [data-baseweb="switch"] {{
        background-color: #cbd5e1 !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_SCOPE} div[data-testid="stToggle"] label p,
    html[data-scoop-theme="dark"] {_MOBILE_TAB_MAIN} [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"] {_MOBILE_TAB_MAIN} [data-testid="stToggle"] label p,
    html[data-scoop-theme="dark"] {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]) [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"] {_MOBILE_TAB_MAIN} [data-testid="stCheckbox"]:has([data-baseweb="switch"]) label p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] label p {{
        color: #e2e8f0 !important;
    }}
    /* Space Dark mode control above market index cards (mobile/tablet only). */
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stToggle"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_SCREENER_INDEX_BANNER_CONTAINER} {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} + [data-testid="stElementContainer"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} + [data-testid="element-container"] {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
}}
"""


def _mirror_sidebar_nav_css_for_home(sidebar_css: str) -> str:
    """Map desktop sidebar nav CSS onto the mobile/tablet home landing column."""
    out = (
        sidebar_css.replace(
            '[data-testid="stSidebar"] [data-testid="stElementContainer"]',
            _HOME_EL,
        )
        .replace(
            '[data-testid="stSidebar"] [data-testid="element-container"]',
            _HOME_EL,
        )
        .replace(
            '[data-testid="stSidebar"] [data-testid="stVerticalBlock"]',
            f'{_HOME_MAIN_SCOPE} [data-testid="stVerticalBlock"]',
        )
        .replace(
            '[data-testid="stSidebar"] [data-testid="stPageLink"]',
            f'{_HOME_MAIN_SCOPE} [data-testid="stPageLink"]',
        )
    )
    return (
        out.replace(
            'html:not([data-scoop-theme="dark"]) html[data-scoop-home-page="1"]',
            'html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"]',
        ).replace(
            'html[data-scoop-theme="dark"] html[data-scoop-home-page="1"]',
            'html[data-scoop-theme="dark"][data-scoop-home-page="1"]',
        )
    )


_HOME_MARKET_NAV_BASE_RULES = f"""
    {_HOME_MAIN_SCOPE} [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"] a[href$="_Top_10"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href$="_Top_10"]) {{
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stPageLink"]:has(a[href$="_Top_10"]) {{
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }}
"""

_HOME_DESCRIPTION_TO_NAV_FINAL = f"""
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-home-landing),
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-home-landing) {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        height: auto !important;
        min-height: fit-content !important;
        overflow: visible !important;
    }}
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-home-landing) [data-testid="stMarkdownContainer"],
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-home-landing) [data-testid="stMarkdownContainer"] {{
        height: auto !important;
        min-height: fit-content !important;
        overflow: visible !important;
        margin-bottom: 0 !important;
    }}
    html[data-scoop-home-page="1"] .scoop-home-landing {{
        display: block !important;
        margin: 0 0 {_DESKTOP_MARKET_NAV_GAP} 0 !important;
        padding: 0 !important;
        overflow: visible !important;
    }}
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-home-landing) + [data-testid="element-container"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-home-landing) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-home-landing) + [data-testid="element-container"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-home-landing) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"]) {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
"""

# Phone/tablet home landing: full-width white logo card; circular mark centered inside.
_HOME_LOGO_BOX_CHROME = """
        background: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
        width: 100% !important;
        max-width: 100% !important;
"""
_HOME_LOGO_INNER = """
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        min-width: 0 !important;
        max-width: 100% !important;
        padding: 0 !important;
        margin: 0 auto !important;
"""
_HOME_LOGO_MOBILE_RULES = f"""
@media (max-width: 768px) {{
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
{_HOME_LOGO_BOX_CHROME}
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 1rem 1.25rem !important;
        margin: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] {{
{_HOME_LOGO_INNER}
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] img {{
        width: auto !important;
        max-width: {_HOME_LOGO_MAX} !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
        object-fit: contain !important;
        object-position: center !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
        background: #ffffff !important;
    }}
}}
"""

# Tablet home landing: same white card, larger centered mark.
_HOME_LOGO_TABLET_RULES = f"""
@media (min-width: 769px) and (max-width: 1366px) {{
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
{_HOME_LOGO_BOX_CHROME}
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        padding: 1.15rem 1.5rem !important;
        margin: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] {{
{_HOME_LOGO_INNER}
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] img {{
        width: auto !important;
        max-width: {_HOME_LOGO_TABLET_MAX} !important;
        height: auto !important;
        display: block !important;
        margin: 0 auto !important;
        object-fit: contain !important;
        object-position: center !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
        background: #ffffff !important;
    }}
}}
"""

# Late cascade — clear Streamlit header so the circular home logo is not clipped (mobile/tablet only).
_HOME_LOGO_TOP_CLEARANCE_FINAL = f"""
@media (max-width: 1366px) {{
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"],
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp .stMainBlockContainer {{
        padding-top: {_HOME_HEADER_CLEARANCE} !important;
        overflow: visible !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stImage"]) {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        margin-top: 0 !important;
        padding-top: {_HOME_HEADER_CLEARANCE} !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
        padding-bottom: 1rem !important;
        overflow: visible !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stImage"],
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stFullScreenFrame"] {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        overflow: visible !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-home-page="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stImage"] img {{
        display: block !important;
        width: auto !important;
        height: auto !important;
        max-height: none !important;
        margin-left: auto !important;
        margin-right: auto !important;
        object-fit: contain !important;
        object-position: center !important;
    }}
}}
"""

# Desktop sidebar: no logo box, use full sidebar width.
DESKTOP_SIDEBAR_LOGO_RULES = """
@media (min-width: 1367px) {
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stImage"]) {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        padding: 0 !important;
        margin: 0 -1rem 0.25rem -1rem !important;
        width: calc(100% + 2rem) !important;
        max-width: calc(100% + 2rem) !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] {
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    [data-testid="stSidebar"] [data-testid="stImage"] img {
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        display: block !important;
    }
    /* Desktop: hide Streamlit image Fullscreen so the sidebar logo cannot overlay the page. */
    [data-testid="stSidebar"] [data-testid="stElementToolbar"],
    [data-testid="stSidebar"] button[aria-label="Fullscreen"],
    [data-testid="stSidebar"] [data-testid="stFullScreenFrame"] button[aria-label="Fullscreen"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
    [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]):has(button[aria-label="Close fullscreen"]) {
        position: static !important;
        inset: auto !important;
        width: 100% !important;
        height: auto !important;
        z-index: auto !important;
    }
    [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]):has(button[aria-label="Close fullscreen"]) img {
        width: 100% !important;
        max-width: 100% !important;
        max-height: none !important;
        height: auto !important;
    }
    [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]) button[aria-label="Close fullscreen"] {
        display: none !important;
    }
}
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stImage"]),
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stImage"]) {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    margin: 0 -1rem 0.25rem -1rem !important;
    width: calc(100% + 2rem) !important;
    max-width: calc(100% + 2rem) !important;
}
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="stImage"],
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="stImage"] img {
    background: transparent !important;
    border: none !important;
    box-shadow: none !important;
    width: 100% !important;
    max-width: 100% !important;
}
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="stElementToolbar"],
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] button[aria-label="Fullscreen"],
html[data-scoop-desktop-layout="1"] [data-testid="stSidebar"] [data-testid="stFullScreenFrame"] button[aria-label="Fullscreen"] {
    display: none !important;
    visibility: hidden !important;
    pointer-events: none !important;
}
html[data-scoop-desktop-layout="1"] [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]):has(button[aria-label="Close fullscreen"]) {
    position: static !important;
    inset: auto !important;
    width: 100% !important;
    height: auto !important;
    z-index: auto !important;
}
html[data-scoop-desktop-layout="1"] [data-testid="stFullScreenFrame"]:has([data-testid="stImage"]) button[aria-label="Close fullscreen"] {
    display: none !important;
}
"""

# Desktop + tablet: flow disclaimer below content (no fixed black bar overlay).
DESKTOP_TABLET_DISCLAIMER_FLOW = """
@media (min-width: 769px) {
    html body .stApp .disclaimer-footer {
        position: static !important;
        left: 0 !important;
        bottom: auto !important;
        width: 100% !important;
        margin-top: 1.25rem !important;
        padding: 0.5rem 0.75rem !important;
        font-size: clamp(0.76rem, 1.8vw, 0.92rem) !important;
        line-height: 1.35 !important;
        z-index: auto !important;
    }
    html body .stApp .disclaimer-footer strong,
    html body .stApp .disclaimer-footer a {
        font-size: inherit !important;
    }
    html body .stApp .stMainBlockContainer,
    html body .stApp [data-testid="stMainBlockContainer"] {
        padding-bottom: 2.5rem !important;
    }
}
"""

_HOME_MARKET_NAV_LIGHT_RULES = _mirror_sidebar_nav_css_for_home(_DESKTOP_MARKET_NAV_LIGHT_RULES)
_HOME_MARKET_NAV_DARK_RULES = _mirror_sidebar_nav_css_for_home(_DESKTOP_MARKET_NAV_DARK_RULES)

# 12px space between market nav buttons — final cascade wins over margin resets.
_HOME_MARKET_NAV_GAP_SPACER_RULES = f"""
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"]) {{
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]) {{
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-bottom: 0 !important;
    }}
"""

_HOME_BRAND_TOGGLE_BUFFER_RULES = f"""
    {_HOME_MAIN_SCOPE} .sidebar-brand {{
        margin-bottom: 0.85rem !important;
    }}
    {_HOME_TOGGLE_WRAP} {{
        margin-top: 0.25rem !important;
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        width: 100% !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(hr),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(hr),
    {_HOME_MAIN_SCOPE} [data-testid="stMarkdownContainer"]:has(hr) {{
        margin-top: 0 !important;
        margin-bottom: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        min-height: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} hr {{
        margin: 0.1rem 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(.scoop-home-landing),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(.scoop-home-landing),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(.scoop-home-landing),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(.scoop-home-landing),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"]),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(hr) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) {{
        margin-top: 0.15rem !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(.scoop-home-landing),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(.scoop-home-landing) {{
        margin-top: 0 !important;
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        overflow: visible !important;
    }}
    html[data-scoop-home-page="1"] .scoop-home-landing p {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(.scoop-home-landing) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has(.scoop-home-landing) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(.scoop-home-landing) + {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"] a[href*="Top_10"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has(.scoop-home-landing) + {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"] a[href*="Top_10"]) {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stVerticalBlock"] {{
        gap: 0.2rem !important;
    }}
"""

_HOME_SIDEBAR_BRAND_AND_TYPE_RULES = f"""
    html[data-scoop-home-page="1"] {{
        --scoop-home-side-padding: {_HOME_SIDE_PADDING};
    }}
    html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} {{
        background-color: #f0f2f6 !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} {{
        background-color: #111827 !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        max-width: 100% !important;
        margin: 0 !important;
        padding: 1rem 1.25rem !important;
        background: #ffffff !important;
        border: none !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] {{
        display: block !important;
        width: auto !important;
        min-width: 0 !important;
        max-width: 100% !important;
        margin: 0 auto !important;
        padding: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
        box-sizing: border-box !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stImage"]),
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stImage"]) {{
        background: #ffffff !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} [data-testid="stImage"] {{
        background: transparent !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stImage"] img {{
        width: auto !important;
        max-width: {_HOME_LOGO_MAX} !important;
        height: auto !important;
        display: block !important;
        object-fit: contain !important;
        object-position: center !important;
        margin: 0 auto !important;
    }}
    {_HOME_MAIN_SCOPE} .sidebar-brand {{
        font-size: clamp(2rem, 10vw, 3.75rem) !important;
        font-weight: 400 !important;
        color: #000000 !important;
        line-height: 1.05 !important;
        background: transparent !important;
        display: block !important;
        width: 100% !important;
        margin: 0.15rem 0 0.35rem 0 !important;
        padding: 0.7rem 0 !important;
        box-sizing: border-box !important;
        white-space: normal !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} .sidebar-brand {{
        color: #f1f5f9 !important;
        background: #111827 !important;
    }}
    {_HOME_MAIN_SCOPE} .sidebar-brand-row {{
        display: inline-flex !important;
        align-items: flex-end !important;
        gap: 10px !important;
        width: 100% !important;
        max-width: 100% !important;
    }}
    {_HOME_MAIN_SCOPE} .sidebar-brand-text,
    {_HOME_MAIN_SCOPE} #scoop-title {{
        font-size: clamp(2rem, 10vw, 3.75rem) !important;
        font-weight: 400 !important;
        color: #000000 !important;
        line-height: 1.05 !important;
        text-decoration: underline !important;
        text-underline-offset: 6px !important;
        text-decoration-color: #000000 !important;
        white-space: normal !important;
        overflow-wrap: break-word !important;
        word-break: normal !important;
        max-width: 100% !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .sidebar-brand-text,
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] #scoop-title {{
        color: #ffffff !important;
        text-decoration-color: #ffffff !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="element-container"]:has([data-testid="stPageLink"]),
    {_HOME_MAIN_SCOPE} [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) {{
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stPageLink"] {{
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }}
    {_HOME_MAIN_SCOPE} [data-testid="stPageLink"] a,
    {_HOME_MAIN_SCOPE} [data-testid="stPageLink"] span,
    {_HOME_MAIN_SCOPE} [data-testid="stPageLink"] p {{
        font-size: clamp(1rem, 4.2vw, 1.5rem) !important;
        line-height: 1.25 !important;
        white-space: normal !important;
        overflow-wrap: anywhere !important;
        word-break: break-word !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] {_HOME_MAIN_SCOPE} hr {{
        border-color: #334155 !important;
        background-color: #334155 !important;
    }}
"""

# Mobile/tablet slide-out: boxed nav items for all sidebar page links (light + dark active state).
_RESPONSIVE_MARKET_NAV_GAP = "10px"

_RESPONSIVE_MARKET_NAV_SPACING_RULES = f"""
    [data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"]) {{
        margin: 0 !important;
        padding: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stPageLink"] {{
        margin: 0 !important;
    }}
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    [data-testid="stSidebar"] [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]),
    [data-testid="stSidebar"] [data-testid="element-container"]:has([data-testid="stPageLink"]) + [data-testid="stElementContainer"]:has([data-testid="stPageLink"]) {{
        margin-top: {_RESPONSIVE_MARKET_NAV_GAP} !important;
    }}
"""

_RESPONSIVE_MARKET_NAV_LIGHT_RULES = """
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"] {
        border: 2px solid #334155 !important;
        border-radius: 0.75rem !important;
        background: #ffffff !important;
        padding: 0.2rem 0.4rem !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
        border-color: #0f172a !important;
        box-shadow: 0 2px 6px rgba(15, 23, 42, 0.1) !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        display: block !important;
        width: 100% !important;
        border-radius: 0.55rem !important;
        padding: 0.55rem 0.75rem !important;
        box-sizing: border-box !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] {
        background: #dbeafe !important;
        border-color: #60a5fa !important;
        box-shadow: 0 2px 8px rgba(37, 99, 235, 0.18) !important;
    }
    html:not([data-scoop-theme="dark"]) [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] a {
        background-color: rgba(96, 165, 250, 0.14) !important;
        color: #1e40af !important;
        font-weight: 600 !important;
    }
"""

_RESPONSIVE_MARKET_NAV_DARK_RULES = """
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] {
        border: 2px solid #94a3b8 !important;
        border-radius: 0.75rem !important;
        background: #000000 !important;
        padding: 0.2rem 0.4rem !important;
        box-sizing: border-box !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.35) !important;
        transition: border-color 0.15s ease, box-shadow 0.15s ease, background-color 0.15s ease !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"]:hover {
        border-color: #e2e8f0 !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.45) !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] a {
        display: block !important;
        width: 100% !important;
        border-radius: 0.55rem !important;
        padding: 0.55rem 0.75rem !important;
        box-sizing: border-box !important;
        color: #ffffff !important;
        background-color: transparent !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] span,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] div,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] p,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] a:visited,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] a:hover,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"] a:active {
        color: #ffffff !important;
        background-color: transparent !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] {
        background: #333333 !important;
        border-color: #60a5fa !important;
        box-shadow: 0 2px 8px rgba(96, 165, 250, 0.25) !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] a {
        background-color: rgba(96, 165, 250, 0.18) !important;
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] span,
    html[data-scoop-theme="dark"] [data-testid="stSidebar"] [data-testid="stPageLink"][data-scoop-nav-active] p {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
"""

DESKTOP_SIDEBAR_NAV_MARKET = f"""
@media (min-width: 1367px) {{
{_DESKTOP_MARKET_NAV_SPACING_RULES}
{_DESKTOP_MARKET_NAV_LIGHT_RULES}
{_DESKTOP_MARKET_NAV_DARK_RULES}
}}
html[data-scoop-desktop-layout="1"] {{
{_DESKTOP_MARKET_NAV_SPACING_RULES}
{_DESKTOP_MARKET_NAV_LIGHT_RULES}
{_DESKTOP_MARKET_NAV_DARK_RULES}
}}
@media (max-width: 1366px) {{
{_RESPONSIVE_MARKET_NAV_SPACING_RULES}
{_RESPONSIVE_MARKET_NAV_LIGHT_RULES}
{_RESPONSIVE_MARKET_NAV_DARK_RULES}
}}
"""

# Analyze deep-dive: drop header padding, js_eval gaps, and divider lines (desktop only).
_DESKTOP_ANALYZE_TOP_COMPACT_RULES = """
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"],
    html[data-scoop-analyze-active="1"] section.main > div,
    html[data-scoop-analyze-active="1"] [data-testid="stAppViewContainer"] > section.main {
        padding-top: 0.75rem !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
"""

DESKTOP_ANALYZE_TOP_COMPACT = f"""
@media (min-width: 1367px) {{
{_DESKTOP_ANALYZE_TOP_COMPACT_RULES}
}}
html[data-scoop-desktop-layout="1"][data-scoop-analyze-active="1"] {{
{_DESKTOP_ANALYZE_TOP_COMPACT_RULES}
}}
"""

# Mobile/tablet Analyze deep-dive: collapse bootstrap gaps, js_eval, and stray divider lines.
_RESPONSIVE_ANALYZE_TOP_COMPACT_RULES = """
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]),
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stHtml"]),
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stHtml"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style),
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] style) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)),
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-analyze-active="1"] [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.35rem !important;
    }
"""

RESPONSIVE_ANALYZE_TOP_COMPACT = f"""
@media (max-width: 1366px) {{
{_RESPONSIVE_ANALYZE_TOP_COMPACT_RULES}
}}
"""

# Market screener landing pages (_Top_10): drop header padding, js_eval gaps, and block spacing.
_DESKTOP_SCREENER_TOP_COMPACT_RULES = """
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"],
    html[data-scoop-screener-active="1"] section.main > div,
    html[data-scoop-screener-active="1"] [data-testid="stAppViewContainer"] > section.main {
        padding-top: 12px !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.55rem !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(+ [data-testid="stElementContainer"] h1) {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
"""

DESKTOP_SCREENER_TOP_COMPACT = f"""
@media (min-width: 1367px) {{
{_DESKTOP_SCREENER_TOP_COMPACT_RULES}
}}
html[data-scoop-desktop-layout="1"][data-scoop-screener-active="1"] {{
{_DESKTOP_SCREENER_TOP_COMPACT_RULES}
}}
"""

# Desktop screener gating view (terms not yet accepted): full-width banners + intro.
_DESKTOP_SCREENER_GATING_LAYOUT_RULES = """
    html[data-scoop-screener-gated="1"] [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]),
    html[data-scoop-screener-gated="1"] [data-testid="stAppViewContainer"] > section.main {
        flex: 1 1 0 !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"],
    html[data-scoop-screener-gated="1"] [data-testid="stAppViewContainer"] > section.main,
    html[data-scoop-screener-gated="1"] section.main > div,
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] .block-container {
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlockBorderWrapper"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] h1 {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] .scoop-landing-summary,
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] .scoop-landing-info,
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] .scoop-landing-sentiment,
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] .scoop-landing-affiliate {
        width: 100% !important;
        max-width: none !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] .scoop-banner-compact {
        display: none !important;
    }
    html[data-scoop-screener-gated="1"] .scoop-banner-desktop,
    html[data-scoop-screener-gated="1"] [data-testid="stMarkdownContainer"] div[style*="display:flex"][style*="flex-wrap:wrap"][style*="margin-bottom:1rem"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        gap: 1rem !important;
        width: 100% !important;
        max-width: 100% !important;
        margin-bottom: 1rem !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] .scoop-banner-desktop > div,
    html[data-scoop-screener-gated="1"] [data-testid="stMarkdownContainer"] div[style*="max-width:50%"],
    html[data-scoop-screener-gated="1"] [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"] {
        flex: 1 1 0 !important;
        min-width: 0 !important;
        max-width: none !important;
        width: auto !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stAlert"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stAlert"]),
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] div[data-testid="stCheckbox"],
    html[data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stCheckbox"]) {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
"""

DESKTOP_SCREENER_GATING_LAYOUT = f"""
@media (min-width: 1367px) {{
{_DESKTOP_SCREENER_GATING_LAYOUT_RULES}
}}
html[data-scoop-desktop-layout="1"][data-scoop-screener-gated="1"] {{
{_DESKTOP_SCREENER_GATING_LAYOUT_RULES}
}}
"""

# Mobile/tablet screener landing pages: collapse bootstrap gaps (js_eval, stHtml, page CSS).
_RESPONSIVE_SCREENER_TOP_COMPACT_RULES = """
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]),
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stHtml"]),
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stHtml"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style),
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] style) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.6rem !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(+ [data-testid="stElementContainer"] h1),
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(+ [data-testid="element-container"] h1) {
        margin-bottom: 0 !important;
        padding-bottom: 0 !important;
    }
    /* Market pages: index banner cards fill the viewport (desktop keeps inline 50%). */
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"],
    html[data-scoop-screener-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stMarkdownContainer"] > div,
    html[data-scoop-screener-active="1"] .scoop-banner-compact,
    html[data-scoop-screener-active="1"] .scoop-banner-desktop,
    html[data-scoop-screener-active="1"] [data-testid="stMarkdownContainer"] div[style*="display:flex"][style*="flex-wrap"][style*="margin-bottom"] {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-screener-active="1"] [data-testid="stMarkdownContainer"] div[style*="max-width:50%"],
    html[data-scoop-screener-active="1"] [data-testid="stMarkdownContainer"] div[style*="max-width: 50%"],
    html[data-scoop-screener-active="1"] .scoop-banner-compact > div,
    html[data-scoop-screener-active="1"] .scoop-banner-desktop > div {
        flex: 1 1 100% !important;
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        box-sizing: border-box !important;
    }
"""

# Mobile/tablet terms gate checkbox — restore compact page styling (not Dark mode box).
_MOBILE_TABLET_TERMS_CHECKBOX_RESTORE = f"""
@media (max-width: 1366px) {{
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)),
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"],
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"] {{
        padding: 0.5rem 0.8rem !important;
        margin-top: 0.35rem !important;
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        width: 100% !important;
        max-width: 100% !important;
        height: auto !important;
        min-height: 0 !important;
        max-height: none !important;
        font-size: inherit !important;
        overflow: visible !important;
    }}
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"] label p {{
        font-size: inherit !important;
        line-height: normal !important;
    }}
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"] [data-testid="stTooltipIcon"],
    html[data-scoop-screener-gated="1"] {_MOBILE_TAB_MAIN} [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(.scoop-mobile-inner-top-toggle)) div[data-testid="stCheckbox"] [data-testid="stTooltipIcon"] {{
        font-size: 14px !important;
        width: 14px !important;
        height: 14px !important;
    }}
}}
"""

# Mobile/tablet market pages: space between dark-mode row and index banner cards.
_MOBILE_SCREENER_TOGGLE_BANNER_GAP_FINAL = f"""
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stToggle"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} div[data-testid="stCheckbox"] {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_SCREENER_INDEX_BANNER_CONTAINER} {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} + [data-testid="stElementContainer"],
    html[data-scoop-tab-nav="1"] {_MOBILE_TAB_DARK_MODE_ROW} + [data-testid="element-container"] {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
"""

# Mobile/tablet gated view: space between terms checkbox and disclaimer footer.
_MOBILE_TABLET_CONSENT_DISCLAIMER_GAP_FINAL = f"""
@media (max-width: 1366px) {{
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] {_MOBILE_TAB_TERMS_CHECKBOX_ROW} {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
        padding-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] {_MOBILE_TAB_TERMS_CHECKBOX_ROW} div[data-testid="stCheckbox"] {{
        margin-bottom: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] {_MOBILE_TAB_TERMS_CHECKBOX_ROW} + [data-testid="stElementContainer"],
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] {_MOBILE_TAB_TERMS_CHECKBOX_ROW} + [data-testid="element-container"],
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.disclaimer-footer),
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.disclaimer-footer) {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
    html[data-scoop-tab-nav="1"][data-scoop-screener-gated="1"] .disclaimer-footer {{
        margin-top: {_DESKTOP_MARKET_NAV_GAP} !important;
    }}
}}
"""

_MOBILE_TABLET_DARK_MODE_UNBOX_ALWAYS = f"""
@media (max-width: 1366px) {{
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] {{
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }}
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stToggle"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stToggle"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stCheckbox"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stCheckbox"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="stElementContainer"]:has([data-testid="stToggle"]) [data-testid="stToggle"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="element-container"]:has([data-testid="stToggle"]) [data-testid="stToggle"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(+ [data-testid="stElementContainer"] .disclaimer-footer)) [data-testid="stCheckbox"],
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(+ [data-testid="element-container"] .disclaimer-footer)) [data-testid="stCheckbox"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_CHROME}
    }}
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(+ [data-testid="stElementContainer"] .disclaimer-footer)) [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="element-container"]:has([data-testid="stCheckbox"]):not(:has(+ [data-testid="element-container"] .disclaimer-footer)) [data-testid="stCheckbox"] label p,
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stCheckbox"] label p,
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] label p {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL}
    }}
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-baseweb="switch"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH}
    }}
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-baseweb="switch"] > div {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH_KNOB}
    }}
    html body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_TIP}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-baseweb="checkbox"] > div:first-child {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-baseweb="checkbox"] > div:first-child > div {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_SWITCH_KNOB}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_TIP}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-baseweb="checkbox"],
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] > label {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_ROW}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-baseweb="checkbox"] > div:has([data-testid="stWidgetLabel"]) {{
        width: auto !important;
        max-width: none !important;
        flex: 0 0 auto !important;
        display: inline-flex !important;
        align-items: center !important;
        position: static !important;
        overflow: visible !important;
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stWidgetLabel"],
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stWidgetLabel"] {{
{_MOBILE_TABLET_DARK_MODE_TOGGLE_LABEL_SHELL}
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stMarkdownContainer"],
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stMarkdownContainer"] {{
        margin: 0 !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
    }}
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipHoverTarget"],
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipHoverTarget"],
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] button,
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] button {{
        position: static !important;
        display: inline-flex !important;
        align-items: center !important;
        transform: none !important;
        inset: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }}
    html[data-scoop-theme="dark"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(.scoop-mobile-inner-top-toggle) ~ [data-testid="stElementContainer"]:has([data-testid="stCheckbox"]):not(:has(+ [data-testid="stElementContainer"] .disclaimer-footer)) [data-testid="stCheckbox"] [data-testid="stWidgetLabel"] p {{
        color: #ffffff !important;
    }}
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] label p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"],
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] button,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] svg,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"],
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] button,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] svg {{
        color: #ffffff !important;
        stroke: #ffffff !important;
    }}
}}
"""

RESPONSIVE_SCREENER_TOP_COMPACT = f"""
@media (max-width: 1366px) {{
{_RESPONSIVE_SCREENER_TOP_COMPACT_RULES}
{_MOBILE_SCREENER_TOGGLE_BANNER_GAP_FINAL}
}}
""" + _MARKET_MOBILE_TABLET_TOGGLE_BOXED + _MOBILE_TABLET_TERMS_CHECKBOX_RESTORE + _MOBILE_TABLET_DARK_MODE_PILL_LAYOUT_FINAL + _MOBILE_TABLET_CONSENT_DISCLAIMER_GAP_FINAL + _MOBILE_TABLET_DARK_MODE_UNBOX_ALWAYS

# Mobile/tablet Terms page: collapse bootstrap gaps before title and divider lines.
_DESKTOP_TERMS_TOP_COMPACT_RULES = """
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"],
    html[data-scoop-terms-active="1"] section.main > div,
    html[data-scoop-terms-active="1"] [data-testid="stAppViewContainer"] > section.main {
        padding-top: 12px !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stHtml"]),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stHtml"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] style) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.35rem !important;
    }
"""

DESKTOP_TERMS_TOP_COMPACT = f"""
@media (min-width: 1367px) {{
{_DESKTOP_TERMS_TOP_COMPACT_RULES}
}}
html[data-scoop-desktop-layout="1"][data-scoop-terms-active="1"] {{
{_DESKTOP_TERMS_TOP_COMPACT_RULES}
}}
"""

_RESPONSIVE_TERMS_TOP_COMPACT_RULES = """
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"] {
        gap: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has(iframe[src*="streamlit_js_eval"]),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has(iframe[src*="streamlit_js_eval"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stHtml"]),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stHtml"]) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] style),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] style) {
        margin: 0 !important;
        padding: 0 !important;
        min-height: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] hr:not(.search-52w-range-divider) {
        display: none !important;
        margin: 0 !important;
        padding: 0 !important;
        border: none !important;
        height: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)),
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"]:has([data-testid="stMarkdownContainer"] hr:not(.search-52w-range-divider)) {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stMainBlockContainer"] h1 {
        margin-top: 0.5rem !important;
        margin-bottom: 0.35rem !important;
    }
"""

RESPONSIVE_TERMS_TOP_COMPACT = f"""
@media (max-width: 1366px) {{
{_RESPONSIVE_TERMS_TOP_COMPACT_RULES}
}}
"""

# Phone mobile (≤743px): Terms page stays in overlay-sidebar layout (not desktop split).
MOBILE_CONSENT_TERMS_MAIN_VIEW_CSS = """
@media (max-width: 743px) {
    html[data-scoop-terms-active="1"] [data-testid="stAppViewContainer"],
    html[data-scoop-terms-active="1"][data-scoop-desktop-layout="1"] [data-testid="stAppViewContainer"],
    html[data-scoop-terms-active="1"][data-scoop-screener-gated="1"] [data-testid="stAppViewContainer"] {
        display: block !important;
        flex-direction: column !important;
        width: 100% !important;
        max-width: 100vw !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    html[data-scoop-terms-active="1"] [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]),
    html[data-scoop-terms-active="1"] [data-testid="stAppViewContainer"] > section.main {
        width: 100% !important;
        max-width: 100vw !important;
        flex: none !important;
    }
    html[data-scoop-terms-active="1"] section[data-testid="stSidebar"]:not([aria-expanded="true"]),
    html[data-scoop-terms-active="1"][data-scoop-desktop-layout="1"] section[data-testid="stSidebar"]:not([aria-expanded="true"]) {
        position: fixed !important;
        transform: translateX(-100vw) !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
    html[data-scoop-terms-active="1"] .scoop-banner-desktop,
    html[data-scoop-terms-active="1"][data-scoop-screener-gated="1"] .scoop-banner-desktop {
        display: none !important;
    }
}
"""

TABLET_SEARCH_MOBILE_LAYOUT = (
    """
        .stApp { overflow-x: hidden !important; }
"""
    + TABLET_TYPE
    + """
        h3.search-price-chart-heading { margin-bottom: 0.25rem !important; }
        h3.search-52week-range-heading { margin-bottom: 0.35rem !important; }
        hr.search-52w-range-divider { margin: 0.1rem 0 !important; }

        .mood-column { margin-top: 0 !important; }
        .mood-feed {
            height: auto !important;
            max-height: none !important;
            overflow: visible !important;
            margin-bottom: 0 !important;
            padding-bottom: 0.25rem !important;
            font-size: clamp(1.15rem, 2.5vw, 1.38rem) !important;
            line-height: 1.62 !important;
        }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

"""
    + RESPONSIVE_GENERIC_TOOLTIP_LAYOUT
)

TABLET_TERMS_MOBILE_LAYOUT = TABLET_TYPE

# Phone portrait (≤743px): full off-screen sidebar retract (iPhone, etc.); tablet/desktop unchanged.
PHONE_SIDEBAR_LAYOUT = f"""
    /* ===== Phone mobile (≤743px) — overlay sidebar full off-screen retract; tablet/desktop unchanged ===== */
    @media (max-width: 743px) {{
{SURFACE_DUO_SIDEBAR}
    }}
"""

# iPad Mini portrait (744–768px): overlay above Deploy bar, plain arrows like Surface Duo.
IPAD_MINI_PORTRAIT_LAYOUT = f"""
    /* ===== iPad Mini portrait (744px–768px) — overlay sidebar; phones/tablet/desktop unchanged ===== */
    @media (min-width: 744px) and (max-width: 768px) {{
{SURFACE_DUO_SIDEBAR}
    }}
"""

# iPad Mini (744–768px): keep generic + headlines popups inside the viewport (no clip/off-page).
_IPAD_MINI_POPUP_SCOPE = (
    'html body .stApp [data-testid="stAppViewContainer"] .stMarkdown'
)
IPAD_MINI_POPUP_CLAMP_CSS = f"""
@media (min-width: 744px) and (max-width: 768px) {{
        {_IPAD_MINI_POPUP_SCOPE} .tip-wrap:not(.headlines-tip).scoop-mobile-tip-open .tip-text {{
            box-sizing: border-box !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            max-height: min(calc(100dvh - 1.5rem), calc(100vh - 1.5rem), var(--scoop-ipad-mini-tip-max-height, 28rem)) !important;
        }}
        {_IPAD_MINI_POPUP_SCOPE} .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text {{
            box-sizing: border-box !important;
            top: var(--hl-fixed-top, 90px) !important;
            left: var(--hl-fixed-left, 50%) !important;
            right: auto !important;
            width: var(--hl-fixed-width, min(20rem, calc(100vw - 1.5rem))) !important;
            max-width: var(--hl-fixed-width, min(20rem, calc(100vw - 1.5rem))) !important;
            overflow: hidden !important;
            max-height: min(var(--hl-fixed-max-height, calc(100dvh - 90px - 30px)), calc(100dvh - 90px - 30px), calc(100vh - 90px - 30px)) !important;
        }}
        {_IPAD_MINI_POPUP_SCOPE} .full-results-wrap .tip-wrap.headlines-tip:has(.hl-tip-cb:checked) .tip-text .headlines-tip-scroll {{
            min-height: 0 !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            overscroll-behavior-y: contain !important;
        }}
}}
"""

# Injected early on every page (via theme_mode) so mobile/tablet overlay sidebar wins first paint.
TABLET_SIDEBAR_TOGGLE_AVAILABILITY = """
    /* Tablet (769–1366): keep Streamlit sidebar chevrons only when NOT using tab navigation. */
    @media (min-width: 769px) and (max-width: 1366px) {
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stHeader"] [data-testid="collapsedControl"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="collapsedControl"] {
            display: none !important;
        }
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stSidebarCollapseButton"],
        html:not([data-scoop-tab-nav="1"]) .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
            display: flex !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        html:not([data-scoop-tab-nav="1"]) section[data-testid="stSidebar"][aria-expanded="false"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
        }
    }
"""

RESPONSIVE_SIDEBAR_BOOTSTRAP = f"""
@media (max-width: 1366px) {{
{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
}}
{TABLET_SIDEBAR_TOGGLE_AVAILABILITY}
{PHONE_SIDEBAR_LAYOUT}
{IPAD_MINI_PORTRAIT_LAYOUT}
"""

TABLET_SCREENER_INNER = f"""{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
{TABLET_SCREENER_MOBILE_LAYOUT}"""

TABLET_SEARCH_INNER = f"""{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
{TABLET_SEARCH_MOBILE_LAYOUT}"""

TABLET_TERMS_INNER = f"""{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
{TABLET_TERMS_MOBILE_LAYOUT}"""

_ZENBOOK_FOLDED_MEDIA = (
    "(min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),\n"
    "           (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px)"
)

# Unfolded Zenbook exceeds the 1367px desktop breakpoint at common OS scale factors
# (e.g. 1920×1280 CSS px at 150% on 2880×1920 panel).
_ZENBOOK_UNFOLDED_MEDIA = (
    "(min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),\n"
    "           (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),\n"
    "           (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px)"
)

# iPad Mini portrait uses SURFACE_DUO_SIDEBAR + mobile card layout (≤768px).
# Zenbook Fold reuses that overlay sidebar with the shared card-layout rules.
_ZENBOOK_IPAD_MINI_SCREENER_INNER = f"""{SURFACE_DUO_SIDEBAR}
{TABLET_SCREENER_MOBILE_LAYOUT}"""

_ZENBOOK_IPAD_MINI_SEARCH_INNER = f"""{SURFACE_DUO_SIDEBAR}
{TABLET_SEARCH_MOBILE_LAYOUT}"""

_ZENBOOK_IPAD_MINI_TERMS_INNER = f"""{SURFACE_DUO_SIDEBAR}
{TABLET_TERMS_MOBILE_LAYOUT}"""

# Beat desktop split-sidebar when unfolded width exceeds 1366px.
_ZENBOOK_DESKTOP_SIDEBAR_BEAT = IPAD_14_PRO_MAX_LANDSCAPE_OVERRIDE

ASUS_ZENBOOK_FOLD_SCREENER_LAYOUT = f"""
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (folded) ===== */
    @media {_ZENBOOK_FOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_SCREENER_INNER}
    }}
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (unfolded) ===== */
    @media {_ZENBOOK_UNFOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_SCREENER_INNER}
{_ZENBOOK_DESKTOP_SIDEBAR_BEAT}
    }}
"""

ASUS_ZENBOOK_FOLD_SEARCH_LAYOUT = f"""
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (folded) ===== */
    @media {_ZENBOOK_FOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_SEARCH_INNER}
    }}
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (unfolded) ===== */
    @media {_ZENBOOK_UNFOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_SEARCH_INNER}
{_ZENBOOK_DESKTOP_SIDEBAR_BEAT}
    }}
"""

ASUS_ZENBOOK_FOLD_TERMS_LAYOUT = f"""
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (folded) ===== */
    @media {_ZENBOOK_FOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_TERMS_INNER}
    }}
    /* ===== Asus Zenbook Fold only — iPad Mini-style overlay (unfolded) ===== */
    @media {_ZENBOOK_UNFOLDED_MEDIA} {{
{_ZENBOOK_IPAD_MINI_TERMS_INNER}
{_ZENBOOK_DESKTOP_SIDEBAR_BEAT}
    }}
"""

# Mobile/tablet tab navigation — replaces slide-out sidebar; desktop split sidebar unchanged.
_RESPONSIVE_TAB_NAV_HIDE_SIDEBAR_RULES = """
    html[data-scoop-tab-nav="1"] section[data-testid="stSidebar"],
    html[data-scoop-tab-nav="1"] [data-testid="stSidebarBackdrop"],
    html[data-scoop-tab-nav="1"] [data-testid="stSidebarNav"],
    html[data-scoop-tab-nav="1"] [data-testid="stSidebarCollapseButton"],
    html[data-scoop-tab-nav="1"] [data-testid="stExpandSidebarButton"],
    html[data-scoop-tab-nav="1"] [data-testid="collapsedControl"],
    html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
    html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="collapsedControl"],
    html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
        transform: none !important;
    }
    html[data-scoop-tab-nav="1"] [data-testid="stAppViewContainer"] {
        display: block !important;
        width: 100% !important;
        max-width: 100vw !important;
        margin-left: 0 !important;
        padding-left: 0 !important;
    }
    html[data-scoop-tab-nav="1"] [data-testid="stAppViewContainer"] section.main,
    html[data-scoop-tab-nav="1"] [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]) {
        width: 100% !important;
        max-width: 100vw !important;
        margin-left: 0 !important;
    }
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"],
    html[data-scoop-tab-nav="1"] section.main > div,
    html[data-scoop-tab-nav="1"] [data-testid="stAppViewContainer"] > section.main {
        padding-top: 0.25rem !important;
    }
"""

# Final cascade — beats tablet overlay sidebar rules that re-show Streamlit chevrons.
_RESPONSIVE_TAB_NAV_HIDE_SIDEBAR_CONTROLS_FINAL = """
    @media (max-width: 1366px) {
        html[data-scoop-tab-nav="1"] [data-testid="stExpandSidebarButton"],
        html[data-scoop-tab-nav="1"] [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] [data-testid="collapsedControl"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="collapsedControl"],
        html[data-scoop-tab-nav="1"] section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"]) [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"]) [data-testid="stHeader"] [data-testid="collapsedControl"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"]) [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"]) section[data-testid="stSidebar"] [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="false"]) [data-testid="stHeader"] [data-testid="collapsedControl"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="collapsedControl"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stSidebarCollapseButton"],
        html[data-scoop-tab-nav="1"] .stApp:has(section[data-testid="stSidebar"][aria-expanded="true"]) [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
            min-width: 0 !important;
            min-height: 0 !important;
            max-width: 0 !important;
            max-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            overflow: hidden !important;
            clip: rect(0, 0, 0, 0) !important;
            position: absolute !important;
            left: -9999px !important;
            top: auto !important;
        }
        html[data-scoop-tab-nav="1"] [data-testid="stExpandSidebarButton"] button,
        html[data-scoop-tab-nav="1"] [data-testid="stSidebarCollapseButton"] button,
        html[data-scoop-tab-nav="1"] [data-testid="collapsedControl"] button,
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] button,
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] button,
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="collapsedControl"] button,
        html[data-scoop-tab-nav="1"] [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
        html[data-scoop-tab-nav="1"] [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
        html[data-scoop-tab-nav="1"] [data-testid="collapsedControl"] [data-testid="stIconMaterial"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] [data-testid="stIconMaterial"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stSidebarCollapseButton"] [data-testid="stIconMaterial"],
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="collapsedControl"] [data-testid="stIconMaterial"] {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
            width: 0 !important;
            height: 0 !important;
            overflow: hidden !important;
        }
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stToolbar"] > div:first-child:has([data-testid="stExpandSidebarButton"]),
        html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stToolbar"] > div:first-child:has([data-testid="collapsedControl"]) {
            display: none !important;
            visibility: hidden !important;
            width: 0 !important;
            min-width: 0 !important;
            max-width: 0 !important;
            overflow: hidden !important;
            pointer-events: none !important;
        }
    }
"""

RESPONSIVE_TAB_NAV_HIDE_SIDEBAR = f"""
@media (max-width: 1366px) {{
{_RESPONSIVE_TAB_NAV_HIDE_SIDEBAR_RULES}
}}
@media (width: 540px),
       (width: 720px) and (max-height: 541px),
       (min-width: 1110px) and (max-width: 1118px) and (max-height: 741px),
       (min-width: 1028px) and (max-width: 1036px) and (min-height: 1370px),
       (min-width: 1370px) and (max-width: 1382px) and (max-height: 1040px),
       (min-width: 849px) and (max-width: 857px) and (min-height: 1276px) and (max-height: 1284px),
       (min-width: 1276px) and (max-width: 1284px) and (min-height: 849px) and (max-height: 857px),
       (min-width: 1700px) and (max-width: 1714px) and (min-height: 1000px) and (max-height: 1120px),
       (min-width: 1910px) and (max-width: 1930px) and (min-height: 1270px) and (max-height: 1290px),
       (min-width: 1270px) and (max-width: 1290px) and (min-height: 1910px) and (max-height: 1930px) {{
{_RESPONSIVE_TAB_NAV_HIDE_SIDEBAR_RULES}
}}
"""

RESPONSIVE_TAB_NAV_SHELL = """
@media (max-width: 1366px) {
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-shell {
        display: block !important;
    }
}
@media (min-width: 1367px) {
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-shell {
        display: none !important;
    }
}
"""

RESPONSIVE_TAB_NAV_BAR = """
@media (max-width: 1366px) {
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-shell {
        margin: 0 0 0.75rem 0;
        padding: 0 clamp(0.5rem, 2vw, 0.85rem);
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-header {
        display: flex !important;
        align-items: center !important;
        gap: 0.65rem !important;
        margin-bottom: 0.55rem !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-header [data-testid="stImage"] {
        flex: 0 0 auto !important;
        width: 3.25rem !important;
        min-width: 3.25rem !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-header [data-testid="stImage"] img {
        width: 100% !important;
        height: auto !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-title {
        flex: 1 1 auto !important;
        font-size: 1.35rem !important;
        font-weight: 800 !important;
        line-height: 1.15 !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-nav-toggle {
        flex: 0 0 auto !important;
        min-width: 6.5rem !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-wrap: nowrap !important;
        overflow-x: auto !important;
        gap: 0.45rem !important;
        -webkit-overflow-scrolling: touch !important;
        scrollbar-width: none !important;
        padding-bottom: 0.15rem !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stHorizontalBlock"]::-webkit-scrollbar {
        display: none !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="column"] {
        flex: 0 0 auto !important;
        width: auto !important;
        min-width: max-content !important;
    }
    html:not([data-scoop-theme="dark"]) .scoop-mobile-tab-row [data-testid="stPageLink"] {
        border: 2px solid #334155 !important;
        border-radius: 999px !important;
        background: #ffffff !important;
        padding: 0.1rem 0.2rem !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06) !important;
        white-space: nowrap !important;
    }
    html:not([data-scoop-theme="dark"]) .scoop-mobile-tab-row [data-testid="stPageLink"][data-scoop-nav-active] {
        background: #dbeafe !important;
        border-color: #1d4ed8 !important;
    }
    html:not([data-scoop-theme="dark"]) .scoop-mobile-tab-row [data-testid="stPageLink"] a {
        padding: 0.35rem 0.7rem !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        white-space: nowrap !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-tab-row [data-testid="stPageLink"] {
        border: 2px solid #94a3b8 !important;
        border-radius: 999px !important;
        background: #000000 !important;
        padding: 0.1rem 0.2rem !important;
        white-space: nowrap !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-tab-row [data-testid="stPageLink"][data-scoop-nav-active] {
        background: #333333 !important;
        border-color: #e2e8f0 !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-tab-row [data-testid="stPageLink"] a {
        padding: 0.35rem 0.7rem !important;
        font-size: 0.82rem !important;
        color: #ffffff !important;
        white-space: nowrap !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-back-home {
        display: inline-flex !important;
        align-items: center !important;
        margin: 0 0 0.45rem 0 !important;
        padding: 0.35rem 0.75rem !important;
        border-radius: 999px !important;
        border: 2px solid #334155 !important;
        background: #f8fafc !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        color: #0f172a !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-back-home {
        border-color: #94a3b8 !important;
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-back-row {
        margin: 0 0 0.45rem 0 !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-back-row [data-testid="stPageLink"] {
        width: fit-content !important;
    }
    html[data-scoop-tab-nav="1"] .scoop-mobile-back-row [data-testid="stPageLink"] a {
        display: inline-flex !important;
        align-items: center !important;
        padding: 0.35rem 0.75rem !important;
        border-radius: 999px !important;
        border: 2px solid #334155 !important;
        background: #f8fafc !important;
        font-size: 0.85rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-back-row [data-testid="stPageLink"] a {
        border-color: #94a3b8 !important;
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
}
"""

MOBILE_BACK_HOME_BAR = """
@media (max-width: 1366px) {
    .scoop-mobile-back-home-bar {
        position: fixed !important;
        top: calc(0.4rem + env(safe-area-inset-top, 0px)) !important;
        left: 0 !important;
        right: 0 !important;
        z-index: 1000010 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        gap: 0.5rem !important;
        width: 100vw !important;
        max-width: 100vw !important;
        padding-left: calc(0.55rem + env(safe-area-inset-left, 0px)) !important;
        padding-right: calc(0.55rem + env(safe-area-inset-right, 0px)) !important;
        box-sizing: border-box !important;
        pointer-events: auto !important;
    }
    html[data-scoop-tab-nav="1"] [data-testid="stHeader"] [data-testid="stToolbar"] {
        visibility: hidden !important;
        pointer-events: none !important;
    }
    .scoop-mobile-back-home-bar .scoop-mobile-back-home {
        display: inline-flex !important;
        align-items: center !important;
        margin: 0 !important;
        padding: 0.4rem 0.8rem !important;
        border-radius: 999px !important;
        border: 2px solid #334155 !important;
        background: #f8fafc !important;
        font-size: 0.88rem !important;
        font-weight: 700 !important;
        text-decoration: none !important;
        color: #0f172a !important;
        box-shadow: 0 1px 3px rgba(15, 23, 42, 0.12) !important;
        white-space: nowrap !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-back-home-bar .scoop-mobile-back-home {
        border-color: #94a3b8 !important;
        background: #1e293b !important;
        color: #f1f5f9 !important;
    }
    .scoop-mobile-fixed-dark {
        display: inline-flex !important;
        align-items: center !important;
        gap: 0.4rem !important;
        margin: 0 !important;
        padding: 0.2rem 0.15rem !important;
        cursor: pointer !important;
        user-select: none !important;
        color: #0f172a !important;
        font-size: clamp(0.94rem, 2.6vw, 1.08rem) !important;
        font-weight: 600 !important;
        line-height: 1 !important;
        white-space: nowrap !important;
        overflow: visible !important;
        flex: 0 0 auto !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-fixed-dark {
        color: #ffffff !important;
    }
    .scoop-mobile-fixed-dark-cb {
        position: absolute !important;
        opacity: 0 !important;
        width: 1px !important;
        height: 1px !important;
        pointer-events: none !important;
    }
    .scoop-mobile-fixed-dark-switch {
        display: inline-block !important;
        width: 2.35rem !important;
        height: 1.25rem !important;
        border-radius: 999px !important;
        background: #cbd5e1 !important;
        box-shadow: inset 0 0 0 1px #94a3b8 !important;
        position: relative !important;
        flex: 0 0 auto !important;
    }
    .scoop-mobile-fixed-dark-switch::after {
        content: "" !important;
        position: absolute !important;
        top: 0.12rem !important;
        left: 0.12rem !important;
        width: 1rem !important;
        height: 1rem !important;
        border-radius: 50% !important;
        background: #ffffff !important;
        box-shadow: 0 1px 2px rgba(15, 23, 42, 0.28) !important;
        transition: left 0.15s ease !important;
    }
    .scoop-mobile-fixed-dark-cb:checked + .scoop-mobile-fixed-dark-switch {
        background: #334155 !important;
    }
    .scoop-mobile-fixed-dark-cb:checked + .scoop-mobile-fixed-dark-switch::after {
        left: 1.2rem !important;
    }
    html[data-scoop-theme="dark"] .scoop-mobile-fixed-dark-switch {
        background: #334155 !important;
        box-shadow: inset 0 0 0 1px #94a3b8 !important;
    }
    .scoop-mobile-back-home-spacer {
        display: block !important;
        height: 2.35rem !important;
        margin: 0 0 0.25rem 0 !important;
        pointer-events: none !important;
    }
}
@media (min-width: 1367px) {
    .scoop-mobile-back-home-bar,
    .scoop-mobile-back-home-spacer {
        display: none !important;
        visibility: hidden !important;
        pointer-events: none !important;
    }
}
"""

MOBILE_INNER_TOP_BAR = """
@media (max-width: 1366px) {
    .scoop-mobile-inner-top {
        display: block !important;
        margin: 0 0 12px 0 !important;
        padding: 0 !important;
    }
    .scoop-mobile-inner-top [data-testid="stHorizontalBlock"] {
        align-items: center !important;
        gap: 0.35rem !important;
        margin: 0 !important;
    }
    .scoop-mobile-inner-top-toggle {
        display: flex !important;
        justify-content: flex-end !important;
        align-items: center !important;
        min-width: 0 !important;
        width: 100% !important;
    }
    html[data-scoop-tab-nav="1"]:not([data-scoop-home-page="1"]) [data-testid="stMainBlockContainer"],
    html[data-scoop-tab-nav="1"]:not([data-scoop-home-page="1"]) section.main > div,
    html[data-scoop-tab-nav="1"]:not([data-scoop-home-page="1"]) [data-testid="stAppViewContainer"] > section.main {
        padding-top: 0.25rem !important;
    }
    [data-testid="stMainBlockContainer"] [data-testid="stToggle"],
    [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has([data-baseweb="switch"]),
    [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has([aria-label="Dark mode"]) {
        background: transparent !important;
        background-color: transparent !important;
        border: none !important;
        border-radius: 0 !important;
        padding: 0 !important;
        box-shadow: none !important;
    }
}
@media (min-width: 1367px) {
    .scoop-mobile-inner-top {
        display: none !important;
    }
}
"""

RESPONSIVE_HOME_LANDING = (
    """
@media (max-width: 1366px) {
    html[data-scoop-home-page="1"] section[data-testid="stSidebar"] {
        display: none !important;
        width: 0 !important;
        min-width: 0 !important;
        max-width: 0 !important;
        overflow: hidden !important;
        pointer-events: none !important;
    }
    html[data-scoop-home-page="1"] .stApp,
    html[data-scoop-home-page="1"] [data-testid="stAppViewContainer"] {
        display: block !important;
        width: 100vw !important;
        max-width: 100vw !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow-x: hidden !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stAppViewContainer"] > section.main,
    html[data-scoop-home-page="1"] [data-testid="stAppViewContainer"] > div:not([data-testid="stSidebar"]),
    html[data-scoop-home-page="1"] section.main > div,
    html[data-scoop-home-page="1"] section.main .block-container {
        width: 100% !important;
        max-width: 100% !important;
        min-width: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-left: 0 !important;
        padding-right: 0 !important;
        padding-top: 0 !important;
        margin-top: 0 !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        padding-top: 1rem !important;
        padding-bottom: 1rem !important;
        padding-left: var(--scoop-home-side-padding, 20px) !important;
        padding-right: var(--scoop-home-side-padding, 20px) !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stVerticalBlock"],
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="block-container"] {
        gap: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="element-container"],
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stElementContainer"] {
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-home-page="1"] [data-testid="element-container"] {
        width: 100% !important;
        max-width: 100% !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stCustomComponentV1"] {
        min-height: 0 !important;
        height: auto !important;
        margin: 0 !important;
        padding: 0 !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stCustomComponentV1"] iframe,
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] iframe {
        display: block !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        border: 0 !important;
        overflow: hidden !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stSidebarNav"] {
        display: none !important;
    }
    html[data-scoop-home-page="1"] .scoop-env-banner {
        display: none !important;
        height: 0 !important;
        min-height: 0 !important;
        margin: 0 !important;
        padding: 0 !important;
        overflow: hidden !important;
        visibility: hidden !important;
    }
    html[data-scoop-home-page="1"] .scoop-home-landing {
        padding: 0 !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    html[data-scoop-home-page="1"] .scoop-home-landing h1 {
        display: none !important;
    }
    html[data-scoop-home-page="1"] .scoop-home-landing p {
        font-size: clamp(1rem, 4vw, 1.5rem) !important;
        line-height: 1.45 !important;
        margin: 0 !important;
        color: #0f172a !important;
        width: 100% !important;
        max-width: 100% !important;
    }
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] .scoop-home-landing p {
        color: #e2e8f0 !important;
    }
"""
    + _HOME_SIDEBAR_BRAND_AND_TYPE_RULES
    + _HOME_BRAND_TOGGLE_BUFFER_RULES
    + _HOME_MARKET_NAV_BASE_RULES
    + _HOME_MARKET_NAV_LIGHT_RULES
    + _HOME_MARKET_NAV_DARK_RULES
    + """
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href$="_Top_10"]) {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
    }
    html[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]) {
        display: block !important;
        width: 100% !important;
        margin-top: 0 !important;
        margin-left: 0 !important;
        margin-right: 0 !important;
        margin-bottom: 0 !important;
        border: none !important;
        background: transparent !important;
        box-shadow: none !important;
    }
    html:not([data-scoop-theme="dark"])[data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]) a {
        display: inline-flex !important;
        width: 100% !important;
        max-width: 100% !important;
        padding: 0.25rem 0 !important;
        font-size: clamp(1rem, 4.2vw, 1.5rem) !important;
        font-weight: 400 !important;
        text-align: left !important;
        color: #0f172a !important;
        box-sizing: border-box !important;
    }
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Terms_of_Service"]) a {
        color: #93c5fd !important;
        font-size: clamp(1rem, 4.2vw, 1.5rem) !important;
        font-weight: 400 !important;
        width: 100% !important;
        max-width: 100% !important;
        box-sizing: border-box !important;
    }
"""
    + _HOME_MARKET_NAV_GAP_SPACER_RULES
    + _HOME_DESCRIPTION_TO_NAV_FINAL
    + """
}
"""
    + _HOME_LOGO_MOBILE_RULES
    + _HOME_LOGO_TABLET_RULES
    + _HOME_LOGO_TOP_CLEARANCE_FINAL
)

# Mobile/tablet only — hover/press shade on market and tab buttons (dark on light, light on dark).
_MOBILE_TABLET_BUTTON_HOVER_SHADER = """
@media (max-width: 1366px) {
    html[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]),
    html[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"] {
        transition: background-color 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease !important;
    }
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):hover,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):active,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:hover,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:active {
        background: #94a3b8 !important;
        box-shadow: inset 0 0 0 999px rgba(15, 23, 42, 0.22), 0 8px 22px rgba(15, 23, 42, 0.42) !important;
    }
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):hover a,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):active a,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:hover a,
    html:not([data-scoop-theme="dark"])[data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:active a {
        background-color: rgba(15, 23, 42, 0.18) !important;
    }
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):hover,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):active,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:hover,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:active {
        background: #475569 !important;
        box-shadow: inset 0 0 0 999px rgba(248, 250, 252, 0.2), 0 8px 22px rgba(248, 250, 252, 0.32) !important;
    }
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):hover a,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] [data-testid="stMainBlockContainer"] [data-testid="stPageLink"]:has(a[href*="Top_10"]):active a,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:hover a,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] .scoop-mobile-tab-row [data-testid="stPageLink"]:active a {
        background-color: rgba(248, 250, 252, 0.16) !important;
        color: #ffffff !important;
    }
}
"""

# Mobile/tablet dark mode — Dark mode label + help icon stay white.
_MOBILE_TABLET_DARK_MODE_LABEL_WHITE = """
@media (max-width: 1366px) {
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) label p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stWidgetLabel"] p,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] label p {
        color: #ffffff !important;
    }
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"],
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] button,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stCheckbox"]:has(input[aria-label="Dark mode"]) [data-testid="stTooltipIcon"] svg,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"],
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] button,
    html[data-scoop-theme="dark"][data-scoop-tab-nav="1"] body .stApp [data-testid="stMainBlockContainer"] [data-testid="stToggle"] [data-testid="stTooltipIcon"] svg {
        color: #ffffff !important;
        stroke: #ffffff !important;
    }
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .sidebar-brand-text,
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] #scoop-title,
    html[data-scoop-theme="dark"][data-scoop-home-page="1"] [data-testid="stMainBlockContainer"] .sidebar-brand #scoop-title {
        color: #ffffff !important;
        text-decoration-color: #ffffff !important;
    }
}
"""

RESPONSIVE_TAB_NAV_BOOTSTRAP = (
    RESPONSIVE_TAB_NAV_HIDE_SIDEBAR
    + RESPONSIVE_TAB_NAV_SHELL
    + RESPONSIVE_TAB_NAV_BAR
    + MOBILE_BACK_HOME_BAR
    + MOBILE_INNER_TOP_BAR
    + RESPONSIVE_HOME_LANDING
    + _RESPONSIVE_TAB_NAV_HIDE_SIDEBAR_CONTROLS_FINAL
    + MOBILE_TABLET_TOGGLE_STYLE
    + _MOBILE_TABLET_TOGGLE_FINAL
    + _HOME_MOBILE_TABLET_TOGGLE_BOXED
    + _MOBILE_TABLET_DARK_MODE_PILL_LAYOUT_FINAL
    + _MOBILE_TABLET_CONSENT_DISCLAIMER_GAP_FINAL
    + _HOME_LOGO_TOP_CLEARANCE_FINAL
    + _MOBILE_TABLET_BUTTON_HOVER_SHADER
    + _MOBILE_TABLET_DARK_MODE_LABEL_WHITE
    + _MOBILE_TABLET_ANALYZE_LINK_FINAL
)
