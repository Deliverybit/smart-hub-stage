from __future__ import annotations

from textblob import TextBlob

import streamlit as st

from app_config import ALPHAVANTAGE_CACHE_TIMEOUT, SCREENER_CACHE_VERSION


def _headlines_from_news_items(news_items: list) -> tuple[list[str], list[str]]:
    headlines = []
    urls = []
    for item in news_items[:10]:
        title = item.get("title", "")
        url = item.get("url", "")
        if not title or (not url and title.startswith("No current news found")):
            continue
        headlines.append(title)
        urls.append(url)
    return headlines, urls


def _polarity_from_headlines(headlines: list[str]) -> float:
    if not headlines:
        return 0.0
    return sum(TextBlob(headline).sentiment.polarity for headline in headlines) / len(headlines)


@st.cache_data(ttl=ALPHAVANTAGE_CACHE_TIMEOUT, show_spinner=False)
def _cached_news_items(ticker: str, _cache_version: int = SCREENER_CACHE_VERSION) -> tuple[tuple[str, str, str], ...]:
    """Fetch and cache headline payloads per ticker (matches screener refresh cadence)."""
    from market_data import MarketData

    try:
        news_items = MarketData().get_news_items(ticker)
    except Exception:
        news_items = []

    rows = []
    for item in news_items[:10]:
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
        headlines, urls = _headlines_from_news_items(news_items)
        polarity = _polarity_from_headlines(headlines)

        enriched.at[idx, "Headline Sentiment"] = round(polarity, 3)
        enriched.at[idx, "Headlines"] = len(headlines)
        enriched.at[idx, "_headline_texts"] = headlines
        enriched.at[idx, "_headline_urls"] = urls

    return enriched
