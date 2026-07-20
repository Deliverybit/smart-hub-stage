from __future__ import annotations

import streamlit as st

from app_config import ALPHAVANTAGE_CACHE_TIMEOUT, SCREENER_CACHE_VERSION
from headline_service import (
    enrich_result_row,
    fetch_news_items,
    headlines_from_news_items,
    polarity_from_headlines,
)


@st.cache_data(ttl=ALPHAVANTAGE_CACHE_TIMEOUT, show_spinner=False)
def _cached_news_items(ticker: str, _cache_version: int = SCREENER_CACHE_VERSION) -> tuple[tuple[str, str, str], ...]:
    """Fetch and cache headline payloads per ticker (matches screener refresh cadence)."""
    rows = []
    for item in fetch_news_items(ticker)[:10]:
        rows.append((
            item.get("title", ""),
            item.get("url", ""),
            item.get("source", "") or item.get("source_domain", "") or "",
        ))
    return tuple(rows)


def enrich_headline_sentiment(
    df,
    _market_data,
    ticker_column: str = "_source_ticker",
    *,
    cache_version: int = SCREENER_CACHE_VERSION,
):
    """Fetch headlines only for displayed screener rows and update sentiment fields."""

    if df.empty:
        return df

    enriched = df.copy()
    for idx, row in enriched.iterrows():
        ticker = row.get(ticker_column) or row.get("Ticker")
        if not ticker:
            continue

        cached_rows = _cached_news_items(ticker, cache_version)
        news_items = [{"title": t, "url": u, "source": s} for t, u, s in cached_rows]
        headlines, urls = headlines_from_news_items(news_items)
        polarity = polarity_from_headlines(headlines)

        enriched.at[idx, "Headline Sentiment"] = round(polarity, 3)
        enriched.at[idx, "Headlines"] = len(headlines)
        enriched.at[idx, "_headline_texts"] = headlines
        enriched.at[idx, "_headline_urls"] = urls

    return enriched
