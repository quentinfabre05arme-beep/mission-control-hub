#!/usr/bin/env python3
"""
social_intelligence_engine.py
Real-Time Social Intelligence Engine
Based on 2025-2026 Social Media Research Methods

Features:
- Real-time sentiment tracking
- Trend detection with momentum/innovation scoring
- Competitor benchmarking
- Crisis detection alerts
- Network analysis for influencer identification
- Predictive viral content forecasting
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from collections import defaultdict, Counter
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Sentiment(Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"
    MIXED = "mixed"


class TrendStatus(Enum):
    EMERGING = "emerging"      # Just starting
    GROWING = "growing"        # Gaining momentum
    PEAKING = "peaking"        # At peak
    DECLINING = "declining"    # Losing steam
    STABLE = "stable"          # Consistent


class AlertLevel(Enum):
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"


@dataclass
class SentimentAnalysis:
    """Sentiment analysis result"""
    text: str
    overall_sentiment: Sentiment
    confidence: float
    sentiment_scores: Dict[str, float]
    aspects: Dict[str, Sentiment]
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "text": self.text[:100] + "..." if len(self.text) > 100 else self.text,
            "overall_sentiment": self.overall_sentiment.value,
            "confidence": round(self.confidence, 2),
            "sentiment_scores": {k: round(v, 2) for k, v in self.sentiment_scores.items()},
            "aspects": {k: v.value for k, v in self.aspects.items()},
            "analyzed_at": self.analyzed_at
        }


@dataclass
class Trend:
    """Trend detection result"""
    topic: str
    status: TrendStatus
    momentum_score: float      # 0-1, rate of growth
    innovation_score: float    # 0-1, novelty factor
    volume: int                # Mention count
    velocity: float            # Mentions per hour
    related_topics: List[str]
    key_influencers: List[str]
    first_seen: str
    last_seen: str
    
    def to_dict(self) -> Dict:
        return {
            "topic": self.topic,
            "status": self.status.value,
            "momentum_score": round(self.momentum_score, 2),
            "innovation_score": round(self.innovation_score, 2),
            "volume": self.volume,
            "velocity": round(self.velocity, 2),
            "related_topics": self.related_topics,
            "key_influencers": self.key_influencers,
            "first_seen": self.first_seen,
            "last_seen": self.last_seen
        }


@dataclass
class CrisisAlert:
    """Crisis detection alert"""
    alert_id: str
    level: AlertLevel
    topic: str
    trigger: str
    sentiment_shift: float
    volume_spike: float
    affected_accounts: List[str]
    recommended_actions: List[str]
    detected_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "alert_id": self.alert_id,
            "level": self.level.value,
            "topic": self.topic,
            "trigger": self.trigger,
            "sentiment_shift": round(self.sentiment_shift, 2),
            "volume_spike": round(self.volume_spike, 2),
            "affected_accounts": self.affected_accounts,
            "recommended_actions": self.recommended_actions,
            "detected_at": self.detected_at
        }


@dataclass
class CompetitorIntel:
    """Competitor intelligence"""
    competitor: str
    share_of_voice: float
    sentiment_distribution: Dict[str, int]
    top_content: List[Dict]
    engagement_rate: float
    follower_growth: float
    key_topics: List[str]
    analyzed_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    
    def to_dict(self) -> Dict:
        return {
            "competitor": self.competitor,
            "share_of_voice": round(self.share_of_voice, 2),
            "sentiment_distribution": self.sentiment_distribution,
            "top_content": self.top_content,
            "engagement_rate": round(self.engagement_rate, 2),
            "follower_growth": round(self.follower_growth, 2),
            "key_topics": self.key_topics,
            "analyzed_at": self.analyzed_at
        }


class SocialIntelligenceEngine:
    """
    Real-time social intelligence engine
    Implements 2025-2026 research methodologies
    """
    
    # Sentiment keywords (simplified - production would use ML models)
    POSITIVE_WORDS = {
        'excellent', 'great', 'amazing', 'love', 'best', 'fantastic', 
        'awesome', 'perfect', 'brilliant', 'outstanding', 'impressive',
        'innovative', 'game-changing', 'breakthrough', 'promising', 'bullish'
    }
    
    NEGATIVE_WORDS = {
        'terrible', 'awful', 'worst', 'hate', 'bad', 'horrible',
        'disappointing', 'failed', 'scam', 'crash', 'dump', 'bearish',
        'concerning', 'alarming', 'problem', 'issue', 'risk'
    }
    
    EMOTIONAL_INTENSIFIERS = {
        'very', 'extremely', 'incredibly', 'absolutely', 'completely',
        'totally', 'utterly', 'massively', 'hugely', 'significantly'
    }
    
    def __init__(self):
        self.sentiment_history: List[SentimentAnalysis] = []
        self.trends: Dict[str, Trend] = {}
        self.alerts: List[CrisisAlert] = []
        self.competitor_data: Dict[str, CompetitorIntel] = {}
        self.topic_mentions: Dict[str, List[datetime]] = defaultdict(list)
        self.influencer_mentions: Dict[str, int] = defaultdict(int)
        
        logger.info("SocialIntelligenceEngine initialized")
    
    def analyze_sentiment(self, text: str, 
                         context: Optional[Dict] = None) -> SentimentAnalysis:
        """
        Analyze sentiment of text
        
        Args:
            text: Text to analyze
            context: Additional context (source, author, etc.)
        
        Returns:
            SentimentAnalysis result
        """
        text_lower = text.lower()
        words = text_lower.split()
        
        # Count sentiment words
        pos_count = sum(1 for word in words if word in self.POSITIVE_WORDS)
        neg_count = sum(1 for word in words if word in self.NEGATIVE_WORDS)
        
        # Check for intensifiers
        intensifier_multiplier = 1.0
        if any(word in words for word in self.EMOTIONAL_INTENSIFIERS):
            intensifier_multiplier = 1.3
        
        # Calculate scores
        total_sentiment_words = pos_count + neg_count
        if total_sentiment_words == 0:
            sentiment = Sentiment.NEUTRAL
            confidence = 0.5
        elif pos_count > neg_count * 1.5:
            sentiment = Sentiment.POSITIVE
            confidence = min(1.0, (pos_count / total_sentiment_words) * intensifier_multiplier)
        elif neg_count > pos_count * 1.5:
            sentiment = Sentiment.NEGATIVE
            confidence = min(1.0, (neg_count / total_sentiment_words) * intensifier_multiplier)
        else:
            sentiment = Sentiment.MIXED
            confidence = 0.6
        
        # Aspect-based sentiment (simple implementation)
        aspects = {}
        # In production, this would use NER and aspect extraction
        
        result = SentimentAnalysis(
            text=text,
            overall_sentiment=sentiment,
            confidence=confidence,
            sentiment_scores={
                "positive": pos_count,
                "negative": neg_count,
                "neutral": len(words) - total_sentiment_words
            },
            aspects=aspects
        )
        
        self.sentiment_history.append(result)
        logger.info(f"Sentiment analysis: {sentiment.value} (confidence: {confidence:.2f})")
        
        return result
    
    def batch_sentiment_analysis(self, texts: List[str]) -> List[SentimentAnalysis]:
        """Analyze sentiment for multiple texts"""
        return [self.analyze_sentiment(text) for text in texts]
    
    def get_sentiment_distribution(self, 
                                   timeframe_hours: int = 24) -> Dict[str, Any]:
        """Get sentiment distribution over timeframe"""
        cutoff = datetime.utcnow() - timedelta(hours=timeframe_hours)
        recent = [s for s in self.sentiment_history 
                 if datetime.fromisoformat(s.analyzed_at) > cutoff]
        
        distribution = Counter([s.overall_sentiment.value for s in recent])
        avg_confidence = sum(s.confidence for s in recent) / len(recent) if recent else 0
        
        return {
            "timeframe_hours": timeframe_hours,
            "total_analyzed": len(recent),
            "distribution": dict(distribution),
            "average_confidence": round(avg_confidence, 2),
            "dominant_sentiment": distribution.most_common(1)[0][0] if distribution else "none"
        }
    
    def detect_trends(self, texts: List[str], 
                     min_mentions: int = 5) -> List[Trend]:
        """
        Detect emerging trends from texts
        
        Args:
            texts: List of texts to analyze
            min_mentions: Minimum mentions to qualify as trend
        
        Returns:
            List of detected trends
        """
        # Extract hashtags and keywords
        topics = defaultdict(int)
        for text in texts:
            # Extract hashtags
            hashtags = re.findall(r'#(\w+)', text.lower())
            for tag in hashtags:
                topics[tag] += 1
            
            # Extract capitalized phrases (likely topics)
            capitalized = re.findall(r'\b[A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)+\b', text)
            for phrase in capitalized:
                topics[phrase.lower()] += 1
        
        # Filter by minimum mentions
        trend_candidates = {t: c for t, c in topics.items() if c >= min_mentions}
        
        trends = []
        for topic, count in trend_candidates.items():
            # Calculate momentum (simulated - would use time-series in production)
            momentum = min(1.0, count / 100)  # Normalize
            
            # Calculate innovation (how new is this topic)
            innovation = self._calculate_innovation_score(topic)
            
            # Determine status
            if momentum > 0.8:
                status = TrendStatus.PEAKING
            elif momentum > 0.5:
                status = TrendStatus.GROWING
            elif momentum > 0.2:
                status = TrendStatus.EMERGING
            elif momentum > 0:
                status = TrendStatus.DECLINING
            else:
                status = TrendStatus.STABLE
            
            trend = Trend(
                topic=topic,
                status=status,
                momentum_score=momentum,
                innovation_score=innovation,
                volume=count,
                velocity=count / 24,  # mentions per hour (assuming 24h window)
                related_topics=self._find_related_topics(topic, topics),
                key_influencers=[],  # Would extract from mentions
                first_seen=datetime.utcnow().isoformat(),
                last_seen=datetime.utcnow().isoformat()
            )
            
            trends.append(trend)
            self.trends[topic] = trend
        
        logger.info(f"Detected {len(trends)} trends")
        return sorted(trends, key=lambda t: t.momentum_score, reverse=True)
    
    def _calculate_innovation_score(self, topic: str) -> float:
        """Calculate how innovative/novel a topic is"""
        # In production, this would compare against historical data
        # Newer topics = higher innovation score
        if topic not in self.topic_mentions:
            return 1.0  # Completely new
        
        first_mention = min(self.topic_mentions[topic])
        days_since_first = (datetime.utcnow() - first_mention).days
        
        if days_since_first < 1:
            return 0.9
        elif days_since_first < 7:
            return 0.7
        elif days_since_first < 30:
            return 0.5
        else:
            return 0.3
    
    def _find_related_topics(self, topic: str, all_topics: Dict[str, int]) -> List[str]:
        """Find topics related to given topic"""
        # Simple implementation - in production would use semantic similarity
        related = []
        for other_topic in all_topics:
            if other_topic != topic and all_topics[other_topic] > 3:
                # Check for substring match
                if topic in other_topic or other_topic in topic:
                    related.append(other_topic)
        return related[:5]
    
    def detect_crisis(self, mentions: List[Dict], 
                     account_keywords: List[str]) -> List[CrisisAlert]:
        """
        Detect potential crisis situations
        
        Args:
            mentions: List of mention dicts with text, sentiment, etc.
            account_keywords: Keywords associated with monitored account
        
        Returns:
            List of crisis alerts
        """
        alerts = []
        
        # Analyze sentiment shift
        recent_sentiments = [m.get('sentiment', Sentiment.NEUTRAL) for m in mentions]
        negative_ratio = sum(1 for s in recent_sentiments if s == Sentiment.NEGATIVE) / len(recent_sentiments) if recent_sentiments else 0
        
        # Check for volume spike
        current_volume = len(mentions)
        baseline_volume = self._get_baseline_volume()
        volume_spike = current_volume / baseline_volume if baseline_volume > 0 else 1.0
        
        # Crisis detection logic
        if negative_ratio > 0.6 and volume_spike > 2:
            # Negative sentiment spike
            alert = CrisisAlert(
                alert_id=f"crisis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                level=AlertLevel.CRITICAL,
                topic="Negative Sentiment Spike",
                trigger=f"{negative_ratio:.0%} negative sentiment with {volume_spike:.1f}x volume spike",
                sentiment_shift=negative_ratio - 0.5,  # Baseline assumption
                volume_spike=volume_spike,
                affected_accounts=account_keywords,
                recommended_actions=[
                    "Activate crisis response team",
                    "Prepare official statement",
                    "Monitor sentiment every 15 minutes",
                    "Pause scheduled content"
                ]
            )
            alerts.append(alert)
        
        elif negative_ratio > 0.4 and volume_spike > 1.5:
            alert = CrisisAlert(
                alert_id=f"warning_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
                level=AlertLevel.WARNING,
                topic="Elevated Negative Sentiment",
                trigger=f"{negative_ratio:.0%} negative sentiment with increased volume",
                sentiment_shift=negative_ratio - 0.3,
                volume_spike=volume_spike,
                affected_accounts=account_keywords,
                recommended_actions=[
                    "Monitor closely",
                    "Prepare response templates",
                    "Alert stakeholders"
                ]
            )
            alerts.append(alert)
        
        self.alerts.extend(alerts)
        return alerts
    
    def _get_baseline_volume(self) -> int:
        """Get baseline mention volume (simplified)"""
        # In production, would calculate from historical data
        return 50  # Default baseline
    
    def analyze_competitor(self, competitor: str, 
                          mentions: List[Dict]) -> CompetitorIntel:
        """
        Analyze competitor from mentions
        
        Args:
            competitor: Competitor name/handle
            mentions: Mentions of competitor
        
        Returns:
            CompetitorIntel result
        """
        # Calculate sentiment distribution
        sentiments = [self.analyze_sentiment(m.get('text', '')).overall_sentiment 
                     for m in mentions]
        sentiment_dist = Counter([s.value for s in sentiments])
        
        # Find top content
        top_content = sorted(
            mentions,
            key=lambda m: m.get('engagement', {}).get('total', 0),
            reverse=True
        )[:5]
        
        # Extract key topics
        all_text = ' '.join([m.get('text', '') for m in mentions])
        words = re.findall(r'\b\w+\b', all_text.lower())
        word_freq = Counter(words)
        key_topics = [word for word, _ in word_freq.most_common(10) 
                     if len(word) > 3 and word not in {'https', 'http', 'the', 'and', 'for'}]
        
        intel = CompetitorIntel(
            competitor=competitor,
            share_of_voice=0.0,  # Would calculate from total market mentions
            sentiment_distribution=dict(sentiment_dist),
            top_content=top_content,
            engagement_rate=0.0,  # Would calculate from interactions/followers
            follower_growth=0.0,  # Would track over time
            key_topics=key_topics
        )
        
        self.competitor_data[competitor] = intel
        return intel
    
    def identify_influencers(self, mentions: List[Dict], 
                          min_followers: int = 1000) -> List[Dict]:
        """
        Identify key influencers from mentions
        
        Args:
            mentions: List of mentions
            min_followers: Minimum follower count
        
        Returns:
            List of influencer profiles
        """
        author_counts = defaultdict(lambda: {"count": 0, "followers": 0, "engagement": 0})
        
        for mention in mentions:
            author = mention.get('author', 'unknown')
            author_counts[author]["count"] += 1
            author_counts[author]["followers"] = mention.get('author_followers', 0)
            author_counts[author]["engagement"] += mention.get('engagement', {}).get('total', 0)
        
        influencers = []
        for author, data in author_counts.items():
            if data["followers"] >= min_followers or data["count"] >= 5:
                influence_score = (
                    data["followers"] * 0.3 +
                    data["count"] * 100 +
                    data["engagement"] * 0.5
                ) / 1000
                
                influencers.append({
                    "handle": author,
                    "mention_count": data["count"],
                    "followers": data["followers"],
                    "engagement": data["engagement"],
                    "influence_score": round(influence_score, 2),
                    "tier": "micro" if data["followers"] < 10000 else 
                           "mid" if data["followers"] < 100000 else "macro"
                })
        
        return sorted(influencers, key=lambda x: x["influence_score"], reverse=True)
    
    def predict_viral_potential(self, content: str) -> Dict:
        """
        Predict viral potential of content
        
        Args:
            content: Content to analyze
        
        Returns:
            Viral potential assessment
        """
        factors = {
            "emotional_triggers": 0.0,
            "shareability": 0.0,
            "timeliness": 0.0,
            "uniqueness": 0.0,
            "visual_appeal": 0.0
        }
        
        text_lower = content.lower()
        
        # Emotional triggers
        emotional_words = ['shocking', 'breaking', 'exclusive', 'revealed', 'secret']
        factors["emotional_triggers"] = sum(1 for word in emotional_words if word in text_lower) / len(emotional_words)
        
        # Shareability
        has_question = '?' in content
        has_cta = any(term in text_lower for term in ['share', 'retweet', 'tag'])
        factors["shareability"] = (0.5 if has_question else 0) + (0.5 if has_cta else 0)
        
        # Timeliness (check for trending keywords)
        trending_keywords = set(self.trends.keys())
        content_words = set(text_lower.split())
        overlap = len(trending_keywords & content_words)
        factors["timeliness"] = min(1.0, overlap / 3)
        
        # Uniqueness (contrarian indicators)
        contrarian = ['actually', 'unpopular opinion', 'contrarian', 'the truth']
        factors["uniqueness"] = sum(0.25 for term in contrarian if term in text_lower)
        
        # Visual appeal indicators
        has_visual = any(term in text_lower for term in ['image', 'video', 'chart', 'graph'])
        factors["visual_appeal"] = 1.0 if has_visual else 0.3
        
        # Calculate overall score
        viral_score = sum(factors.values()) / len(factors)
        
        return {
            "viral_score": round(viral_score, 2),
            "factors": {k: round(v, 2) for k, v in factors.items()},
            "prediction": "high" if viral_score > 0.7 else 
                         "medium" if viral_score > 0.5 else "low",
            "confidence": round(0.6 + (viral_score * 0.3), 2)
        }
    
    def generate_research_brief(self, topic: str, 
                               timeframe: str = "24h") -> Dict:
        """Generate comprehensive research brief"""
        
        return {
            "topic": topic,
            "timeframe": timeframe,
            "generated_at": datetime.utcnow().isoformat(),
            "sentiment_overview": self.get_sentiment_distribution(),
            "top_trends": [t.to_dict() for t in list(self.trends.values())[:5]],
            "alerts": [a.to_dict() for a in self.alerts[-5:]],
            "competitors": {k: v.to_dict() for k, v in self.competitor_data.items()},
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate strategic recommendations"""
        recs = []
        
        if self.trends:
            top_trend = max(self.trends.values(), key=lambda t: t.momentum_score)
            recs.append(f"Consider content on '{top_trend.topic}' - high momentum trend")
        
        recent_sentiment = self.get_sentiment_distribution()
        if recent_sentiment.get('dominant_sentiment') == 'negative':
            recs.append("Dominant negative sentiment detected - monitor closely")
        
        return recs


