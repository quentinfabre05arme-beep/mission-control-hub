#!/usr/bin/env python3
"""
Engagement Analytics & Tracking Module
Tracks post performance and optimizes future content based on X algorithm insights
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
import statistics

class EngagementAnalytics:
    """
    Tracks and analyzes X post performance
    Provides insights for content optimization
    """
    
    def __init__(self):
        self.workspace = Path("C:/Users/quent/.openclaw/workspace")
        self.analytics_dir = self.workspace / "operations" / "analytics"
        self.analytics_dir.mkdir(parents=True, exist_ok=True)
        
        self.posts_file = self.analytics_dir / "post_history.json"
        self.metrics_file = self.analytics_dir / "engagement_metrics.json"
        
        # Algorithm weights from research
        self.algorithm_weights = {
            "retweets": 20,
            "replies": 13.5,
            "profile_clicks": 12,
            "link_clicks": 11,
            "likes": 1
        }
    
    def record_post(self, post_data: Dict) -> None:
        """Record a new post to history"""
        history = self._load_history()
        
        post_record = {
            "id": post_data.get("id", f"post_{len(history) + 1}"),
            "timestamp": datetime.now().isoformat(),
            "topic": post_data.get("topic"),
            "format": post_data.get("format"),  # single, thread
            "angle_type": post_data.get("angle_type"),
            "hashtags": post_data.get("hashtags", []),
            "time_posted": post_data.get("time_posted"),
            "engagement_score_predicted": post_data.get("engagement_score", 0),
            "metrics": {
                "impressions": 0,
                "likes": 0,
                "replies": 0,
                "retweets": 0,
                "profile_clicks": 0,
                "link_clicks": 0
            },
            "weighted_score": 0,
            "status": "posted"
        }
        
        history.append(post_record)
        self._save_history(history)
        print(f"✓ Recorded post: {post_record['topic']} at {post_record['time_posted']}")
    
    def update_metrics(self, post_id: str, metrics: Dict) -> None:
        """Update metrics for a post"""
        history = self._load_history()
        
        for post in history:
            if post["id"] == post_id:
                post["metrics"].update(metrics)
                post["weighted_score"] = self._calculate_weighted_score(post["metrics"])
                post["status"] = "measured"
                break
        
        self._save_history(history)
        print(f"✓ Updated metrics for post: {post_id}")
    
    def _calculate_weighted_score(self, metrics: Dict) -> float:
        """Calculate weighted engagement score based on algorithm"""
        score = 0
        for metric_type, weight in self.algorithm_weights.items():
            value = metrics.get(metric_type, 0)
            score += value * weight
        return round(score, 2)
    
    def generate_insights(self) -> Dict:
        """Generate performance insights"""
        history = self._load_history()
        
        if not history:
            return {"message": "No posts recorded yet"}
        
        # Filter to measured posts
        measured = [p for p in history if p["status"] == "measured"]
        
        if not measured:
            return {
                "total_posts": len(history),
                "measured_posts": 0,
                "message": "Posts recorded but no metrics yet"
            }
        
        insights = {
            "total_posts": len(history),
            "measured_posts": len(measured),
            "date_range": {
                "start": measured[0]["timestamp"],
                "end": measured[-1]["timestamp"]
            },
            "performance_by_topic": {},
            "performance_by_format": {},
            "performance_by_angle": {},
            "best_performing_posts": [],
            "recommendations": []
        }
        
        # Analyze by topic
        topics = {}
        for post in measured:
            topic = post["topic"]
            if topic not in topics:
                topics[topic] = []
            topics[topic].append(post["weighted_score"])
        
        for topic, scores in topics.items():
            insights["performance_by_topic"][topic] = {
                "count": len(scores),
                "avg_score": round(statistics.mean(scores), 2),
                "max_score": max(scores),
                "min_score": min(scores)
            }
        
        # Analyze by format
        formats = {}
        for post in measured:
            fmt = post["format"]
            if fmt not in formats:
                formats[fmt] = []
            formats[fmt].append(post["weighted_score"])
        
        for fmt, scores in formats.items():
            insights["performance_by_format"][fmt] = {
                "count": len(scores),
                "avg_score": round(statistics.mean(scores), 2)
            }
        
        # Analyze by angle type
        angles = {}
        for post in measured:
            angle = post.get("angle_type", "unknown")
            if angle not in angles:
                angles[angle] = []
            angles[angle].append(post["weighted_score"])
        
        for angle, scores in angles.items():
            insights["performance_by_angle"][angle] = {
                "count": len(scores),
                "avg_score": round(statistics.mean(scores), 2)
            }
        
        # Top 3 posts
        sorted_posts = sorted(measured, key=lambda x: x["weighted_score"], reverse=True)
        insights["best_performing_posts"] = [
            {
                "id": p["id"],
                "topic": p["topic"],
                "score": p["weighted_score"],
                "format": p["format"],
                "angle": p.get("angle_type")
            }
            for p in sorted_posts[:3]
        ]
        
        # Generate recommendations
        insights["recommendations"] = self._generate_recommendations(insights)
        
        return insights
    
    def _generate_recommendations(self, insights: Dict) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        
        # Format recommendation
        by_format = insights.get("performance_by_format", {})
        if by_format:
            best_format = max(by_format.items(), key=lambda x: x[1]["avg_score"])
            recommendations.append(
                f"Use {best_format[0].upper()} format - performs {best_format[1]['avg_score']:.1f}x better"
            )
        
        # Topic recommendation
        by_topic = insights.get("performance_by_topic", {})
        if by_topic:
            best_topic = max(by_topic.items(), key=lambda x: x[1]["avg_score"])
            recommendations.append(
                f"Double down on {best_topic[0]} - your strongest topic"
            )
        
        # Angle recommendation
        by_angle = insights.get("performance_by_angle", {})
        if by_angle:
            best_angle = max(by_angle.items(), key=lambda x: x[1]["avg_score"])
            recommendations.append(
                f"{best_angle[0].replace('-', ' ').title()} angles perform best"
            )
        
        # General recommendations
        recommendations.extend([
            "Post 3-10x daily for algorithm visibility",
            "Use reply hooks to drive 13.5x weighted engagement",
            "Threads outperform single posts for complex topics",
            "Morning posting (8-10 AM) optimal for original content"
        ])
        
        return recommendations
    
    def export_report(self) -> str:
        """Export analytics report"""
        insights = self.generate_insights()
        
        report = f"""╔══════════════════════════════════════════════════════════════════════╗
