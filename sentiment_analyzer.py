#!/usr/bin/env python3
"""
Sentiment Analyzer Module
Analyzes content sentiment for research findings
Based on research: Social media sentiment analysis best practices
"""

import json
from datetime import datetime
from pathlib import Path

class SentimentAnalyzer:
    """Analyze sentiment of research and content"""
    
    # Sentiment keywords based on research findings
    POSITIVE_INDICATORS = [
        "growth", "surge", "rally", "bullish", "breakthrough", "innovation",
        "momentum", "adoption", "partnership", "expansion", "strong",
        "outperform", "exceed", "boost", "accelerate", "rise", "gain"
    ]
    
    NEGATIVE_INDICATORS = [
        "decline", "fall", "bearish", "concern", "risk", "volatility",
        "uncertainty", "drop", "decrease", "slowdown", "underperform",
        "miss", "challenge", "headwind", "pressure", "weak"
    ]
    
    NEUTRAL_INDICATORS = [
        "report", "announce", "update", "maintain", "steady", "flat",
        "neutral", "hold", "monitor", "track", "observe"
    ]
    
    def __init__(self):
        self.results_cache = {}
    
    def analyze_text(self, text):
        """Basic sentiment analysis using keyword matching"""
        text_lower = text.lower()
        
        positive_count = sum(1 for word in self.POSITIVE_INDICATORS if word in text_lower)
        negative_count = sum(1 for word in self.NEGATIVE_INDICATORS if word in text_lower)
        neutral_count = sum(1 for word in self.NEUTRAL_INDICATORS if word in text_lower)
        
        total = positive_count + negative_count + neutral_count
        if total == 0:
            return {"sentiment": "neutral", "confidence": 0.5, "score": 0}
        
        # Calculate sentiment score (-1 to 1)
        score = (positive_count - negative_count) / total
        
        # Determine sentiment category
        if score > 0.2:
            sentiment = "positive"
        elif score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Calculate confidence based on signal strength
        confidence = min(abs(score) + 0.3, 1.0)
        
        return {
            "sentiment": sentiment,
            "confidence": round(confidence, 2),
            "score": round(score, 2),
            "counts": {
                "positive": positive_count,
                "negative": negative_count,
                "neutral": neutral_count
            }
        }
    
    def analyze_research_data(self, research_file):
        """Analyze sentiment of research data file"""
        with open(research_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        analysis = {
            "timestamp": datetime.now().isoformat(),
            "file": str(research_file),
            "pillars": []
        }
        
        for pillar_data in data.get("pillars", []):
            pillar_name = pillar_data.get("pillar", "")
            research_text = json.dumps(pillar_data.get("research", {}))
            
            sentiment = self.analyze_text(research_text)
            
            analysis["pillars"].append({
                "pillar": pillar_name,
                "sentiment": sentiment
            })
        
        # Calculate overall sentiment
        sentiments = [p["sentiment"]["sentiment"] for p in analysis["pillars"]]
        if sentiments:
            positive_ratio = sentiments.count("positive") / len(sentiments)
            negative_ratio = sentiments.count("negative") / len(sentiments)
            
            if positive_ratio > 0.5:
                overall = "positive"
            elif negative_ratio > 0.5:
                overall = "negative"
            else:
                overall = "neutral"
            
            analysis["overall_sentiment"] = overall
            analysis["sentiment_distribution"] = {
                "positive": positive_ratio,
                "neutral": sentiments.count("neutral") / len(sentiments),
                "negative": negative_ratio
            }
        
        return analysis
    
    def save_analysis(self, analysis, output_dir="operations/sentiment"):
        """Save sentiment analysis to file"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / f"sentiment_analysis_{date_str}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(analysis, f, indent=2, ensure_ascii=False)
        
        return file_path
    
    def generate_sentiment_brief(self, analysis):
        """Generate human-readable sentiment brief"""
        lines = [
            "🎭 Daily Sentiment Analysis",
            f"Generated: {analysis['timestamp']}",
            "",
            f"Overall Market Sentiment: {analysis.get('overall_sentiment', 'neutral').upper()}",
            "",
            "Per-Pillar Breakdown:"
        ]
        
        for pillar in analysis.get("pillars", []):
            name = pillar["pillar"]
            sentiment = pillar["sentiment"]["sentiment"]
            confidence = pillar["sentiment"]["confidence"]
            emoji = {"positive": "📈", "negative": "📉", "neutral": "➡️"}.get(sentiment, "➡️")
            lines.append(f"  {emoji} {name}: {sentiment} (confidence: {confidence})")
        
        if "sentiment_distribution" in analysis:
            dist = analysis["sentiment_distribution"]
            lines.extend([
                "",
                "Sentiment Distribution:",
                f"  📈 Positive: {dist['positive']:.0%}",
                f"  ➡️ Neutral: {dist['neutral']:.0%}",
                f"  📉 Negative: {dist['negative']:.0%}"
            ])
        
        return "\n".join(lines)

def main():
    """Test sentiment analyzer"""
    analyzer = SentimentAnalyzer()
    
    # Test with sample text
    sample_text = "Strong growth momentum with new partnerships driving adoption"
    result = analyzer.analyze_text(sample_text)
    print(f"Test text: {sample_text}")
    print(f"Sentiment: {result['sentiment']} (confidence: {result['confidence']})")

if __name__ == "__main__":
    main()
