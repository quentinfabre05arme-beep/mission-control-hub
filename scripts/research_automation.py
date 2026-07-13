#!/usr/bin/env python3
"""
Research Automation System

Implements research methods from social media research best practices:
- Content analysis
- Sentiment analysis
- Trend detection
- Data extraction and storage

Usage: python research_automation.py [--topic TOPIC] [--analyze-sentiment] [--monitor]
"""

import os
import json
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from collections import defaultdict
import re

# Configuration
RESEARCH_DB_DIR = "operations/research_db"
TREND_CACHE_FILE = "operations/trends_cache.json"
COMPETITORS_FILE = "operations/competitors.json"

# Research topics aligned with content pillars
RESEARCH_TOPICS = {
    "eth_treasury": {
        "keywords": ["ethereum treasury", "eth treasury", "bitmine", "semler scientific", 
                     "corporate eth", "eth staking yield"],
        "sources": ["coindesk", "cointelegraph", "decrypt", "the block"],
        "sentiment_keywords": ["bullish", "bearish", "accumulation", "institutional"]
    },
    "hims_healthcare": {
        "keywords": ["hims", "hims & hers", "glip-1", "telehealth", "healthcare infrastructure"],
        "sources": ["fierce healthcare", "mobi health news", "healthcare dive"],
        "sentiment_keywords": ["growth", "expansion", "regulatory", "earnings"]
    },
    "ai_commerce": {
        "keywords": ["ai agents", "agentic commerce", "mcp protocol", "a2a protocol", 
                     "autonomous commerce"],
        "sources": ["techcrunch", "the information", "a16z", "mcKinsey"],
        "sentiment_keywords": ["adoption", "infrastructure", "enterprise", "growth"]
    }
}


@dataclass
class ResearchResult:
    """Structured research result"""
    topic: str
    query: str
    timestamp: str
    findings: List[Dict]
    sentiment: Dict[str, int]
    key_entities: List[str]
    sources: List[str]
    confidence: float


@dataclass
class TrendReport:
    """Trend analysis report"""
    topic: str
    date_range: Tuple[str, str]
    trend_direction: str
    momentum_score: float
    key_narratives: List[str]
    emerging_keywords: List[str]
    volume_change: float
    recommendation: str


class ContentAnalyzer:
    """Content Analysis Agent"""
    
    def __init__(self):
        self.categories = defaultdict(list)
        
    def analyze_text(self, text: str, source: str = "") -> Dict:
        """Analyze text content"""
        analysis = {
            "word_count": len(text.split()),
            "sentence_count": len(re.split(r'[.!?]+', text)),
            "hashtags": re.findall(r'#\w+', text),
            "mentions": re.findall(r'@\w+', text),
            "urls": re.findall(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text),
            "keywords_found": [],
            "sentiment_indicators": self._extract_sentiment_words(text)
        }
        
        return analysis
    
    def categorize_content(self, items: List[str], categories: List[str]) -> Dict[str, List[str]]:
        """Categorize content items"""
        categorized = {cat: [] for cat in categories}
        
        for item in items:
            for category in categories:
                if any(keyword in item.lower() for keyword in category.split()):
                    categorized[category].append(item)
                    break
        
        return categorized
    
    def _extract_sentiment_words(self, text: str) -> Dict[str, List[str]]:
        """Extract sentiment-indicating words"""
        positive = ['bullish', 'growth', 'surge', 'breakout', 'rally', 'moon', 'pump']
        negative = ['bearish', 'crash', 'dump', 'collapse', 'fear', 'panic', 'sell']
        
        text_lower = text.lower()
        return {
            "positive": [w for w in positive if w in text_lower],
            "negative": [w for w in negative if w in text_lower]
        }


