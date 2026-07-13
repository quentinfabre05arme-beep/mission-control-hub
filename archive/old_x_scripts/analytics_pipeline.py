"""
Social Media Operations System - Analytics Pipeline
Phase 4: Analytics & Learning Workflow

Workflow: Pull Data → Process & Compare → Generate Insights → Update Memory → Optional Report
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field

sys.stdout.reconfigure(encoding='utf-8')

@dataclass
class AnalyticsSnapshot:
    """Snapshot of account metrics at a point in time"""
    timestamp: str
    followers: int
    following: int
    posts_count: int
    engagement_rate: float
    impressions: int
    profile_visits: int
    mentions: int
    top_post_id: Optional[str] = None
    top_post_engagement: float = 0.0

@dataclass
class ContentPerformance:
    """Performance metrics for a specific content piece"""
    content_id: str
    content_type: str  # thread, single, reply
    pillar: str
    posted_at: str
    likes: int
    replies: int
    reposts: int
    bookmarks: int
    impressions: int
    engagement_rate: float
    hook: str
    
@dataclass
class Insight:
    """Generated insight from analytics"""
    id: str
    category: str  # growth, engagement, content, timing
    insight: str
    confidence: float  # 0-1
    action_recommendation: str
    generated_at: str

class AnalyticsPipeline:
    """
    Analytics & Learning Pipeline
    
    Collects metrics, generates insights, updates memory
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path(__file__).parent
        self.snapshots_file = self.workspace / "operations" / "analytics_snapshots.json"
        self.performance_file = self.workspace / "operations" / "content_performance.json"
        self.insights_file = self.workspace / "operations" / "insights.json"
        self.report_file = self.workspace / "operations" / "weekly_report.md"
        
        # Ensure directories exist
        self.snapshots_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.snapshots: List[AnalyticsSnapshot] = []
        self.performance: Dict[str, ContentPerformance] = {}
        self.insights: List[Insight] = []
        
        self._load_data()
    
    def _load_data(self):
        """Load analytics data from disk"""
        if self.snapshots_file.exists():
            with open(self.snapshots_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.snapshots = [AnalyticsSnapshot(**item) for item in data]
        
        if self.performance_file.exists():
            with open(self.performance_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for content_id, perf_data in data.items():
                    self.performance[content_id] = ContentPerformance(**perf_data)
        
        if self.insights_file.exists():
            with open(self.insights_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.insights = [Insight(**item) for item in data]
    
    def _save_data(self):
        """Save analytics data to disk"""
        snapshots_data = [
            {
                "timestamp": s.timestamp,
                "followers": s.followers,
                "following": s.following,
                "posts_count": s.posts_count,
                "engagement_rate": s.engagement_rate,
                "impressions": s.impressions,
                "profile_visits": s.profile_visits,
                "mentions": s.mentions,
                "top_post_id": s.top_post_id,
                "top_post_engagement": s.top_post_engagement
            }
            for s in self.snapshots
        ]
        
        with open(self.snapshots_file, 'w', encoding='utf-8') as f:
            json.dump(snapshots_data, f, indent=2, ensure_ascii=False)
        
        performance_data = {}
        for content_id, perf in self.performance.items():
            performance_data[content_id] = {
                "content_id": perf.content_id,
                "content_type": perf.content_type,
                "pillar": perf.pillar,
                "posted_at": perf.posted_at,
                "likes": perf.likes,
                "replies": perf.replies,
                "reposts": perf.reposts,
                "bookmarks": perf.bookmarks,
                "impressions": perf.impressions,
                "engagement_rate": perf.engagement_rate,
                "hook": perf.hook
            }
        
        with open(self.performance_file, 'w', encoding='utf-8') as f:
            json.dump(performance_data, f, indent=2, ensure_ascii=False)
        
        insights_data = [
            {
                "id": i.id,
                "category": i.category,
                "insight": i.insight,
                "confidence": i.confidence,
                "action_recommendation": i.action_recommendation,
                "generated_at": i.generated_at
            }
            for i in self.insights
        ]
        
        with open(self.insights_file, 'w', encoding='utf-8') as f:
            json.dump(insights_data, f, indent=2, ensure_ascii=False)
    
    def record_snapshot(self, followers: int, following: int = None,
                       posts_count: int = None, engagement_rate: float = None,
                       impressions: int = 0, profile_visits: int = 0,
                       mentions: int = 0):
        """Record a new analytics snapshot"""
        snapshot = AnalyticsSnapshot(
            timestamp=datetime.now().isoformat(),
            followers=followers,
            following=following or 0,
            posts_count=posts_count or 0,
            engagement_rate=engagement_rate or 0.0,
            impressions=impressions,
            profile_visits=profile_visits,
            mentions=mentions
        )
        
        self.snapshots.append(snapshot)
        self._save_data()
        
        print(f"[ANALYTICS] Snapshot recorded: {followers} followers")
        return snapshot
    
    def record_content_performance(self, content_id: str, content_type: str,
                                  pillar: str, posted_at: str, hook: str,
                                  likes: int = 0, replies: int = 0,
                                  reposts: int = 0, bookmarks: int = 0,
                                  impressions: int = 0) -> ContentPerformance:
        """Record performance for a content piece"""
        total_engagement = likes + replies + reposts + bookmarks
        engagement_rate = (total_engagement / impressions * 100) if impressions > 0 else 0
        
        performance = ContentPerformance(
            content_id=content_id,
            content_type=content_type,
            pillar=pillar,
            posted_at=posted_at,
            likes=likes,
            replies=replies,
            reposts=reposts,
            bookmarks=bookmarks,
            impressions=impressions,
            engagement_rate=round(engagement_rate, 2),
            hook=hook
        )
        
        self.performance[content_id] = performance
        self._save_data()
        
        print(f"[ANALYTICS] Performance recorded: {content_id} ({engagement_rate:.2f}%)")
        return performance
    
    def calculate_growth(self, days: int = 7) -> Dict:
        """Calculate growth metrics over a period"""
        if len(self.snapshots) < 2:
            return {"error": "Not enough snapshots for growth calculation"}
        
        # Get snapshots from period
        cutoff = datetime.now() - timedelta(days=days)
        recent = [s for s in self.snapshots if datetime.fromisoformat(s.timestamp) > cutoff]
        
        if len(recent) < 2:
            return {"error": f"Not enough snapshots in last {days} days"}
        
        start = recent[0]
        end = recent[-1]
        
        followers_change = end.followers - start.followers
        followers_pct = (followers_change / start.followers * 100) if start.followers > 0 else 0
        
        return {
            "period_days": days,
            "followers_start": start.followers,
            "followers_end": end.followers,
            "followers_change": followers_change,
            "followers_change_pct": round(followers_pct, 2),
            "engagement_rate": end.engagement_rate,
            "impressions": end.impressions
        }
    
    def analyze_content_pillars(self) -> Dict:
        """Analyze performance by content pillar"""
        if not self.performance:
            return {"error": "No content performance data"}
        
        pillars = {}
        
        for perf in self.performance.values():
            if perf.pillar not in pillars:
                pillars[perf.pillar] = {
                    "count": 0,
                    "total_engagement": 0,
                    "avg_engagement_rate": 0,
                    "total_impressions": 0
                }
            
            p = pillars[perf.pillar]
            p["count"] += 1
            p["total_engagement"] += perf.likes + perf.replies + perf.reposts + perf.bookmarks
            p["total_impressions"] += perf.impressions
        
        # Calculate averages
        for pillar in pillars:
            p = pillars[pillar]
            p["avg_engagement_rate"] = round(
                (p["total_engagement"] / p["total_impressions"] * 100) if p["total_impressions"] > 0 else 0,
                2
            )
        
        # Rank by engagement rate
        ranked = sorted(pillars.items(), key=lambda x: x[1]["avg_engagement_rate"], reverse=True)
        
        return {
            "pillars": pillars,
            "ranked": ranked,
            "best_performing": ranked[0][0] if ranked else None
        }
    
    def generate_insights(self) -> List[Insight]:
        """Generate insights from analytics data"""
        new_insights = []
        
        # Growth insight
        growth = self.calculate_growth(7)
        if "error" not in growth:
            if growth["followers_change"] > 0:
                insight = Insight(
                    id=f"insight_growth_{int(datetime.now().timestamp())}",
                    category="growth",
                    insight=f"Gained {growth['followers_change']} followers in 7 days (+{growth['followers_change_pct']}%)",
                    confidence=0.8,
                    action_recommendation="Continue current posting rhythm and engagement strategy",
                    generated_at=datetime.now().isoformat()
                )
                new_insights.append(insight)
            elif growth["followers_change"] < 0:
                insight = Insight(
                    id=f"insight_growth_{int(datetime.now().timestamp())}",
                    category="growth",
                    insight=f"Lost {abs(growth['followers_change'])} followers in 7 days",
                    confidence=0.7,
                    action_recommendation="Review content strategy and engagement quality",
                    generated_at=datetime.now().isoformat()
                )
                new_insights.append(insight)
        
        # Content pillar insight
        pillar_analysis = self.analyze_content_pillars()
        if "error" not in pillar_analysis and pillar_analysis["best_performing"]:
            insight = Insight(
                id=f"insight_pillar_{int(datetime.now().timestamp())}",
                category="content",
                insight=f"'{pillar_analysis['best_performing']}' is your best performing content pillar",
                confidence=0.75,
                action_recommendation=f"Create more content around {pillar_analysis['best_performing']} theme",
                generated_at=datetime.now().isoformat()
            )
            new_insights.append(insight)
        
        # Engagement rate insight
        if len(self.snapshots) > 0:
            latest = self.snapshots[-1]
            if latest.engagement_rate >= 5:
                insight = Insight(
                    id=f"insight_eng_{int(datetime.now().timestamp())}",
                    category="engagement",
                    insight=f"Engagement rate of {latest.engagement_rate}% is above average (5%+)",
                    confidence=0.85,
                    action_recommendation="Maintain quality over quantity approach",
                    generated_at=datetime.now().isoformat()
                )
                new_insights.append(insight)
        
        self.insights.extend(new_insights)
        self._save_data()
        
        print(f"[ANALYTICS] Generated {len(new_insights)} insights")
        return new_insights
    
    def generate_weekly_report(self) -> str:
        """Generate weekly analytics report"""
        growth = self.calculate_growth(7)
        pillar_analysis = self.analyze_content_pillars()
        
        # Get top performing content
        top_content = sorted(
            self.performance.values(),
            key=lambda x: x.engagement_rate,
            reverse=True
        )[:3]
        
        report = f"""# Weekly Analytics Report
## @quentinvest1 | Week of {datetime.now().strftime('%Y-%m-%d')}

### Growth Metrics
"""
        
        if "error" not in growth:
            report += f"""- **Followers**: {growth['followers_start']} → {growth['followers_end']} ({growth['followers_change']:+,})
- **Growth Rate**: {growth['followers_change_pct']:+.2f}%
- **Target Progress**: {growth['followers_end']}/10,000 ({growth['followers_end']/100:.2f}%)

"""
        else:
            report += f"_Insufficient data for growth calculation_\n\n"
        
        report += "### Content Performance by Pillar\n\n"
        
        if "error" not in pillar_analysis:
            for pillar, stats in pillar_analysis["ranked"]:
                report += f"- **{pillar}**: {stats['avg_engagement_rate']:.2f}% avg engagement ({stats['count']} posts)\n"
        else:
            report += "_No content performance data available_\n"
        
        report += "\n### Top Performing Content\n\n"
        
        for i, content in enumerate(top_content, 1):
            report += f"{i}. **{content.pillar}** — {content.engagement_rate:.2f}% engagement\n"
            report += f"   Hook: _{content.hook[:60]}..._\n\n"
        
        report += "### Recent Insights\n\n"
        
        recent_insights = [i for i in self.insights if 
                          (datetime.now() - datetime.fromisoformat(i.generated_at)).days <= 7]
        
        if recent_insights:
            for insight in recent_insights[-5:]:  # Last 5
                report += f"- **{insight.category.upper()}**: {insight.insight}\n"
                report += f"  → Action: {insight.action_recommendation}\n\n"
        else:
            report += "_No new insights this week_\n"
        
        report += f"\n---\n*Generated: {datetime.now().isoformat()}*"
        
        # Save report
        with open(self.report_file, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"[ANALYTICS] Weekly report generated: {self.report_file}")
        return report
    
    def get_dashboard_metrics(self) -> Dict:
        """Get metrics for dashboard display"""
        if not self.snapshots:
            return {"error": "No data"}
        
        latest = self.snapshots[-1]
        growth = self.calculate_growth(7)
        
        return {
            "followers": latest.followers,
            "followers_change": growth.get("followers_change", 0),
            "engagement_rate": latest.engagement_rate,
            "impressions": latest.impressions,
            "growth_pct": growth.get("followers_change_pct", 0),
            "target_progress": (latest.followers / 10000) * 100
        }

if __name__ == "__main__":
    # Test analytics pipeline
    pipeline = AnalyticsPipeline("C:\\Users\\quent\\.openclaw\\workspace")
    
    # Record test data
    pipeline.record_snapshot(
        followers=213,
        following=310,
        posts_count=1224,
        engagement_rate=4.9,
        impressions=1500,
        profile_visits=45,
        mentions=3
    )
    
    # Record test content performance
    pipeline.record_content_performance(
        content_id="thread_eth_treasury_001",
        content_type="thread",
        pillar="ETH Treasury",
        posted_at="2026-07-09T10:00:00",
        hook="The BTC treasury playbook is proven...",
        likes=24,
        replies=8,
        reposts=12,
        bookmarks=5,
        impressions=850
    )
    
    # Generate insights
    pipeline.generate_insights()
    
    # Generate report
    report = pipeline.generate_weekly_report()
    
    print("\n" + "="*60)
    print("WEEKLY REPORT PREVIEW")
    print("="*60)
    print(report[:800] + "...")
    print("="*60)
    
    # Dashboard metrics
    metrics = pipeline.get_dashboard_metrics()
    print("\nDashboard Metrics:")
    print(f"  Followers: {metrics['followers']} ({metrics['followers_change']:+})")
    print(f"  Engagement: {metrics['engagement_rate']}%")
    print(f"  Target Progress: {metrics['target_progress']:.2f}%")
