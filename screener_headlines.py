from textblob import TextBlob


def enrich_headline_sentiment(df, market_data, ticker_column: str = "_source_ticker"):
    """Fetch headlines only for displayed screener rows and update sentiment fields."""
    if df.empty:
        return df

    enriched = df.copy()
    for idx, row in enriched.iterrows():
        ticker = row.get(ticker_column) or row.get("Ticker")
        if not ticker:
            continue

        try:
            news_items = market_data.get_news_items(ticker)
        except Exception:
            news_items = []

        headlines = []
        urls = []
        for item in news_items[:10]:
            title = item.get("title", "")
            url = item.get("url", "")
            if not title or (not url and title.startswith("No current news found")):
                continue
            headlines.append(title)
            urls.append(url)

        polarity = 0.0
        if headlines:
            polarity = sum(TextBlob(headline).sentiment.polarity for headline in headlines) / len(headlines)

        enriched.at[idx, "Headline Sentiment"] = round(polarity, 3)
        enriched.at[idx, "Headlines"] = len(headlines)
        enriched.at[idx, "_headline_texts"] = headlines
        enriched.at[idx, "_headline_urls"] = urls

    return enriched
