from textblob import TextBlob
import time

class SentimentEngine:
    def __init__(self):
        # We can define custom "weight" for financial words if needed later
        pass

    def analyze_headlines(self, ticker, headlines):
        """Analyzes a list of headlines and returns an aggregated sentiment report."""
        if not headlines or "No current news" in headlines[0]:
            return {"score": 0.0, "label": "neutral", "total": 0, "headline_scores": []}

        total_polarity = 0
        total_subjectivity = 0
        headline_scores = []

        for hl in headlines:
            blob = TextBlob(hl)
            pol = blob.sentiment.polarity
            subj = blob.sentiment.subjectivity
            
            # Simple Financial Logic: 
            # If headlines mention 'surge', 'buy', 'record', boost polarity slightly.
            # If 'crash', 'drop', 'recall', lower it.
            if any(word in hl.lower() for word in ['surge', 'rally', 'record', 'breakout']):
                pol += 0.1
            elif any(word in hl.lower() for word in ['crash', 'drop', 'slump', 'recall']):
                pol -= 0.1
            
            # Clamp polarity between -1 and 1
            pol = max(min(pol, 1.0), -1.0)
            
            total_polarity += pol
            total_subjectivity += subj
            headline_scores.append((hl, round(pol, 2)))

        avg_polarity = total_polarity / len(headlines)
        
        # Labeling based on your previous logic
        if avg_polarity > 0.05:
            label = "bullish"
        elif avg_polarity < -0.05:
            label = "bearish"
        else:
            label = "neutral"

        return {
            "score": round(avg_polarity, 4),
            "label": label,
            "total": len(headlines),
            "headline_scores": headline_scores
        }