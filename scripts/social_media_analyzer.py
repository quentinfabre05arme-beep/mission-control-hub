#!/usr/bin/env python3
"""
Social Media Analysis System

Implements research methods for X/Twitter:
- Content analysis automation
- Sentiment tracking
- Engagement pattern analysis
- Competitor monitoring
- Hashtag/trend analysis

Usage: python social_media_analyzer.py [--analyze-profile] [--track-hashtag TAG] [--competitor-analysis]
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
ANALYTICS_DIR = "operations/social_analytics"
ENGAGEMENT_CACHE = "operations/engagement_cache.json"
CONTENT_CALENDAR = "operations/content_calendar.json"

# Engagement scoring weights (based on X algorithm research)
ENGAGEMENT_WEIGHTS = {
    "reply": 13.5,
    "retweet": 2.0,
    "like": 1.0,
    "bookmark": 1.5,
    "click": 1.2,
    "profile_click": 1.0
}

# Best posting times based on engagement research
OPTIMAL_TIMES = {
    "weekday": ["09:00", "11:00", "15:00", "19:00", "21:00"],
    "weekend": ["10:00", "12:00", "16:00", "20:00"]
}


@dataclass
class PostAnalysis:
    """Analysis of a single post"""
    post_id: str
    timestamp: str
    content: str
    format: str
    
    impressions: int
    engagements: int
    replies: int
    retweets: int
    likes: int
    bookmarks: int
    
    engagement_rate: float
    weighted_score: float
    viral_coefficient: float
    
    word_count: int
    hashtags: List[str]
    mentions: List[str]
    has_media: bool
    has_link: bool
    
    sentiment: str
    sentiment_score: float


@dataclass
class ContentPillarAnalysis:
    """Analysis of content pillar performance"""
    pillar_name: str
    total_posts: int
    total_engagement: float
    avg_engagement_rate: float
    best_performing_post: Optional[str]
    best_time: str
    best_format: str
    trend: str
    recommendation: str


class EngagementCalculator:
    """Calculates engagement metrics using X algorithm weights"""
    
    def calculate_weighted_score(self, post: Dict) -> float:
        """Calculate weighted engagement score"""
        score = 0.0
        
        score += post.get('replies', 0) * ENGAGEMENT_WEIGHTS['reply']
        score += post.get('retweets', 0) * ENGAGEMENT_WEIGHTS['retweet']
        score += post.get('likes', 0) * ENGAGEMENT_WEIGHTS['like']
        score += post.get('bookmarks', 0) * ENGAGEMENT_WEIGHTS['bookmark']
        
        return round(score, 2)
    
    def calculate_engagement_rate(self, post: Dict) -> float:
        """Calculate engagement rate"""
        impressions = post.get('impressions', 1)
        engagements = post.get('engagements', 0)
        
        if impressions == 0:
            return 0.0
        
        return round((engagements / impressions) * 100, 2)
    
    def calculate_viral_coefficient(self, post: Dict) -> float:
        """Calculate viral potential"""
        weighted = self.calculate_weighted_score(post)
        impressions = post.get('impressions', 1)
        
        if impressions == 0:
            return 0.0
        
        return round(weighted / impressions * 1000, 2)


class ContentAnalyzer:
    """Analyzes content patterns and performance"""
    
    def __init__(self):
        self.engagement_calc = EngagementCalculator()
        
    def analyze_post(self, post_data: Dict) -> PostAnalysis:
        """Analyze a single post"""
        content = post_data.get('content', '')
        
        return PostAnalysis(
            post_id=post_data.get('id', 'unknown'),
            timestamp=post_data.get('timestamp', datetime.now().isoformat()),
            content=content,
            format=self._detect_format(post_data),
            impressions=post_data.get('impressions', 0),
            engagements=post_data.get('engagements', 0),
            replies=post_data.get('replies', 0),
            retweets=post_data.get('retweets', 0),
            likes=post_data.get('likes', 0),
            bookmarks=post_data.get('bookmarks', 0),
            engagement_rate=self.engagement_calc.calculate_engagement_rate(post_data),
            weighted_score=self.engagement_calc.calculate_weighted_score(post_data),
            viral_coefficient=self.engagement_calc.calculate_viral_coefficient(post_data),
            word_count=len(content.split()),
            hashtags=re.findall(r'#\w+', content),
            mentions=re.findall(r'@\w+', content),
            has_media=post_data.get('has_media', False),
            has_link='http' in content,
            sentiment=post_data.get('sentiment', 'neutral'),
            sentiment_score=post_data.get('sentiment_score', 0.5)
        )
    
    def _detect_format(self, post: Dict) -> str:
        """Detect post format"""
        if post.get('is_thread'):
            return "thread"
        elif post.get('is_reply'):
            return "reply"
        return "single"
    
    def analyze_content_patterns(self, posts: List[Dict]) -> Dict:
        """Analyze patterns across posts"""
        analyses = [self.analyze_post(p) for p in posts]
        
        if not analyses:
            return {}
        
        total_posts = len(analyses)
        total_engagement = sum(a.weighted_score for a in analyses)
        
        best_post = max(analyses, key=lambda x: x.weighted_score)
        
        format_breakdown = defaultdict(list)
        for a in analyses:
            format_breakdown[a.format].append(a.weighted_score)
        
        format_performance = {
            fmt: round(sum(scores) / len(scores), 2)
            for fmt, scores in format_breakdown.items()
        }
        
        time_performance = self._analyze_timing(analyses)
        length_analysis = self._analyze_length(analyses)
        
        return {
            "total_posts": total_posts,
            "total_engagement": round(total_engagement, 2),
            "avg_engagement_rate": round(sum(a.engagement_rate for a in analyses) / total_posts, 2),
            "best_post": {
                "id": best_post.post_id,
                "score": best_post.weighted_score,
                "format": best_post.format
            },
            "format_performance": format_performance,
            "time_performance": time_performance,
            "length_analysis": length_analysis,
            "hashtag_performance": self._analyze_hashtags(analyses)
        }
    
    def _analyze_timing(self, analyses: List[PostAnalysis]) -> Dict:
        """Analyze performance by time"""
        hour_performance = defaultdict(list)
        
        for a in analyses:
            hour = datetime.fromisoformat(a.timestamp.replace('Z', '+00:00')).hour
            hour_performance[hour].append(a.weighted_score)
        
        return {
            str(h): round(sum(s) / len(s), 2)
            for h, s in hour_performance.items()
        }
    
    def _analyze_length(self, analyses: List[PostAnalysis]) -> Dict:
        """Analyze performance by content length"""
        buckets = {
            "short": [],
            "medium": [],
            "long": []
        }
        
        for a in analyses:
            if a.word_count <= 50:
                buckets["short"].append(a.weighted_score)
            elif a.word_count <= 150:
                buckets["medium"].append(a.weighted_score)
            else:
                buckets["long"].append(a.weighted_score)
        
        return {
            bucket: round(sum(scores) / max(len(scores), 1), 2)
            for bucket, scores in buckets.items()
        }
    
    def _analyze_hashtags(self, analyses: List[PostAnalysis]) -> Dict:
        """Analyze hashtag performance"""
        hashtag_scores = defaultdict(list)
        
        for a in analyses:
            for hashtag in a.hashtags:
                hashtag_scores[hashtag.lower()].append(a.weighted_score)
        
        return {
            tag: {
                "avg_score": round(sum(scores) / len(scores), 2),
                "usage_count": len(scores)
            }
            for tag, scores in sorted(hashtag_scores.items(), 
                                   key=lambda x: sum(x[1]) / len(x[1]), 
                                   reverse=True)[:10]
        }


class CompetitorMonitor:
    """Monitors competitor activity and performance"""
    
    def __init__(self, competitors_file: str = "operations/competitors.json"):
        self.competitors_file = competitors_file
        self.competitors = self._load_competitors()
    
    def _load_competitors(self) -> Dict:
        """Load competitor list"""
        if os.path.exists(self.competitors_file):
            with open(self.competitors_file, 'r') as f:
                return json.load(f)
        return {}
    
    def analyze_competitor(self, handle: str, their_posts: List[Dict]) -> Dict:
        """Analyze a competitor's content"""
        analyzer = ContentAnalyzer()
        patterns = analyzer.analyze_content_patterns(their_posts)
        
        return {
            "handle": handle,
            "analyzed_at": datetime.now().isoformat(),
            "post_count": len(their_posts),
            "patterns": patterns,
            "content_themes": self._extract_themes(their_posts),
            "posting_frequency": self._calculate_frequency(their_posts),
            "engagement_tier": self._classify_engagement(patterns.get("total_engagement", 0))
        }
    
    def _extract_themes(self, posts: List[Dict]) -> List[str]:
        """Extract common themes from posts"""
        all_text = " ".join([p.get('content', '') for p in posts]).lower()
        
        keywords = re.findall(r'\b[a-z]{5,}\b', all_text)
        freq = defaultdict(int)
        
        for kw in keywords:
            if kw not in ['https', 'twitter', 'thread', 'about', 'their']:
                freq[kw] += 1
        
        return [k for k, v in sorted(freq.items(), key=lambda x: x[1], reverse=True)[:5]]
    
    def _calculate_frequency(self, posts: List[Dict]) -> Dict:
        """Calculate posting frequency"""
        if len(posts) < 2:
            return {"avg_per_day": 0}
        
        timestamps = sorted([p.get('timestamp', datetime.now().isoformat()) for p in posts])
        first = datetime.fromisoformat(timestamps[0].replace('Z', '+00:00'))
        last = datetime.fromisoformat(timestamps[-1].replace('Z', '+00:00'))
        
        days = max((last - first).days, 1)
        
        return {
            "avg_per_day": round(len(posts) / days, 2),
            "total_posts": len(posts),
            "date_range": f"{first.date()} to {last.date()}"
        }
    
    def _classify_engagement(self, total_engagement: float) -> str:
        """Classify engagement level"""
        if total_engagement > 10000:
            return "high"
        elif total_engagement > 1000:
            return "medium"
        return "low"


