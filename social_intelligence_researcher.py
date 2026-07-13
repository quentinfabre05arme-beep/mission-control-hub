#!/usr/bin/env python3
"""
Social Intelligence Researcher v1.0
Implements 2025 social media research methods
Content analysis, sentiment analysis, trend detection, network analysis
"""

import json
import re
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Set
from collections import Counter
from dataclasses import dataclass
import os

@dataclass
class ResearchFinding:
    """Structured research finding"""
    topic: str
    sentiment: str
    confidence: float
    key_insights: List[str]
    sources: List[str]
    timestamp: str

class SentimentAnalyzer:
    """Analyze sentiment of content"""
    
    def __init__(self):
        # Positive indicators
        self.positive_words = {
            'bullish', 'growth', 'innovation', 'breakthrough', 'opportunity',
            'strong', 'momentum', 'surge', 'rally', 'adoption', 'partnership',
            'expansion', 'upgrade', 'milestone', 'success', 'outperform',
            'record', 'exceeds', 'beat', 'gains', 'positive', 'optimistic'
        }
        
        # Negative indicators
        self.negative_words = {
            'bearish', 'decline', 'crash', 'risk', 'concern', 'warning',
            'weak', 'struggle', 'drop', 'fall', 'sell', 'short', 'fear',
            'uncertainty', 'downturn', 'loss', 'miss', 'underperform',
            'cut', 'reduce', 'negative', 'pessimistic', 'volatile'
        }
        
        # Neutral/factual indicators
        self.neutral_words = {
            'report', 'data', 'analysis', 'study', 'survey', 'statistics',
            'according', 'shows', 'indicates', 'suggests', 'found',
            'research', 'findings', 'metrics', 'measurement'
        }
        
    def analyze(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        pos_count = sum(1 for w in words if w in self.positive_words)
        neg_count = sum(1 for w in words if w in self.negative_words)
        neu_count = sum(1 for w in words if w in self.neutral_words)
        
        total_weighted = pos_count + neg_count + (neu_count * 0.5)
        
        if total_weighted == 0:
            return {"sentiment": "neutral", "score": 0.0, "confidence": 0.5}
        
        # Calculate sentiment score (-1 to 1)
        score = (pos_count - neg_count) / total_weighted
        
        # Determine sentiment label
        if score > 0.2:
            sentiment = "positive"
        elif score < -0.2:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        # Confidence based on word density
        confidence = min(0.95, 0.5 + (total_weighted / len(words)) * 2)
        
        return {
            "sentiment": sentiment,
            "score": round(score, 3),
            "confidence": round(confidence, 3),
            "breakdown": {
                "positive_hits": pos_count,
                "negative_hits": neg_count,
                "neutral_hits": neu_count
            }
        }

class TrendDetector:
    """Detect emerging trends in content"""
    
    def __init__(self):
        self.momentum_keywords = {
            'trending', 'viral', 'breaking', 'just announced', 'new',
            'emerging', 'rapid', 'surge', 'explosion', 'wave'
        }
        self.innovation_keywords = {
            'breakthrough', 'novel', 'first', 'pioneering', 'revolutionary',
            'cutting-edge', 'state-of-the-art', 'innovative', 'disruptive'
        }
        
    def detect(self, texts: List[str], timeframe: str = "daily") -> Dict:
        """Detect trends across multiple texts"""
        all_words = []
        bigrams = []
        momentum_mentions = 0
        innovation_mentions = 0
        
        for text in texts:
            text_lower = text.lower()
            words = re.findall(r'\b\w+\b', text_lower)
            all_words.extend(words)
            
            # Extract bigrams
            for i in range(len(words) - 1):
                bigrams.append(f"{words[i]} {words[i+1]}")
            
            # Count momentum/innovation mentions
            if any(kw in text_lower for kw in self.momentum_keywords):
                momentum_mentions += 1
            if any(kw in text_lower for kw in self.innovation_keywords):
                innovation_mentions += 1
        
        # Count frequencies
        word_freq = Counter(all_words)
        bigram_freq = Counter(bigrams)
        
        # Filter for meaningful terms (length > 3, not common stop words)
        stop_words = {'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can',
                     'had', 'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has',
                     'him', 'his', 'how', 'its', 'may', 'new', 'now', 'old', 'see',
                     'two', 'way', 'who', 'boy', 'did', 'she', 'use', 'her', 'way',
                     'many', 'oil', 'sit', 'set', 'run', 'eat', 'far', 'sea', 'eye'}
        
        filtered_words = {w: c for w, c in word_freq.items() 
                         if len(w) > 3 and w not in stop_words and c > 1}
        
        # Top terms
        top_terms = sorted(filtered_words.items(), key=lambda x: x[1], reverse=True)[:10]
        top_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)[:5]
        
        # Calculate momentum score
        momentum_score = min(1.0, (momentum_mentions / max(len(texts), 1)) * 2)
        innovation_score = min(1.0, (innovation_mentions / max(len(texts), 1)) * 2)
        
        return {
            "top_terms": top_terms,
            "top_bigrams": top_bigrams,
            "momentum_score": round(momentum_score, 3),
            "innovation_score": round(innovation_score, 3),
            "total_texts_analyzed": len(texts),
            "unique_terms": len(filtered_words),
            "trending_indicators": {
                "momentum_mentions": momentum_mentions,
                "innovation_mentions": innovation_mentions
            }
        }

