#!/usr/bin/env python3
"""
Enhanced Daily Digest - Includes trends, content strategy, and diversified posting
"""

import json
import sys
sys.path.insert(0, '.')

from x_automation import XAutomation
from x_trend_monitor import XTrendMonitor
from content_strategist import ContentStrategist
from datetime import datetime

class EnhancedDigest:
    def __init__(self):
        self.automation = XAutomation()
        self.trend_monitor = XTrendMonitor()
        self.strategist = ContentStrategist()
    
    def generate(self) -> str:
        """Generate comprehensive daily digest"""
        
        # Get all data sources
        trends = self.trend_monitor.get_content_recommendations()
        content_mix = self.strategist.get_daily_content_mix()
        schedule = self.strategist.get_posting_schedule()
        thread_today = self.strategist.should_post_thread_today()
        thread_topic = self.strategist.get_next_thread_topic()
        
        # Build digest
        digest = f"""=== Daily X Mission Digest ===
Date: {datetime.now().strftime('%Y-%m-%d %A')}

=== ACCOUNT STATUS ===
Followers: {self.automation.config['account']['current_followers']} / {self.automation.config['account']['target_followers']}
Progress: {(self.automation.config['account']['current_followers']/self.automation.config['account']['target_followers']*100):.1f}%

=== TREND ANALYSIS (3x Daily Monitoring) ===
Hot Topics Right Now:
"""
        
        for topic in trends['trending_topics'][:3]:
            digest += f"  - {topic['topic']} ({topic['category']}) [{topic['recommendation']}]\n"
        
        digest += f"\nRecommended Action: {trends['recommended_action']}\n"
        
        digest += """
=== TODAY'S CONTENT STRATEGY ===
"""
        
        # Content mix
        digest += "Content Mix:\n"
        for content_type, count in content_mix.items():
            if count > 0:
                digest += f"  - {content_type}: {count}\n"
        
        # Thread decision
        digest += f"\nThread Today: {'YES' if thread_today else 'NO'}"
        if thread_today and thread_topic:
            digest += f" - Topic: {thread_topic.upper()}"
        digest += "\n"
        
        # Schedule
        digest += "\nPosting Schedule:\n"
        for item in schedule:
            digest += f"  {item['time']} - {item['type'].upper()}\n"
            digest += f"    {item['description']}\n"
        
        digest += """
=== ENGAGEMENT TARGETS ===
"""
        # Tier 1 targets
        for target in self.automation.config['targets']['tier_1'][:3]:
            digest += f"  - @{target}\n"
        
        digest += """
=== CONTENT IDEAS (Based on Trends) ===
"""
        
        # Generate ideas based on hot topics
        hot_topic = trends['trending_topics'][0]['topic'] if trends['trending_topics'] else "ETH treasury"
        
        ideas_single = self.strategist.generate_content_ideas(hot_topic, "single_post")
        ideas_poll = self.strategist.generate_content_ideas(hot_topic, "poll")
        
        digest += f"Single Post:\n  {ideas_single[0]}\n\n"
        digest += f"Poll Idea:\n  {ideas_poll[0]}\n"
        
        digest += """
=== QUICK ACTIONS ===
Commands you can use:
  - "post single on [topic]" - Create single post
  - "post poll on [topic]" - Create poll
  - "post thread" - Post next thread (if today is thread day)
  - "show trends" - Get fresh trend analysis
  - "draft replies" - Get strategic reply drafts
  - "update followers [count]" - Update follower count

=== NOTES ===
• 3x daily trend monitoring: 9am, 1pm, 7pm
• Threads: Mon-Wed only (not every day)
• Focus: Singles, polls, replies, carousels for variety
• Engagement > Broadcast (build relationships first)
"""
        
        return digest


def main():
    digest_generator = EnhancedDigest()
    print(digest_generator.generate())


if __name__ == "__main__":
    main()