class SentimentAnalyzer:
    """Sentiment Analysis Agent"""
    
    def __init__(self):
        self.sentiment_lexicon = {
            "positive": [
                "bullish", "growth", "surge", "rally", "moon", " ATH", "breakout",
                "strong", "solid", "confident", "optimistic", "promising", "opportunity"
            ],
            "negative": [
                "bearish", "crash", "dump", "collapse", "fear", "panic", "sell",
                "weak", "concerning", "worrying", "risky", "dangerous", "avoid"
            ],
            "neutral": [
                "analysis", "data", "report", "update", "announced", "stated",
                "according", "shows", "indicates"
            ]
        }
    
    def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        
        pos_count = sum(1 for word in self.sentiment_lexicon["positive"] if word in text_lower)
        neg_count = sum(1 for word in self.sentiment_lexicon["negative"] if word in text_lower)
        neu_count = sum(1 for word in self.sentiment_lexicon["neutral"] if word in text_lower)
        
        total = pos_count + neg_count + neu_count
        if total == 0:
            return {"sentiment": "neutral", "score": 0.5, "confidence": 0.3}
        
        pos_ratio = pos_count / total
        neg_ratio = neg_count / total
        
        if pos_ratio > neg_ratio and pos_ratio > 0.4:
            sentiment = "positive"
            score = 0.5 + (pos_ratio * 0.5)
        elif neg_ratio > pos_ratio and neg_ratio > 0.4:
            sentiment = "negative"
            score = 0.5 - (neg_ratio * 0.5)
        else:
            sentiment = "neutral"
            score = 0.5
        
        confidence = min(total / 5, 1.0)
        
        return {
            "sentiment": sentiment,
            "score": round(score, 2),
            "confidence": round(confidence, 2),
            "breakdown": {
                "positive_indicators": pos_count,
                "negative_indicators": neg_count,
                "neutral_indicators": neu_count
            }
        }
    
    def track_sentiment_shift(self, current: Dict, historical: List[Dict]) -> Dict:
        """Track sentiment shifts over time"""
        if not historical:
            return {"shift": "new", "trend": "insufficient_data"}
        
        avg_score = sum(h["score"] for h in historical) / len(historical)
        current_score = current["score"]
        
        diff = current_score - avg_score
        
        if diff > 0.2:
            shift = "significantly_more_positive"
        elif diff > 0.1:
            shift = "more_positive"
        elif diff < -0.2:
            shift = "significantly_more_negative"
        elif diff < -0.1:
            shift = "more_negative"
        else:
            shift = "stable"
        
        return {
            "shift": shift,
            "score_change": round(diff, 2),
            "current_vs_avg": round(current_score - avg_score, 2),
            "trend": "improving" if diff > 0.1 else "declining" if diff < -0.1 else "stable"
        }


class TrendDetector:
    """Trend Detection Agent"""
    
    def __init__(self):
        self.trend_history = self._load_trend_cache()
    
    def _load_trend_cache(self) -> Dict:
        """Load cached trend data"""
        if os.path.exists(TREND_CACHE_FILE):
            try:
                with open(TREND_CACHE_FILE, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}
    
    def detect_trends(self, topic: str, new_data: List[Dict]) -> TrendReport:
        """Detect trends for a topic"""
        today = datetime.now()
        week_ago = today - timedelta(days=7)
        
        current_volume = len(new_data)
        historical_volume = self.trend_history.get(topic, {}).get('avg_volume', current_volume)
        
        volume_change = ((current_volume - historical_volume) / max(historical_volume, 1)) * 100
        
        all_text = " ".join([d.get('text', '') for d in new_data])
        narratives = self._extract_narratives(all_text)
        
        momentum = min(abs(volume_change) * 2, 100)
        
        direction = "rising" if volume_change > 20 else "falling" if volume_change < -20 else "stable"
        
        report = TrendReport(
            topic=topic,
            date_range=(week_ago.strftime('%Y-%m-%d'), today.strftime('%Y-%m-%d')),
            trend_direction=direction,
            momentum_score=momentum,
            key_narratives=narratives[:5],
            emerging_keywords=self._extract_emerging_keywords(all_text),
            volume_change=round(volume_change, 1),
            recommendation=self._generate_recommendation(direction, momentum, narratives)
        )
        
        self._update_trend_cache(topic, current_volume)
        
        return report
    
    def _extract_narratives(self, text: str) -> List[str]:
        """Extract key narratives from text"""
        narratives = []
        
        narrative_patterns = [
            r"(\w+\s+is\s+\w+)",
            r"(\w+\s+could\s+\w+)",
            r"(\w+\s+will\s+\w+)",
        ]
        
        for pattern in narrative_patterns:
            matches = re.findall(pattern, text.lower())
            narratives.extend(matches[:3])
        
        return list(set(narratives))
    
    def _extract_emerging_keywords(self, text: str) -> List[str]:
        """Extract emerging keywords"""
        words = re.findall(r'\b[a-zA-Z]{4,}\b', text.lower())
        word_freq = defaultdict(int)
        
        for word in words:
            if word not in ['this', 'that', 'with', 'from', 'have', 'been']:
                word_freq[word] += 1
        
        sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)
        return [word for word, freq in sorted_words[:5]]
    
    def _generate_recommendation(self, direction: str, momentum: float, 
                                  narratives: List[str]) -> str:
        """Generate trend-based recommendation"""
        if direction == "rising" and momentum > 60:
            return "Strong momentum - create content immediately"
        elif direction == "rising":
            return "Growing interest - monitor for peak timing"
        elif direction == "falling":
            return "Declining interest - consider contrarian angle"
        else:
            return "Stable - focus on quality over timing"
    
    def _update_trend_cache(self, topic: str, volume: int):
        """Update trend cache"""
        if topic not in self.trend_history:
            self.trend_history[topic] = {"volumes": [], "avg_volume": volume}
        
        self.trend_history[topic]["volumes"].append(volume)
        if len(self.trend_history[topic]["volumes"]) > 10:
            self.trend_history[topic]["volumes"] = self.trend_history[topic]["volumes"][-10:]
        
        self.trend_history[topic]["avg_volume"] = sum(self.trend_history[topic]["volumes"]) / len(self.trend_history[topic]["volumes"])
        
        os.makedirs(os.path.dirname(TREND_CACHE_FILE), exist_ok=True)
        with open(TREND_CACHE_FILE, 'w') as f:
            json.dump(self.trend_history, f, indent=2)