class ContentAnalyzer:
    """Analyze content patterns and themes"""
    
    def __init__(self):
        self.theme_patterns = {
            "infrastructure": r"\b(infrastructure|data center|compute|GPU|server|cloud)\b",
            "adoption": r"\b(adoption|integrat|deploy|implement|rollout)\b",
            "financial": r"\b(revenue|earnings|profit|growth|valuation|market cap)\b",
            "regulatory": r"\b(regulation|SEC|compliance|policy|legal)\b",
            "technology": r"\b(algorithm|protocol|standard|MCP|A2A|API)\b",
            "market": r"\b(bull|bear|rally|correction|volatility|momentum)\b"
        }
        
    def analyze(self, texts: List[str]) -> Dict:
        """Analyze content themes and patterns"""
        theme_counts = {theme: 0 for theme in self.theme_patterns}
        content_types = {"thread": 0, "single_post": 0, "data_heavy": 0, "opinion": 0}
        
        for text in texts:
            text_lower = text.lower()
            
            # Detect themes
            for theme, pattern in self.theme_patterns.items():
                if re.search(pattern, text_lower, re.IGNORECASE):
                    theme_counts[theme] += 1
            
            # Detect content type
            if '\n\n' in text or len(text) > 280:
                content_types["thread"] += 1
            else:
                content_types["single_post"] += 1
            
            if re.search(r'\$[\d,]+|\d+%|\$[\d]+[BMK]', text):
                content_types["data_heavy"] += 1
            
            if re.search(r'\b(I think|In my opinion|Believe|View)\b', text, re.IGNORECASE):
                content_types["opinion"] += 1
        
        # Calculate theme distribution
        total = len(texts)
        theme_dist = {k: round(v/total, 3) if total > 0 else 0 
                     for k, v in theme_counts.items()}
        
        return {
            "themes": theme_dist,
            "content_types": content_types,
            "dominant_theme": max(theme_dist.items(), key=lambda x: x[1]) if theme_dist else ("none", 0),
            "analysis_timestamp": datetime.now().isoformat()
        }

