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
            padding-left: 1.1rem !important;
            padding-right: 1.1rem !important;
            padding-bottom: 2.5rem !important;
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

# Shared mobile card layout for screener Full Results + Top Picks + tooltips/headlines.
TABLET_SCREENER_MOBILE_LAYOUT = (
    """
        .stApp { overflow-x: hidden !important; }
"""
    + TABLET_TYPE
    + """
        .tip-wrap .tip-text {
            position: fixed !important;
            left: auto !important;
            right: 0 !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: none !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            min-width: 0 !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }

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
            margin-left: -0.5rem !important;
            margin-right: -0.5rem !important;
            width: calc(100% + 1rem) !important;
            max-width: 100vw !important;
            box-sizing: border-box !important;
            padding: 0 0.2rem max(1rem, env(safe-area-inset-bottom)) !important;
            overflow-x: visible !important;
            overflow-y: visible !important;
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

        .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            position: absolute !important;
            left: 0 !important;
            right: auto !important;
            top: auto !important;
            bottom: calc(100% + 1.25rem) !important;
            width: min(22rem, calc(100vw - 2rem)) !important;
            min-width: 0 !important;
            max-width: min(22rem, calc(100vw - 2rem)) !important;
            max-height: min(72vh, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            transform: none !important;
            margin: 0 !important;
            box-sizing: border-box !important;
            word-break: break-word !important;
            overflow-wrap: anywhere !important;
            text-align: left !important;
            z-index: 100001 !important;
            pointer-events: none !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 0.95rem 1.05rem !important;
        }
        .stMarkdown .full-results-wrap .full-results-table tbody td .fr-val .tip-wrap:not(.headlines-tip) .tip-text {
            left: auto !important;
            right: 0 !important;
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
        .stMarkdown .tip-wrap:not(.headlines-tip):active .tip-text {
            visibility: visible !important;
            opacity: 1 !important;
        }
        html.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text,
        body.scoop-tooltip-scrolling .stMarkdown .tip-wrap:not(.headlines-tip) .tip-text {
            visibility: hidden !important;
            opacity: 0 !important;
            pointer-events: none !important;
        }
        .stMarkdown .tip-wrap .tip-text::before,
        .stMarkdown .tip-wrap .tip-text::after {
            display: none !important;
        }
"""
)

TABLET_SIDEBAR = """
        :root {
            --scoop-sidebar-width: clamp(16rem, 42vw, 28rem);
            --footer-sidebar-width: 0px;
        }

        .stApp {
            overflow-x: hidden !important;
        }

        /* Main content uses full viewport width (sidebar overlays when open). */
        [data-testid="stAppViewContainer"] {
            margin-left: 0 !important;
            padding-left: 0 !important;
            width: 100% !important;
            max-width: 100vw !important;
        }
        [data-testid="stAppViewContainer"] > section.main,
        [data-testid="stMainBlockContainer"],
        section.main > div {
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
            max-width: min(92vw, 28rem) !important;
            overflow-x: hidden !important;
            overflow-y: auto !important;
            -webkit-overflow-scrolling: touch !important;
            box-shadow: 4px 0 28px rgba(15, 23, 42, 0.22) !important;
            transform: translateX(-105%) !important;
            transition: transform 0.28s ease !important;
            pointer-events: none !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] {
            transform: translateX(0) !important;
            pointer-events: auto !important;
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
        [data-testid="stSidebarCollapseButton"],
        [data-testid="stExpandSidebarButton"],
        [data-testid="collapsedControl"] {
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            z-index: 1000006 !important;
            visibility: visible !important;
            opacity: 1 !important;
            pointer-events: auto !important;
        }
        [data-testid="stHeader"] [data-testid="stExpandSidebarButton"] {
            display: flex !important;
            color: #31333f !important;
            border: 1px solid #cbd5e1 !important;
            border-radius: 0.5rem !important;
            background: #ffffff !important;
            box-shadow: 0 1px 6px rgba(15, 23, 42, 0.12) !important;
        }
        [data-testid="stSidebarCollapseButton"] button,
        [data-testid="stExpandSidebarButton"],
        [data-testid="stExpandSidebarButton"] button,
        [data-testid="collapsedControl"] button {
            min-width: 2.75rem !important;
            min-height: 2.75rem !important;
            color: #31333f !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarHeader"] {
            position: relative !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] {
            position: absolute !important;
            top: 0.35rem !important;
            right: 0.35rem !important;
            left: auto !important;
            z-index: 1000007 !important;
            background: rgba(255, 255, 255, 0.95) !important;
            border-radius: 0.5rem !important;
            box-shadow: 0 2px 10px rgba(15, 23, 42, 0.18) !important;
        }
        section[data-testid="stSidebar"][aria-expanded="true"] [data-testid="stSidebarCollapseButton"] button {
            color: #31333f !important;
        }
        .scoop-responsive-sidebar-close {
            position: fixed !important;
            z-index: 10000010 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            width: 2.85rem !important;
            height: 2.85rem !important;
            padding: 0 !important;
            margin: 0 !important;
            border: 1px solid #94a3b8 !important;
            border-radius: 0.55rem !important;
            background: #ffffff !important;
            color: #0f172a !important;
            font-size: 1.45rem !important;
            font-weight: 800 !important;
            line-height: 1 !important;
            box-shadow: 0 3px 14px rgba(15, 23, 42, 0.24) !important;
            cursor: pointer !important;
            pointer-events: auto !important;
            touch-action: manipulation !important;
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
            margin: 0.15rem -1rem 1.1rem -1rem !important;
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

        [data-testid="stMainBlockContainer"],
        section.main > div {
            padding-top: calc(0.75rem + env(safe-area-inset-top, 0px) + 1.5rem) !important;
        }

        [data-testid="stVerticalBlock"] { gap: 0.85rem !important; }
        h1, h2, h3, h4 { margin-top: 0.4rem !important; margin-bottom: 0.5rem !important; }

        [data-testid="stHorizontalBlock"] { flex-wrap: wrap !important; }
        [data-testid="stHorizontalBlock"] > div {
            flex: 1 1 100% !important;
            min-width: 100% !important;
        }

        .tip-wrap .tip-text {
            position: fixed !important;
            left: 50% !important;
            right: auto !important;
            top: 20vh !important;
            bottom: auto !important;
            transform: translateX(-50%) !important;
            width: min(34rem, 92vw) !important;
            max-width: 92vw !important;
            margin: 0 !important;
            font-size: clamp(1rem, 2.2vw, 1.2rem) !important;
            line-height: 1.55 !important;
            padding: 1rem 1.15rem !important;
        }
"""
)

TABLET_TERMS_MOBILE_LAYOUT = TABLET_TYPE