║  ENGAGEMENT ANALYTICS REPORT
║  Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}
╚══════════════════════════════════════════════════════════════════════╝

SUMMARY
-------
Total Posts: {insights.get('total_posts', 0)}
Measured Posts: {insights.get('measured_posts', 0)}

"""
        
        if "performance_by_topic" in insights:
            report += "PERFORMANCE BY TOPIC\n--------------------\n"
            for topic, data in insights["performance_by_topic"].items():
                report += f"{topic}: {data['avg_score']:.1f} avg score ({data['count']} posts)\n"
            report += "\n"
        
        if "performance_by_format" in insights:
            report += "PERFORMANCE BY FORMAT\n---------------------\n"
            for fmt, data in insights["performance_by_format"].items():
                report += f"{fmt}: {data['avg_score']:.1f} avg score ({data['count']} posts)\n"
            report += "\n"
        
        if "best_performing_posts" in insights:
            report += "TOP PERFORMING POSTS\n--------------------\n"
            for i, post in enumerate(insights["best_performing_posts"], 1):
                report += f"{i}. {post['topic']} ({post['format']}) - Score: {post['score']}\n"
            report += "\n"
        
        if "recommendations" in insights:
            report += "RECOMMENDATIONS\n---------------\n"
            for rec in insights["recommendations"]:
                report += f"• {rec}\n"
            report += "\n"
        
        # Save report
        report_file = self.analytics_dir / f"report_{datetime.now().strftime('%Y%m%d')}.txt"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"✓ Report saved: {report_file}")
        return report
    
    def _load_history(self) -> List[Dict]:
        """Load post history"""
        if self.posts_file.exists():
            with open(self.posts_file, 'r') as f:
                return json.load(f)
        return []
    
    def _save_history(self, history: List[Dict]) -> None:
        """Save post history"""
        with open(self.posts_file, 'w') as f:
            json.dump(history, f, indent=2)

def main():
    """CLI for engagement analytics"""
    import sys
    
    analytics = EngagementAnalytics()
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python engagement_analytics.py record <topic> <format> <angle_type>")
        print("  python engagement_analytics.py update <post_id> <likes> <replies> <retweets>")
        print("  python engagement_analytics.py report")
        return
    
    command = sys.argv[1]
    
    if command == "record" and len(sys.argv) >= 5:
        post_data = {
            "topic": sys.argv[2],
            "format": sys.argv[3],
            "angle_type": sys.argv[4],
            "time_posted": datetime.now().strftime("%H:%M")
        }
        analytics.record_post(post_data)
    
    elif command == "update" and len(sys.argv) >= 6:
        post_id = sys.argv[2]
        metrics = {
            "likes": int(sys.argv[3]),
            "replies": int(sys.argv[4]),
            "retweets": int(sys.argv[5])
        }
        analytics.update_metrics(post_id, metrics)
    
    elif command == "report":
        report = analytics.export_report()
        print(report)
    
    elif command == "insights":
        insights = analytics.generate_insights()
        print(json.dumps(insights, indent=2))
    
    else:
        print("Unknown command")

if __name__ == "__main__":
    main()