class SocialIntelligenceResearcher:
    """Main orchestrator for social intelligence research"""
    
    def __init__(self):
        self.sentiment_analyzer = SentimentAnalyzer()
        self.trend_detector = TrendDetector()
        self.content_analyzer = ContentAnalyzer()
        self.research_history: List[Dict] = []
        
    def research_topic(self, topic: str, raw_texts: List[str], 
                      metadata: Dict = None) -> ResearchFinding:
        """
        Conduct comprehensive research on a topic
        
        Args:
            topic: Research topic
            raw_texts: List of text content to analyze
            metadata: Optional metadata about sources
            
        Returns:
            ResearchFinding with comprehensive analysis
        """
        if not raw_texts:
            return ResearchFinding(
                topic=topic,
                sentiment="unknown",
                confidence=0.0,
                key_insights=["No data available"],
                sources=[],
                timestamp=datetime.now().isoformat()
            )
        
        # Sentiment analysis
        sentiments = [self.sentiment_analyzer.analyze(t) for t in raw_texts]
        avg_sentiment_score = sum(s["score"] for s in sentiments) / len(sentiments)
        
        if avg_sentiment_score > 0.2:
            overall_sentiment = "positive"
        elif avg_sentiment_score < -0.2:
            overall_sentiment = "negative"
        else:
            overall_sentiment = "neutral"
        
        # Trend detection
        trends = self.trend_detector.detect(raw_texts)
        
        # Content analysis
        content_analysis = self.content_analyzer.analyze(raw_texts)
        
        # Extract key insights
        key_insights = []
        if trends["momentum_score"] > 0.5:
            key_insights.append(f"High momentum topic (score: {trends['momentum_score']})")
        if trends["innovation_score"] > 0.5:
            key_insights.append(f"Innovation activity detected (score: {trends['innovation_score']})")
        
        top_terms = [t[0] for t in trends["top_terms"][:5]]
        if top_terms:
            key_insights.append(f"Key terms: {', '.join(top_terms)}")
        
        if content_analysis["dominant_theme"][0] != "none":
            key_insights.append(f"Dominant theme: {content_analysis['dominant_theme'][0]}")
        
        # Calculate overall confidence
        confidence = sum(s["confidence"] for s in sentiments) / len(sentiments)
        
        result = ResearchFinding(
            topic=topic,
            sentiment=overall_sentiment,
            confidence=round(confidence, 3),
            key_insights=key_insights,
            sources=metadata.get("sources", []) if metadata else [],
            timestamp=datetime.now().isoformat()
        )
        
        # Store in history
        self.research_history.append({
            "finding": result,
            "trends": trends,
            "content_analysis": content_analysis
        })
        
        return result
        
    def generate_research_brief(self, finding: ResearchFinding) -> str:
        """Generate human-readable research brief"""
        lines = [
            f"# Research Brief: {finding.topic}",
            f"**Sentiment:** {finding.sentiment.upper()} (confidence: {finding.confidence})",
            f"**Timestamp:** {finding.timestamp}",
            "",
            "## Key Insights",
        ]
        
        for insight in finding.key_insights:
            lines.append(f"- {insight}")
        
        if finding.sources:
            lines.extend(["", "## Sources"])
            for source in finding.sources[:5]:
                lines.append(f"- {source}")
        
        return "\n".join(lines)

def main():
    """Example usage"""
    researcher = SocialIntelligenceResearcher()
    
    # Sample texts for analysis
    sample_texts = [
        "ETH treasury plays are gaining momentum. Bitmine now holds 5.74M ETH generating $277M annually.",
        "The infrastructure build phase is accelerating. New data centers represent $50B+ investment.",
        "HIMS stock rallied 45% on the JPMorgan $400M facility announcement.",
        "MCP protocol adoption is spreading across AI frameworks. Standardization is key.",
        "Some concerns about regulatory headwinds for crypto treasury companies.",
        "AI agent infrastructure showing strong growth signals for 2025.",
    ]
    
    # Research a topic
    finding = researcher.research_topic(
        topic="AI Infrastructure Investment",
        raw_texts=sample_texts,
        metadata={"sources": ["X Posts", "Research Briefs"]}
    )
    
    # Generate and print brief
    brief = researcher.generate_research_brief(finding)
    print(brief)
    
    # Save to file
    os.makedirs("operations/research", exist_ok=True)
    filename = f"social_intelligence_{datetime.now().strftime('%Y%m%d')}.json"
    with open(f"operations/research/{filename}", "w") as f:
        json.dump({
            "finding": finding.__dict__,
            "timestamp": datetime.now().isoformat()
        }, f, indent=2, default=str)
    
    print(f"\nResearch saved to operations/research/{filename}")

if __name__ == "__main__":
    main()
