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
            color: #ffffff !important;
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
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-link {
            display: none !important;
        }
        .stMarkdown .full-results-wrap .full-results-table .fr-analyze-cell .fr-analyze-mobile-tip {
            display: inline-block !important;
            cursor: help !important;
            border-bottom: 1px dashed #888 !important;
            color: inherit !important;
            font-weight: 600 !important;
            text-decoration: none !important;
        }
"""

# Mobile/tablet: generic info tooltips mirror desktop (above trigger, CSS :hover only).
# Name/Company/Commodity values sit at the top of each card — their tips open below
# the trigger so they are not clipped by the card's overflow:hidden.
_RESPONSIVE_TIP_SCOPE = (
    "html body .stApp [data-testid=\"stAppViewContainer\"] .stMarkdown"
)
_NAME_VALUE_TIP_SELECTOR = (
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip), '
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip), '
    ".full-results-wrap .full-results-table tbody "
    'td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip)'
)
_GENERIC_TIP_ACTIVE = (
    ".tip-wrap:not(.headlines-tip):hover, "
    ".tip-wrap:not(.headlines-tip):active, "
    ".tip-wrap:not(.headlines-tip):focus-within"
)
_NAME_TIP_CELL_SELECTOR = (
    '.full-results-wrap .full-results-table tbody td[data-label="Company"], '
    '.full-results-wrap .full-results-table tbody td[data-label="Name"], '
    '.full-results-wrap .full-results-table tbody td[data-label="Commodity"]'
)
_NAME_TIP_TEXT_LAYOUT = """
            top: 100% !important;
            bottom: auto !important;
            left: 0 !important;
            right: 0 !important;
            transform: none !important;
            width: auto !important;
            min-width: 0 !important;
            max-width: none !important;
            margin-top: 12px !important;
            box-sizing: border-box !important;
"""
_NAME_TIP_TEXT_RULES = f"""
        {_RESPONSIVE_TIP_SCOPE} {_NAME_TIP_CELL_SELECTOR} {{
            position: relative !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} {_NAME_VALUE_TIP_SELECTOR} {{
            position: static !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} {_NAME_VALUE_TIP_SELECTOR} .tip-text {{
{_NAME_TIP_TEXT_LAYOUT}
        }}
        {_RESPONSIVE_TIP_SCOPE} {_NAME_VALUE_TIP_SELECTOR} .tip-text::before {{
            top: -14px !important;
            bottom: auto !important;
        }}
        {_RESPONSIVE_TIP_SCOPE} {_NAME_VALUE_TIP_SELECTOR} .tip-text::after {{
            top: auto !important;
            bottom: 100% !important;
            left: auto !important;
            right: 0.75rem !important;
            transform: none !important;
            border-color: transparent transparent #1e1e2f transparent !important;
        }}
"""
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
{_NAME_TIP_TEXT_RULES}
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
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100003 !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active td {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100004 !important;
        }}
        .stMarkdown .full-results-wrap:has(tr.scoop-name-tip-active) {{
            overflow: visible !important;
        }}
        [data-testid="stMarkdownContainer"]:has(tr.scoop-name-tip-active) {{
            overflow: visible !important;
        }}
"""

# Inserted into page @media blocks (mobile + tablet) — beats inline "appear above" fr-val rules.
NAME_VALUE_TOOLTIP_PAGE_SNIPPET = f"""
        /* Name/Company/Commodity: tooltip below value (full card width, no horizontal clip). */
        .stMarkdown {_NAME_TIP_CELL_SELECTOR} {{
            position: relative !important;
        }}
        .stMarkdown {_NAME_VALUE_TIP_SELECTOR} {{
            position: static !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text {{
{_NAME_TIP_TEXT_LAYOUT}
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::before,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::before,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::before {{
            top: -14px !important;
            bottom: auto !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Company"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::after,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Name"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::after,
        .stMarkdown .full-results-wrap .full-results-table tbody td[data-label="Commodity"] .fr-val .tip-wrap:not(.headlines-tip) .tip-text::after {{
            top: auto !important;
            bottom: 100% !important;
            left: auto !important;
            right: 0.75rem !important;
            transform: none !important;
            border-color: transparent transparent #1e1e2f transparent !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100003 !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active td {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100004 !important;
        }}
        .stMarkdown .full-results-wrap:has(tr.scoop-name-tip-active) {{
            overflow: visible !important;
        }}
"""

NAME_VALUE_TOOLTIP_PAGE_MARKER = (
    "/* Name/Company/Commodity: tooltip below value (full card width, no horizontal clip). */"
)

RESPONSIVE_NAME_VALUE_TOOLTIP_OVERRIDE_CSS = f"""
@media (max-width: 1366px) {{
{_NAME_TIP_TEXT_RULES}
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100003 !important;
        }}
        .stMarkdown .full-results-wrap .full-results-table tbody tr.scoop-name-tip-active td {{
            overflow: visible !important;
            position: relative !important;
            z-index: 100004 !important;
        }}
        .stMarkdown .full-results-wrap:has(tr.scoop-name-tip-active) {{
            overflow: visible !important;
        }}
        [data-testid="stMarkdownContainer"]:has(tr.scoop-name-tip-active) {{
            overflow: visible !important;
        }}
}}
"""

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

# Injected early on every page (via theme_mode) so mobile/tablet overlay sidebar wins first paint.
RESPONSIVE_SIDEBAR_BOOTSTRAP = f"""
@media (max-width: 1366px) {{
{TABLET_SIDEBAR}
{OVERLAY_SIDEBAR_TOPBAR_LAYER}
}}
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