class ContentCalendarOptimizer:
    """Optimizes content calendar based on analytics"""
    
    def __init__(self):
        self.analyzer = ContentAnalyzer()
    
    def generate_optimal_schedule(self, historical_posts: List[Dict], 
                                   content_pillars: List[str]) -> List[Dict]:
        """Generate optimal posting schedule"""
        patterns = self.analyzer.analyze_content_patterns(historical_posts)
        
        schedule = []
        today = datetime.now()
        
        for i, pillar in enumerate(content_pillars):
            best_time = self._find_best_time(patterns, pillar)
            best_format = self._find_best_format(patterns)
            
            post_time = today + timedelta(days=i, hours=int(best_time.split(':')[0]) - today.hour)
            
            schedule.append({
                "date": post_time.strftime('%Y-%m-%d'),
                "time": best_time,
                "pillar": pillar,
                "format": best_format,
                "confidence": self._calculate_schedule_confidence(patterns, best_time)
            })
        
        return schedule
    
    def _find_best_time(self, patterns: Dict, pillar: str) -> str:
        """Find best posting time"""
        time_perf = patterns.get("time_performance", {})
        
        if time_perf:
            best_hour = max(time_perf.items(), key=lambda x: x[1])[0]
            return f"{best_hour}:00"
        
        return "11:00"
    
    def _find_best_format(self, patterns: Dict) -> str:
        """Find best content format"""
        format_perf = patterns.get("format_performance", {})
        
        if format_perf:
            return max(format_perf.items(), key=lambda x: x[1])[0]
        
        return "thread"
    
    def _calculate_schedule_confidence(self, patterns: Dict, time: str) -> float:
        """Calculate confidence score for schedule"""
        time_perf = patterns.get("time_performance", {})
        
        if not time_perf:
            return 0.5
        
        hour = time.split(':')[0]
        if hour in time_perf:
            return min(time_perf[hour] / 100, 1.0)
        
        return 0.6