class ResearchOrchestrator:
    """Orchestrates research automation"""
    
    def __init__(self):
        self.content_analyzer = ContentAnalyzer()
        self.sentiment_analyzer = SentimentAnalyzer()
        self.trend_detector = TrendDetector()
        
    def conduct_research(self, topic_key: str, search_results: List[Dict] = None) -> Dict:
        """Conduct full research on a topic"""
        topic_config = RESEARCH_TOPICS.get(topic_key)
        if not topic_config:
            return {"error": f"Unknown topic: {topic_key}"}
        
        print(f"[RESEARCH] Researching: {topic_key}")
        
        if search_results is None:
            search_results = self._simulate_search(topic_config)
        
        print("  |-- Content analysis...")
        content_analysis = [self.content_analyzer.analyze_text(r.get('text', '')) for r in search_results]
        
        print("  |-- Sentiment analysis...")
        sentiments = [self.sentiment_analyzer.analyze_sentiment(r.get('text', '')) for r in search_results]
        avg_sentiment = {
            "average_score": round(sum(s["score"] for s in sentiments) / len(sentiments), 2),
            "dominant": max(set([s["sentiment"] for s in sentiments]), key=lambda x: sum(1 for s in sentiments if s["sentiment"] == x)),
            "confidence": round(sum(s["confidence"] for s in sentiments) / len(sentiments), 2)
        }
        
        print("  |-- Trend detection...")
        trend_report = self.trend_detector.detect_trends(topic_key, search_results)
        
        result = {
            "topic": topic_key,
            "timestamp": datetime.now().isoformat(),
            "config": topic_config,
            "sentiment": avg_sentiment,
            "trend": {
                "direction": trend_report.trend_direction,
                "momentum": trend_report.momentum_score,
                "volume_change": trend_report.volume_change,
                "narratives": trend_report.key_narratives,
                "keywords": trend_report.emerging_keywords
            },
            "recommendation": trend_report.recommendation,
            "content_metrics": {
                "total_items": len(search_results),
                "avg_word_count": sum(c["word_count"] for c in content_analysis) / max(len(content_analysis), 1),
                "total_hashtags": sum(len(c["hashtags"]) for c in content_analysis)
            }
        }
        
        return result
    
    def _simulate_search(self, topic_config: Dict) -> List[Dict]:
        """Simulate search results"""
        return [
            {"text": f"Recent development in {topic_config['keywords'][0]} showing positive momentum"},
            {"text": f"Analysis of {topic_config['keywords'][1]} reveals growth opportunities"},
            {"text": f"Market update: {topic_config['keywords'][2]} gaining traction"}
        ]
    
    def save_research(self, results: Dict, date: str = None):
        """Save research results"""
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        
        os.makedirs(RESEARCH_DB_DIR, exist_ok=True)
        
        filename = f"{RESEARCH_DB_DIR}/research_{results['topic']}_{date}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"  `-- Saved: {filename}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("Research Automation System")
    print("=" * 60)
    
    orchestrator = ResearchOrchestrator()
    
    all_results = {}
    for topic_key in RESEARCH_TOPICS.keys():
        result = orchestrator.conduct_research(topic_key)
        orchestrator.save_research(result)
        all_results[topic_key] = result
    
    print("\n" + "=" * 60)
    print("Research Summary")
    print("=" * 60)
    
    for topic, result in all_results.items():
        print(f"\n{topic.upper()}:")
        print(f"  Sentiment: {result['sentiment']['dominant']} ({result['sentiment']['average_score']})")
        print(f"  Trend: {result['trend']['direction']} ({result['trend']['momentum']:.0f}/100)")
        print(f"  Volume Delta: {result['trend']['volume_change']:+.1f}%")
        print(f"  -> {result['recommendation']}")
    
    print("\n" + "=" * 60)


if __name__ == "__main__":
    main()