# Example usage
if __name__ == "__main__":
    engine = SocialIntelligenceEngine()
    
    # Test sentiment analysis
    test_texts = [
        "This is absolutely amazing! Best product ever!",
        "Terrible experience, completely disappointed",
        "The results are promising and the team did great work",
        "Failed to deliver on promises, concerning issues"
    ]
    
    print("=" * 60)
    print("SENTIMENT ANALYSIS")
    print("=" * 60)
    for text in test_texts:
        result = engine.analyze_sentiment(text)
        print(f"\nText: {text}")
        print(f"Sentiment: {result.overall_sentiment.value} (confidence: {result.confidence:.2f})")
    
    # Test trend detection
    print("\n" + "=" * 60)
    print("TREND DETECTION")
    print("=" * 60)
    
    trend_texts = [
        "#AI is transforming everything! #ArtificialIntelligence",
        "Just read about #AI agents - game changing technology",
        "#Bitcoin hitting new highs today #Crypto",
        "The #AI revolution is here - Machine Learning advances",
        "Investing in #Bitcoin and #Crypto for the future"
    ]
    
    trends = engine.detect_trends(trend_texts, min_mentions=2)
    for trend in trends:
        print(f"\nTopic: {trend.topic}")
        print(f"Status: {trend.status.value}")
        print(f"Momentum: {trend.momentum_score:.2f}")
    
    # Test viral prediction
    print("\n" + "=" * 60)
    print("VIRAL POTENTIAL PREDICTION")
    print("=" * 60)
    
    test_content = "Here's the unpopular opinion: 90% of AI projects fail because companies skip the basics. The truth? Start small, scale smart. What's your take?"
    prediction = engine.predict_viral_potential(test_content)
    print(json.dumps(prediction, indent=2))