class SocialMediaOrchestrator:
    """Orchestrates social media analysis"""
    
    def __init__(self):
        self.analyzer = ContentAnalyzer()
        self.competitor_monitor = CompetitorMonitor()
        self.calendar_optimizer = ContentCalendarOptimizer()
        
    def analyze_own_content(self, posts: List[Dict]) -> Dict:
        """Analyze own content performance"""
        print("[ANALYZE] Analyzing content performance...")
        
        patterns = self.analyzer.analyze_content_patterns(posts)
        recommendations = self._generate_recommendations(patterns)
        
        return {
            "analysis": patterns,
            "recommendations": recommendations,
            "analyzed_at": datetime.now().isoformat()
        }
    
    def _generate_recommendations(self, patterns: Dict) -> List[str]:
        """Generate optimization recommendations"""
        recommendations = []
        
        format_perf = patterns.get("format_performance", {})
        if format_perf:
            best_format = max(format_perf.items(), key=lambda x: x[1])[0]
            recommendations.append(f"Focus on {best_format} format (best performing)")
        
        time_perf = patterns.get("time_performance", {})
        if time_perf:
            best_times = sorted(time_perf.items(), key=lambda x: x[1], reverse=True)[:3]
            time_str = ", ".join([f"{t[0]}:00" for t in best_times])
            recommendations.append(f"Optimal posting times: {time_str}")
        
        length_analysis = patterns.get("length_analysis", {})
        if length_analysis:
            best_length = max(length_analysis.items(), key=lambda x: x[1])[0]
            recommendations.append(f"Optimal content length: {best_length}")
        
        hashtag_perf = patterns.get("hashtag_performance", {})
        if hashtag_perf:
            top_tags = list(hashtag_perf.keys())[:3]
            recommendations.append(f"Top performing hashtags: {', '.join(top_tags)}")
        
        return recommendations
    
    def generate_weekly_report(self, posts: List[Dict]) -> str:
        """Generate weekly performance report"""
        analysis = self.analyze_own_content(posts)
        
        report = []
        report.append("=" * 60)
        report.append("WEEKLY SOCIAL MEDIA PERFORMANCE REPORT")
        report.append("=" * 60)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        report.append("")
        
        patterns = analysis["analysis"]
        report.append("[PERFORMANCE SUMMARY]")
        report.append(f"  Total Posts: {patterns.get('total_posts', 0)}")
        report.append(f"  Total Engagement: {patterns.get('total_engagement', 0)}")
        report.append(f"  Avg Engagement Rate: {patterns.get('avg_engagement_rate', 0)}%")
        report.append("")
        
        report.append("[RECOMMENDATIONS]")
        for rec in analysis["recommendations"]:
            report.append(f"  * {rec}")
        report.append("")
        
        return "\n".join(report)
    
    def save_analytics(self, data: Dict, filename: str = None):
        """Save analytics to disk"""
        os.makedirs(ANALYTICS_DIR, exist_ok=True)
        
        if filename is None:
            filename = f"analytics_{datetime.now().strftime('%Y-%m-%d')}.json"
        
        filepath = f"{ANALYTICS_DIR}/{filename}"
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"[SAVED] Analytics saved: {filepath}")


