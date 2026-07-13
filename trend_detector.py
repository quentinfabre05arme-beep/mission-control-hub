#!/usr/bin/env python3
"""
Trend Detector Module
Detects emerging trends and momentum patterns
Based on research: Social media trend detection methods
"""

import json
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter

class TrendDetector:
    """Detect trends in research and social data"""
    
    # Trend keywords based on research
    MOMENTUM_KEYWORDS = [
        "breakthrough", "revolutionary", "game-changer", "paradigm shift",
        "explosive", "skyrocketing", "surging", "exponential", "viral",
        "trending", "momentum", "accelerating", "unprecedented"
    ]
    
    INNOVATION_KEYWORDS = [
        "AI", "automation", "protocol", "infrastructure", "platform",
        "integration", "deployment", "scaling", "adoption", "mainstream"
    ]
    
    def __init__(self):
        self.trend_history = []
        self.min_mention_threshold = 2  # Minimum mentions to be considered a trend
    
    def extract_keywords(self, text):
        """Extract potential trend keywords from text"""
        # Simple keyword extraction
        words = text.lower().split()
        return [w for w in words if len(w) > 3]
    
    def calculate_momentum_score(self, mentions_current, mentions_previous=0):
        """Calculate momentum score based on mention velocity"""
        if mentions_previous == 0:
            return mentions_current * 2 if mentions_current > 0 else 0
        
        velocity = (mentions_current - mentions_previous) / mentions_previous
        return round(velocity * 10, 2)
    
    def detect_emerging_trends(self, current_data, historical_data=None):
        """Detect emerging trends from research data"""
        trends = {
            "timestamp": datetime.now().isoformat(),
            "emerging_trends": [],
            "momentum_leaders": [],
            "trending_topics": [],
            "keyword_frequency": {}
        }
        
        # Extract all text from research data
        all_text = ""
        for pillar in current_data.get("pillars", []):
            all_text += json.dumps(pillar.get("research", {})) + " "
            all_text += json.dumps(pillar.get("content", {})) + " "
        
        # Count keyword frequency
        words = self.extract_keywords(all_text)
        word_counts = Counter(words)
        
        # Identify trending keywords
        for word, count in word_counts.most_common(20):
            if count >= self.min_mention_threshold:
                trends["keyword_frequency"][word] = count
        
        # Detect momentum keywords
        for keyword in self.MOMENTUM_KEYWORDS:
            count = all_text.lower().count(keyword)
            if count > 0:
                trends["momentum_leaders"].append({
                    "keyword": keyword,
                    "mentions": count,
                    "momentum_score": self.calculate_momentum_score(count)
                })
        
        # Detect innovation keywords
        for keyword in self.INNOVATION_KEYWORDS:
            count = all_text.lower().count(keyword)
            if count >= self.min_mention_threshold:
                trends["emerging_trends"].append({
                    "trend": keyword,
                    "mentions": count,
                    "category": "innovation"
                })
        
        # Sort by mention count
        trends["momentum_leaders"].sort(key=lambda x: x["momentum_score"], reverse=True)
        trends["emerging_trends"].sort(key=lambda x: x["mentions"], reverse=True)
        
        return trends
    
    def generate_trend_report(self, trends):
        """Generate human-readable trend report"""
        lines = [
            "🔥 Trend Detection Report",
            f"Generated: {trends['timestamp']}",
            ""
        ]
        
        if trends["momentum_leaders"]:
            lines.append("Momentum Leaders:")
            for leader in trends["momentum_leaders"][:5]:
                lines.append(f"  🚀 {leader['keyword']}: {leader['mentions']} mentions (momentum: {leader['momentum_score']})")
            lines.append("")
        
        if trends["emerging_trends"]:
            lines.append("Emerging Trends:")
            for trend in trends["emerging_trends"][:10]:
                lines.append(f"  📈 {trend['trend']}: {trend['mentions']} mentions [{trend['category']}]")
            lines.append("")
        
        if trends["keyword_frequency"]:
            lines.append("Top Keywords:")
            for word, count in list(trends["keyword_frequency"].items())[:10]:
                lines.append(f"  • {word}: {count}")
        
        return "\n".join(lines)
    
    def save_trends(self, trends, output_dir="operations/trends"):
        """Save trend data to file"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        file_path = output_path / f"trends_{date_str}.json"
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(trends, f, indent=2, ensure_ascii=False)
        
        return file_path

def main():
    """Test trend detector"""
    detector = TrendDetector()
    
    # Sample data for testing
    sample_data = {
        "pillars": [
            {
                "pillar": "ETH Treasury",
                "research": {"key_data": "5.74M ETH staked, breakthrough infrastructure"},
                "content": {"angles": {"contrarian": "Not just yield, but infrastructure"}}
            }
        ]
    }
    
    trends = detector.detect_emerging_trends(sample_data)
    print(detector.generate_trend_report(trends))

if __name__ == "__main__":
    main()
