#!/usr/bin/env python3
"""
Social Intelligence Monitor v1.0
Real-time sentiment tracking, trend detection, and social media intelligence
"""

import json
import re
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from collections import Counter, defaultdict
import math


class SocialIntelligenceMonitor:
    """
    Real-time social intelligence monitoring system.
    Tracks sentiment, trends, competitors, and emerging topics.
    """
    
    def __init__(self, config_path: str = "social_intelligence_config.json"):
        self.config = self._load_config(config_path)
        self.monitoring_data = self._load_monitoring_data()
        self.sentiment_lexicon = self._load_sentiment_lexicon()
        self.trend_history = self._load_trend_history()
        
    def _load_config(self, path: str) -> Dict:
        """Load monitor configuration."""
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return self._default_config()
    
    def _default_config(self) -> Dict:
        """Default configuration."""
        return {
            "track_keywords": [
                "AI agents", "automation", "content creation",
                "Bitcoin", "Ethereum", "crypto",
                "GLP-1", "biotech", "healthcare",
                "longevity", "HIMS", "MSTR"
            ],
            "competitors": [],
            "sentiment_threshold": 0.3,
            "trend_velocity_threshold": 1.5,
            "crisis_keywords": ["scam", "fraud", "lawsuit", "hack", "breach"],
            "monitoring_sources": ["x", "reddit", "news"],
            "alert_channels": ["console", "file"],
            "update_interval_minutes": 30
        }
    
    def _load_monitoring_data(self) -> Dict:
        """Load historical monitoring data."""
        data_path = Path("memory/social_monitoring_data.json")
        if data_path.exists():
            with open(data_path, 'r') as f:
                return json.load(f)
        return {"alerts": [], "sentiment_history": [], "trend_snapshots": []}
    
    def _load_sentiment_lexicon(self) -> Dict:
        """Load sentiment analysis lexicon."""
        return {
            "positive": [
                "bullish", "breakthrough", "growth", "moon", "pump", "win",
                "amazing", "great", "excellent", "love", "awesome", "bull",
                "innovation", "success", "surge", "rally", "gains", "profit",
                "bull run", " ATH", "all time high", "green", "upward", "boom"
            ],
            "negative": [
                "bearish", "crash", "dump", "bear", "loss", "lose", "scam",
                "terrible", "awful", "hate", "bad", "fail", "failure",
                "plunge", "tank", "drop", "collapse", "regret", "panic",
                "bear market", "correction", "red", "downward", "bust"
            ],
            "neutral_context": [
                "analysis", "report", "data", "study", "research", "announced",
                "announces", "launched", "launches", "update", "news"
            ]
        }
    
    def _load_trend_history(self) -> List[Dict]:
        """Load trend history for momentum calculation."""
        history_path = Path("memory/trend_history.json")
        if history_path.exists():
            with open(history_path, 'r') as f:
                return json.load(f)
        return []
    
    def analyze_sentiment(self, text: str, context: str = "") -> Dict[str, Any]:
        """
        Analyze sentiment of text with confidence scoring.
        """
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        positive_count = sum(1 for word in self.sentiment_lexicon["positive"] 
                            if word in text_lower)
        negative_count = sum(1 for word in self.sentiment_lexicon["negative"] 
                            if word in text_lower)
        
        # Calculate raw sentiment score (-1 to 1)
        total_sentiment_words = positive_count + negative_count
        if total_sentiment_words == 0:
            sentiment_score = 0
        else:
            sentiment_score = (positive_count - negative_count) / total_sentiment_words
        
        # Calculate confidence based on word count and sentiment words
        confidence = min(1.0, (total_sentiment_words / max(len(words) * 0.1, 5)) + 0.3)
        
        # Adjust for context
        if any(word in text_lower for word in self.sentiment_lexicon["neutral_context"]):
            confidence *= 0.8  # Reduce confidence for news/analysis content
        
        # Determine sentiment category
        if sentiment_score > 0.3:
            category = "positive"
        elif sentiment_score < -0.3:
            category = "negative"
        else:
            category = "neutral"
        
        return {
            "score": round(sentiment_score, 3),
            "category": category,
            "confidence": round(confidence, 2),
            "positive_words": positive_count,
            "negative_words": negative_count,
            "context": context
        }
    
    def detect_trends(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect emerging trends from posts.
        Returns trends with momentum and innovation scores.
        """
        if not posts:
            return []
        
        # Extract topics from posts
        topic_counts = defaultdict(int)
        topic_posts = defaultdict(list)
        
        for post in posts:
            text = post.get("text", "").lower()
            
            # Extract hashtags
            hashtags = re.findall(r'#\w+', text)
            for hashtag in hashtags:
                topic_counts[hashtag] += 1
                topic_posts[hashtag].append(post)
            
            # Extract key phrases (2-3 words)
            words = re.findall(r'\b\w+\b', text)
            for i in range(len(words) - 1):
                bigram = f"{words[i]} {words[i+1]}"
                if len(bigram) > 5:  # Filter short/bigram
                    topic_counts[bigram] += 0.5
                    topic_posts[bigram].append(post)
        
        # Calculate trend metrics
        trends = []
        current_time = datetime.now()
        
        for topic, count in topic_counts.items():
            if count < 2:  # Minimum threshold
                continue
            
            # Calculate velocity (mentions per hour)
            topic_post_times = [
                datetime.fromisoformat(p.get("timestamp", current_time.isoformat()))
                for p in topic_posts[topic]
                if p.get("timestamp")
            ]
            
            if topic_post_times:
                time_span = max(topic_post_times) - min(topic_post_times)
                hours = max(time_span.total_seconds() / 3600, 1)
                velocity = count / hours
            else:
                velocity = count
            
            # Calculate momentum vs previous period
            momentum = self._calculate_momentum(topic, velocity)
            
            # Calculate innovation score (novelty)
            innovation = self._calculate_innovation_score(topic, topic_posts[topic])
            
            # Overall trend score
            trend_score = (velocity * 0.4 + momentum * 0.35 + innovation * 0.25)
            
            trends.append({
                "topic": topic,
                "mentions": count,
                "velocity": round(velocity, 2),
                "momentum": round(momentum, 2),
                "innovation_score": round(innovation, 2),
                "trend_score": round(trend_score, 2),
                "sentiment": self._aggregate_sentiment(topic_posts[topic]),
                "sample_posts": topic_posts[topic][:3],
                "timestamp": current_time.isoformat()
            })
        
        # Sort by trend score
        trends.sort(key=lambda x: x["trend_score"], reverse=True)
        
        # Update trend history
        self._update_trend_history(trends[:10])
        
        return trends[:20]  # Return top 20 trends
    
    def analyze_content(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Comprehensive content analysis.
        """
        if not posts:
            return {}
        
        analysis = {
            "total_posts": len(posts),
            "time_range": self._get_time_range(posts),
            "content_types": self._categorize_content_types(posts),
            "top_keywords": self._extract_top_keywords(posts),
            "engagement_patterns": self._analyze_engagement_patterns(posts),
            "sentiment_distribution": self._analyze_sentiment_distribution(posts),
            "theme_clusters": self._cluster_themes(posts)
        }
        
        return analysis
    
    def detect_crisis_signals(self, posts: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Detect potential crisis signals.
        """
        alerts = []
        
        for post in posts:
            text = post.get("text", "").lower()
            
            # Check for crisis keywords
            for keyword in self.config["crisis_keywords"]:
                if keyword in text:
                    # Check sentiment
                    sentiment = self.analyze_sentiment(text, "crisis_detection")
                    
                    if sentiment["category"] == "negative" and sentiment["confidence"] > 0.5:
                        alert = {
                            "type": "crisis_signal",
                            "keyword": keyword,
                            "post": post,
                            "sentiment": sentiment,
                            "timestamp": datetime.now().isoformat(),
                            "severity": self._calculate_crisis_severity(post, sentiment)
                        }
                        alerts.append(alert)
                        break  # One alert per post
        
        return alerts
    
    def generate_research_brief(self, topic: str, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Generate research brief on a topic.
        """
        # Filter posts related to topic
        topic_posts = [
            p for p in posts 
            if topic.lower() in p.get("text", "").lower()
        ]
        
        if not topic_posts:
            return {"error": f"No posts found for topic: {topic}"}
        
        # Analyze
        sentiment_analysis = [self.analyze_sentiment(p.get("text", "")) for p in topic_posts]
        avg_sentiment = sum(s["score"] for s in sentiment_analysis) / len(sentiment_analysis)
        
        brief = {
            "topic": topic,
            "post_count": len(topic_posts),
            "sentiment_summary": {
                "average_score": round(avg_sentiment, 3),
                "distribution": {
                    "positive": sum(1 for s in sentiment_analysis if s["category"] == "positive"),
                    "neutral": sum(1 for s in sentiment_analysis if s["category"] == "neutral"),
                    "negative": sum(1 for s in sentiment_analysis if s["category"] == "negative")
                }
            },
            "key_insights": self._extract_insights(topic_posts, sentiment_analysis),
            "top_influencers": self._identify_influencers(topic_posts),
            "engagement_summary": self._summarize_engagement(topic_posts),
            "trend_direction": self._determine_trend_direction(topic_posts),
            "generated_at": datetime.now().isoformat()
        }
        
        return brief
    
    def monitor_competitors(self, competitor_data: Dict[str, List[Dict]]) -> Dict[str, Any]:
        """
        Monitor competitor activity and performance.
        """
        analysis = {}
        
        for competitor, posts in competitor_data.items():
            if not posts:
                continue
            
            analysis[competitor] = {
                "post_count": len(posts),
                "avg_engagement": sum(p.get("engagement", 0) for p in posts) / len(posts),
                "top_performing": sorted(posts, key=lambda x: x.get("engagement", 0), reverse=True)[:3],
                "content_themes": self._extract_themes(posts),
                "posting_frequency": self._calculate_posting_frequency(posts),
                "sentiment_trend": self._analyze_sentiment_trend(posts)
            }
        
        return analysis
    
    def save_state(self) -> None:
        """Save monitoring state to disk."""
        data_path = Path("memory/social_monitoring_data.json")
        data_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(data_path, 'w') as f:
            json.dump(self.monitoring_data, f, indent=2)
        
        # Save trend history
        history_path = Path("memory/trend_history.json")
        with open(history_path, 'w') as f:
            json.dump(self.trend_history, f, indent=2)
    
    # Helper methods
    
    def _calculate_momentum(self, topic: str, current_velocity: float) -> float:
        """Calculate trend momentum vs previous period."""
        if not self.trend_history:
            return 1.0
        
        # Find previous velocity for this topic
        previous_velocity = None
        for snapshot in reversed(self.trend_history):
            for trend in snapshot.get("trends", []):
                if trend.get("topic") == topic:
                    previous_velocity = trend.get("velocity", 0)
                    break
            if previous_velocity is not None:
                break
        
        if previous_velocity and previous_velocity > 0:
            return current_velocity / previous_velocity
        
        return 1.0
    
    def _calculate_innovation_score(self, topic: str, posts: List[Dict]) -> float:
        """Calculate innovation score based on content novelty."""
        # Check if topic is new (not in historical data)
        is_new_topic = True
        for snapshot in self.trend_history:
            for trend in snapshot.get("trends", []):
                if trend.get("topic") == topic:
                    is_new_topic = False
                    break
        
        if is_new_topic:
            return 0.9  # High novelty
        
        # Check content uniqueness
        unique_words = set()
        total_words = 0
        
        for post in posts:
            text = post.get("text", "").lower()
            words = re.findall(r'\b\w+\b', text)
            unique_words.update(words)
            total_words += len(words)
        
        if total_words > 0:
            uniqueness_ratio = len(unique_words) / total_words
            return min(0.9, uniqueness_ratio * 2)
        
        return 0.5
    
    def _aggregate_sentiment(self, posts: List[Dict]) -> Dict:
        """Aggregate sentiment across posts."""
        if not posts:
            return {"category": "neutral", "confidence": 0}
        
        sentiments = [self.analyze_sentiment(p.get("text", "")) for p in posts]
        
        avg_score = sum(s["score"] for s in sentiments) / len(sentiments)
        avg_confidence = sum(s["confidence"] for s in sentiments) / len(sentiments)
        
        if avg_score > 0.3:
            category = "positive"
        elif avg_score < -0.3:
            category = "negative"
        else:
            category = "neutral"
        
        return {
            "category": category,
            "average_score": round(avg_score, 3),
            "confidence": round(avg_confidence, 2)
        }
    
    def _update_trend_history(self, trends: List[Dict]) -> None:
        """Update trend history."""
        self.trend_history.append({
            "timestamp": datetime.now().isoformat(),
            "trends": trends
        })
        
        # Keep only last 100 snapshots
        if len(self.trend_history) > 100:
            self.trend_history = self.trend_history[-100:]
    
    def _get_time_range(self, posts: List[Dict]) -> Dict:
        """Get time range of posts."""
        timestamps = [p.get("timestamp") for p in posts if p.get("timestamp")]
        
        if not timestamps:
            return {}
        
        times = [datetime.fromisoformat(ts) for ts in timestamps]
        
        return {
            "earliest": min(times).isoformat(),
            "latest": max(times).isoformat(),
            "duration_hours": (max(times) - min(times)).total_seconds() / 3600
        }
    
    def _categorize_content_types(self, posts: List[Dict]) -> Dict:
        """Categorize posts by type."""
        categories = {
            "text_only": 0,
            "with_image": 0,
            "with_video": 0,
            "thread": 0,
            "reply": 0,
            "poll": 0
        }
        
        for post in posts:
            text = post.get("text", "")
            
            if post.get("is_thread"):
                categories["thread"] += 1
            elif text.startswith("@"):
                categories["reply"] += 1
            elif "poll" in text.lower():
                categories["poll"] += 1
            elif post.get("has_video"):
                categories["with_video"] += 1
            elif post.get("has_image"):
                categories["with_image"] += 1
            else:
                categories["text_only"] += 1
        
        return categories
    
    def _extract_top_keywords(self, posts: List[Dict], top_n: int = 20) -> List[Dict]:
        """Extract top keywords from posts."""
        word_counts = Counter()
        
        stop_words = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "must", "can",
            "shall", "to", "of", "in", "for", "on", "at", "by", "with",
            "from", "as", "and", "but", "or", "yet", "so", "if", "then",
            "than", "that", "this", "these", "those", "i", "you", "he",
            "she", "it", "we", "they", "them", "their", "there", "where",
            "when", "why", "how", "what", "who", "which"
        }
        
        for post in posts:
            text = post.get("text", "").lower()
            words = re.findall(r'\b\w+\b', text)
            
            for word in words:
                if len(word) > 3 and word not in stop_words:
                    word_counts[word] += 1
        
        return [
            {"word": word, "count": count}
            for word, count in word_counts.most_common(top_n)
        ]
    
    def _analyze_engagement_patterns(self, posts: List[Dict]) -> Dict:
        """Analyze engagement patterns."""
        engagements = [p.get("engagement", 0) for p in posts]
        
        if not engagements:
            return {}
        
        avg = sum(engagements) / len(engagements)
        
        return {
            "average": round(avg, 2),
            "median": round(sorted(engagements)[len(engagements)//2], 2),
            "max": max(engagements),
            "min": min(engagements),
            "total": sum(engagements)
        }
    
    def _analyze_sentiment_distribution(self, posts: List[Dict]) -> Dict:
        """Analyze sentiment distribution."""
        sentiments = [self.analyze_sentiment(p.get("text", "")) for p in posts]
        
        positive = sum(1 for s in sentiments if s["category"] == "positive")
        negative = sum(1 for s in sentiments if s["category"] == "negative")
        neutral = sum(1 for s in sentiments if s["category"] == "neutral")
        
        total = len(sentiments)
        
        return {
            "positive": {"count": positive, "percentage": round(positive/total*100, 1)},
            "negative": {"count": negative, "percentage": round(negative/total*100, 1)},
            "neutral": {"count": neutral, "percentage": round(neutral/total*100, 1)}
        }
    
    def _cluster_themes(self, posts: List[Dict]) -> List[Dict]:
        """Cluster posts into themes."""
        # Simple keyword-based clustering
        theme_keywords = {
            "AI/Technology": ["ai", "artificial intelligence", "automation", "tech", "algorithm"],
            "Crypto": ["bitcoin", "ethereum", "crypto", "btc", "eth", "blockchain", "defi"],
            "Healthcare": ["health", "medical", "biotech", "treatment", "drug", "healthcare"],
            "Business": ["business", "startup", "company", "revenue", "profit", "market"]
        }
        
        themes = defaultdict(list)
        
        for post in posts:
            text = post.get("text", "").lower()
            
            for theme, keywords in theme_keywords.items():
                if any(keyword in text for keyword in keywords):
                    themes[theme].append(post)
                    break
        
        return [
            {"theme": theme, "count": len(posts_list)}
            for theme, posts_list in themes.items()
        ]
    
    def _calculate_crisis_severity(self, post: Dict, sentiment: Dict) -> str:
        """Calculate crisis severity level."""
        engagement = post.get("engagement", 0)
        
        if engagement > 1000 and sentiment["category"] == "negative":
            return "high"
        elif engagement > 100 and sentiment["category"] == "negative":
            return "medium"
        else:
            return "low"
    
    def _extract_insights(self, posts: List[Dict], sentiments: List[Dict]) -> List[str]:
        """Extract key insights from posts."""
        insights = []
        
        # Sentiment trend
        positive_ratio = sum(1 for s in sentiments if s["category"] == "positive") / len(sentiments)
        if positive_ratio > 0.6:
            insights.append(f"Strongly positive sentiment ({round(positive_ratio*100)}% positive posts)")
        elif positive_ratio < 0.3:
            insights.append(f"Negative sentiment trend ({round((1-positive_ratio)*100)}% negative posts)")
        
        # Engagement patterns
        high_engagement = [p for p in posts if p.get("engagement", 0) > 100]
        if high_engagement:
            insights.append(f"{len(high_engagement)} posts with high engagement (>100 interactions)")
        
        return insights
    
    def _identify_influencers(self, posts: List[Dict], top_n: int = 5) -> List[Dict]:
        """Identify top influencers from posts."""
        influencers = defaultdict(lambda: {"posts": 0, "total_engagement": 0})
        
        for post in posts:
            author = post.get("author", "unknown")
            influencers[author]["posts"] += 1
            influencers[author]["total_engagement"] += post.get("engagement", 0)
        
        sorted_influencers = sorted(
            influencers.items(),
            key=lambda x: x[1]["total_engagement"],
            reverse=True
        )[:top_n]
        
        return [
            {
                "username": username,
                "posts": data["posts"],
                "total_engagement": data["total_engagement"]
            }
            for username, data in sorted_influencers
        ]
    
    def _summarize_engagement(self, posts: List[Dict]) -> Dict:
        """Summarize engagement metrics."""
        total = sum(p.get("engagement", 0) for p in posts)
        avg = total / len(posts) if posts else 0
        
        return {
            "total_engagement": total,
            "average_per_post": round(avg, 2)
        }
    
    def _determine_trend_direction(self, posts: List[Dict]) -> str:
        """Determine if trend is growing, stable, or declining."""
        # Simple time-based analysis
        timestamps = [p.get("timestamp") for p in posts if p.get("timestamp")]
        
        if len(timestamps) < 3:
            return "insufficient_data"
        
        # Would do more sophisticated time-series analysis in production
        return "stable"  # Placeholder
    
    def _extract_themes(self, posts: List[Dict]) -> List[str]:
        """Extract common themes from posts."""
        return [t["theme"] for t in self._cluster_themes(posts)]
    
    def _calculate_posting_frequency(self, posts: List[Dict]) -> Dict:
        """Calculate posting frequency."""
        timestamps = [p.get("timestamp") for p in posts if p.get("timestamp")]
        
        if len(timestamps) < 2:
            return {"posts_per_day": 0}
        
        times = [datetime.fromisoformat(ts) for ts in timestamps]
        duration = max(times) - min(times)
        days = max(duration.total_seconds() / 86400, 1)
        
        return {
            "posts_per_day": round(len(posts) / days, 2),
            "total_posts": len(posts),
            "days_tracked": round(days, 1)
        }
    
    def _analyze_sentiment_trend(self, posts: List[Dict]) -> Dict:
        """Analyze sentiment trend over time."""
        sentiments = [self.analyze_sentiment(p.get("text", "")) for p in posts]
        
        # Simple average - could do time-series in production
        avg = sum(s["score"] for s in sentiments) / len(sentiments)
        
        return {
            "average_sentiment": round(avg, 3),
            "trend": "improving" if avg > 0.2 else "declining" if avg < -0.2 else "neutral"
        }


def main():
    """Example usage of Social Intelligence Monitor."""
    monitor = SocialIntelligenceMonitor()
    
    # Example posts
    example_posts = [
        {
            "text": "Bitcoin just broke $100k! Bullish on the future of crypto! 🚀 #Bitcoin #Crypto",
            "timestamp": datetime.now().isoformat(),
            "engagement": 250,
            "has_image": True,
            "author": "crypto_trader_1"
        },
        {
            "text": "New AI breakthrough in healthcare - this could revolutionize treatment for chronic diseases. The study shows 90% improvement rates.",
            "timestamp": (datetime.now() - timedelta(hours=2)).isoformat(),
            "engagement": 500,
            "has_image": False,
            "author": "health_tech_news"
        },
        {
            "text": "Market crashing again... when will this bear market end? Lost 30% this month.",
            "timestamp": (datetime.now() - timedelta(hours=3)).isoformat(),
            "engagement": 120,
            "has_image": False,
            "author": "worried_investor"
        }
    ]
    
    # Analyze sentiment
    print("=== Sentiment Analysis ===")
    for post in example_posts:
        sentiment = monitor.analyze_sentiment(post["text"])
        print(f"Text: {post['text'][:60]}...")
        print(f"Sentiment: {sentiment['category']} (score: {sentiment['score']}, confidence: {sentiment['confidence']})")
        print()
    
    # Detect trends
    print("\n=== Trend Detection ===")
    trends = monitor.detect_trends(example_posts)
    for trend in trends[:5]:
        print(f"Topic: {trend['topic']}, Score: {trend['trend_score']}, Velocity: {trend['velocity']}")
    
    # Content analysis
    print("\n=== Content Analysis ===")
    analysis = monitor.analyze_content(example_posts)
    print(f"Total posts: {analysis['total_posts']}")
    print(f"Sentiment distribution: {analysis.get('sentiment_distribution', {})}")
    print(f"Top keywords: {[k['word'] for k in analysis.get('top_keywords', [])[:5]]}")
    
    # Crisis detection
    print("\n=== Crisis Detection ===")
    crisis_signals = monitor.detect_crisis_signals(example_posts)
    if crisis_signals:
        for alert in crisis_signals:
            print(f"Crisis alert: {alert['keyword']} - Severity: {alert['severity']}")
    else:
        print("No crisis signals detected")
    
    # Save state
    monitor.save_state()
    print("\nMonitoring state saved.")


if __name__ == "__main__":
    main()