def main():
    """Main entry point"""
    print("=" * 60)
    print("Social Media Analysis System")
    print("=" * 60)
    
    orchestrator = SocialMediaOrchestrator()
    
    # Demo with sample data
    sample_posts = [
        {
            "id": "1",
            "timestamp": (datetime.now() - timedelta(days=1)).isoformat(),
            "content": "ETH treasury plays are heating up. Bitmine now holds $1B+ in ETH. Thread on why this matters.",
            "impressions": 5000,
            "engagements": 450,
            "replies": 30,
            "retweets": 50,
            "likes": 200,
            "bookmarks": 20,
            "has_media": True
        },
        {
            "id": "2",
            "timestamp": (datetime.now() - timedelta(days=2)).isoformat(),
            "content": "HIMS just secured $400M from JPMorgan. Here's why telehealth infrastructure is the real play.",
            "impressions": 3000,
            "engagements": 180,
            "replies": 15,
            "retweets": 25,
            "likes": 90,
            "bookmarks": 10,
            "has_media": False
        }
    ]
    
    # Analyze content
    analysis = orchestrator.analyze_own_content(sample_posts)
    
    # Print report
    print("\n" + orchestrator.generate_weekly_report(sample_posts))
    
    # Save analytics
    orchestrator.save_analytics(analysis)
    
    print("\n" + "=" * 60)
    print("Analysis Complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
