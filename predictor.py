import pandas as pd
from sentiment_engine import SentimentEngine
from market_data import MarketData

class Predictor:
    def __init__(self):
        self.sentiment_engine = SentimentEngine()
        self.market_data = MarketData()

    def predict(
        self,
        ticker,
        headlines,
        market_data=None,
        *,
        latest_price=None,
        price_change_pct=None,
        sentiment_score=None,
    ):
        """
        Combines sentiment and price action to generate a market signal.
        """
        md = market_data or self.market_data
        if sentiment_score is None:
            sent_result = self.sentiment_engine.analyze_headlines(ticker, headlines)
            sentiment_score = sent_result["score"]  # Scale: -1 to 1

        if latest_price is None or price_change_pct is None:
            latest_price = md.get_latest_price(ticker)
            history = md.get_price_history(ticker, days=7)
            if len(history) >= 2:
                prev_price = history[-2]["price"]
                price_change_pct = (latest_price - prev_price) / prev_price
            else:
                price_change_pct = 0

        # 3. COMBINED LOGIC (The "Brain")
        # We weight sentiment at 60% and price momentum at 40%
        combined_score = (sentiment_score * 0.6) + (price_change_pct * 0.4)
        
        # Default signals
        signal = "HOLD"
        confidence = "low"

        # BULLISH Logic
        if combined_score > 0.1:
            signal = "BUY"
            confidence = "medium"
            if combined_score > 0.4:
                signal = "STRONG BUY"
                confidence = "high"

        # BEARISH Logic
        elif combined_score < -0.1:
            signal = "SELL"
            confidence = "medium"
            if combined_score < -0.4:
                signal = "STRONG SELL"
                confidence = "high"

        # 4. SPECIAL RULES (For low-cap assets like DOGE)
        # Rule: If it's a penny asset (< $0.01), sentiment is high (>0.5), 
        # but the price is dipping (negative) -> "Potential Buy" (The Dip)
        if latest_price < 0.01 and sentiment_score > 0.5 and price_change_pct < 0:
            signal = "POTENTIAL BUY (DIP)"
            confidence = "high"

        return {
            "ticker": ticker,
            "signal": signal,
            "confidence": confidence,
            "combined_score": round(combined_score, 4),
            "sentiment_score": sentiment_score,
            "price_change_pct": round(price_change_pct * 100, 2)
        }