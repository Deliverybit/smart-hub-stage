from __future__ import annotations

import pandas as pd
import requests

from app_config import get_alpha_vantage_api_key

class MarketData:
    def __init__(self):
        self.api_key = get_alpha_vantage_api_key(required=True)
        self.base_url = "https://www.alphavantage.co/query"
        self.session = requests.Session()
        self._daily_cache: dict[tuple[str, str], pd.DataFrame] = {}

    _CRYPTO_SYMBOLS = {
        "BTC", "ETH", "DOGE", "SOL", "ADA", "SHIB", "XRP", "BNB", "AVAX",
        "LINK", "TRX", "DOT", "MATIC", "LTC", "BCH", "UNI", "ATOM", "ETC",
        "XLM", "FIL", "APT", "ARB", "OP", "NEAR", "INJ", "IMX", "SAND",
        "MANA", "AXS", "ENS", "SNX", "COMP", "SUSHI", "1INCH", "BAT",
        "ZEC", "DASH", "PEPE", "BONK", "WIF",
    }

    _INDEX_SYMBOLS = {
        "^IXIC": "IXIC",
        "^NYA": "NYA",
        "^GSPC": "SPY",
        "^DJI": "DIA",
    }

    _FUTURES_SYMBOLS = {
        "CL=F": "USO",
        "BZ=F": "BNO",
        "GC=F": "GLD",
        "SI=F": "SLV",
        "PL=F": "PPLT",
        "PA=F": "PALL",
        "HG=F": "CPER",
        "NG=F": "UNG",
        "RB=F": "UGA",
        "HO=F": "UHN",
        "ZC=F": "CORN",
        "ZS=F": "SOYB",
        "ZW=F": "WEAT",
        "ZL=F": "SOYB",
        "ZM=F": "SOYB",
        "ZO=F": "DBA",
        "ZR=F": "DBA",
        "LE=F": "COW",
        "HE=F": "COW",
        "GF=F": "COW",
        "DC=F": "DBA",
        "ES=F": "SPY",
        "NQ=F": "QQQ",
        "YM=F": "DIA",
        "RTY=F": "IWM",
        "6E=F": "FXE",
        "6J=F": "FXY",
        "6B=F": "FXB",
        "6A=F": "FXA",
        "6C=F": "FXC",
        "ZB=F": "TLT",
        "ZN=F": "IEF",
        "ZF=F": "IEI",
        "ZT=F": "SHY",
        "CC=F": "NIB",
        "KC=F": "JO",
        "CT=F": "DBA",
        "SB=F": "CANE",
        "OJ=F": "DBA",
        "DX=F": "UUP",
    }

    def _format_ticker(self, ticker):
        """Normalize user input into an Alpha Vantage compatible symbol."""
        ticker = (ticker or "").strip().upper()
        if ticker in self._INDEX_SYMBOLS:
            return self._INDEX_SYMBOLS[ticker]
        if ticker in self._FUTURES_SYMBOLS:
            return self._FUTURES_SYMBOLS[ticker]
        if ticker.endswith("-USD"):
            return ticker.replace("-USD", "")
        if ticker in self._CRYPTO_SYMBOLS:
            return ticker
        if ticker.endswith("=F"):
            return ticker.replace("=F", "")
        return ticker

    def _is_crypto(self, ticker: str) -> bool:
        ticker = (ticker or "").strip().upper()
        symbol = ticker.replace("-USD", "")
        return symbol in self._CRYPTO_SYMBOLS

    def _request(self, **params) -> dict:
        try:
            response = self.session.get(
                self.base_url,
                params={**params, "apikey": self.api_key},
                timeout=20,
            )
            response.raise_for_status()
            data = response.json()
        except (requests.RequestException, ValueError):
            return {}

        if "Error Message" in data or "Information" in data or "Note" in data:
            return {}
        return data

    @staticmethod
    def _to_float(value) -> float | None:
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def _daily_history_frame(self, ticker: str, outputsize: str = "full") -> pd.DataFrame:
        symbol = self._format_ticker(ticker)
        cache_key = (symbol, outputsize)
        if cache_key in self._daily_cache:
            return self._daily_cache[cache_key].copy()

        if self._is_crypto(ticker):
            data = self._request(
                function="DIGITAL_CURRENCY_DAILY",
                symbol=symbol,
                market="USD",
            )
            series = data.get("Time Series (Digital Currency Daily)", {})
        else:
            data = self._request(
                function="TIME_SERIES_DAILY_ADJUSTED",
                symbol=symbol,
                outputsize=outputsize,
            )
            series = data.get("Time Series (Daily)", {})

        rows = []
        for date, values in series.items():
            close = self._to_float(values.get("4. close"))
            low = self._to_float(values.get("3. low"))
            high = self._to_float(values.get("2. high"))
            if close is None:
                continue
            rows.append({"date": pd.to_datetime(date), "price": close, "low": low, "high": high})

        df = pd.DataFrame(rows)
        if not df.empty:
            df = df.sort_values("date").reset_index(drop=True)

        self._daily_cache[cache_key] = df
        return df.copy()

    def get_latest_price(self, ticker):
        """Fetch the latest Alpha Vantage price for an asset."""
        symbol = self._format_ticker(ticker)
        if not self._is_crypto(ticker):
            data = self._request(function="GLOBAL_QUOTE", symbol=symbol)
            price = self._to_float(data.get("Global Quote", {}).get("05. price"))
            if price is not None:
                return price

        df = self._daily_history_frame(ticker, outputsize="compact")
        if df.empty:
            return 0.0
        return float(df["price"].iloc[-1])

    def get_price_history(self, ticker, days=30):
        """Fetch historical daily price data. Pass days='max' for all available data."""
        outputsize = "full" if days == "max" else "compact"
        df = self._daily_history_frame(ticker, outputsize=outputsize)
        if df.empty:
            return []

        if days != "max":
            try:
                df = df.tail(int(days))
            except (TypeError, ValueError):
                pass

        df["change_pct"] = df["price"].pct_change()
        history = []
        for _, row in df.iterrows():
            history.append({
                "date": row["date"].strftime("%Y-%m-%d"),
                "price": row["price"],
                "change_pct": row["change_pct"] if not pd.isna(row["change_pct"]) else 0,
            })
        return history

    def get_daily_change(self, ticker):
        """Return latest price and daily percentage change."""
        history = self.get_price_history(ticker, days=5)
        if len(history) < 2:
            return None, None
        previous = history[-2]["price"]
        latest = history[-1]["price"]
        if not previous:
            return latest, 0.0
        return latest, ((latest - previous) / previous) * 100

    def get_market_snapshot(self, ticker):
        """Return current price plus 52-week low/high values for screeners."""
        df = self._daily_history_frame(ticker, outputsize="full").tail(365)
        if df.empty:
            return None

        low_series = df["low"].dropna()
        high_series = df["high"].dropna()
        if low_series.empty or high_series.empty:
            return None

        return {
            "current_price": float(df["price"].iloc[-1]),
            "year_low": float(low_series.min()),
            "year_high": float(high_series.max()),
        }

    def get_52_week_low(self, ticker):
        """Returns the 52-week low price for the asset."""
        snapshot = self.get_market_snapshot(ticker)
        if not snapshot:
            return None
        return snapshot["year_low"]

    def get_52_week_high(self, ticker):
        """Returns the 52-week high price for the asset."""
        snapshot = self.get_market_snapshot(ticker)
        if not snapshot:
            return None
        return snapshot["year_high"]

    def get_52_week_low_high_dates(self, ticker):
        """Returns dates when the 52-week low and high occurred."""
        df = self._daily_history_frame(ticker, outputsize="full").tail(365)
        if df.empty or df["low"].dropna().empty or df["high"].dropna().empty:
            return None, None
        low_date = df.loc[df["low"].idxmin(), "date"].strftime("%b %d, %Y")
        high_date = df.loc[df["high"].idxmax(), "date"].strftime("%b %d, %Y")
        return low_date, high_date

    def get_news_headlines(self, ticker):
        """Pulls real-time headlines for the specific asset."""
        items = self.get_news_items(ticker)
        return [item["title"] for item in items]

    def get_news_items(self, ticker):
        """Pulls headline + source URL pairs for the specific asset."""
        symbol = self._format_ticker(ticker)
        is_crypto = self._is_crypto(ticker)
        params = {"function": "NEWS_SENTIMENT", "limit": 50 if is_crypto else 10}
        if is_crypto:
            params["tickers"] = f"CRYPTO:{symbol}"
        elif symbol:
            params["tickers"] = symbol

        data = self._request(**params)
        feed = data.get("feed", [])
        if is_crypto:
            expected_ticker = f"CRYPTO:{symbol}"
            news = [
                item for item in feed
                if any(
                    sentiment.get("ticker") == expected_ticker
                    for sentiment in item.get("ticker_sentiment", [])
                )
            ]
            source_priority = {
                "Cointelegraph": 0,
                "Decrypt.co": 1,
                "Benzinga": 2,
                "Motley Fool": 3,
            }
            news = sorted(
                enumerate(news),
                key=lambda pair: (
                    source_priority.get(
                        pair[1].get("source") or pair[1].get("source_domain") or "",
                        99,
                    ),
                    pair[0],
                ),
            )
            news = [item for _, item in news]
        else:
            news = feed

        headlines = []
        seen = set()
        for item in news:
            title = item.get("title", "")
            url = item.get("url", "")
            source = item.get("source") or item.get("source_domain") or ""
            if is_crypto and source:
                title = f"{source}: {title}"
            key = (title, url)
            if title and key not in seen:
                seen.add(key)
                headlines.append({
                    "title": title,
                    "url": url,
                    "source": source,
                })
            if len(headlines) >= 10:
                break

        return headlines[:10] if headlines else [{"title": f"No current news found for {symbol}", "url": ""}]