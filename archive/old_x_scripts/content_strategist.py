#!/usr/bin/env python3
"""
Content Strategist - Diversified content for X growth
Threads, single posts, polls, carousels, replies, quotes
"""

import json
import random
from datetime import datetime
from typing import Dict, List, Optional

class ContentStrategist:
    def __init__(self):
        self.content_types = {
            "thread": {
                "frequency": 0.2,  # 20% of posts
                "best_for": ["deep_dive", "education", "thesis"],
                "engagement": "high",
                "time_investment": "high"
            },
            "single_post": {
                "frequency": 0.35,  # 35% of posts
                "best_for": ["hot_take", "data_point", "insight"],
                "engagement": "medium",
                "time_investment": "low"
            },
            "carousel": {
                "frequency": 0.15,  # 15% of posts
                "best_for": ["visual_data", "step_by_step", "list"],
                "engagement": "high",
                "time_investment": "medium"
            },
            "poll": {
                "frequency": 0.1,  # 10% of posts
                "best_for": ["engagement", "market_sentiment", "opinion"],
                "engagement": "high",
                "time_investment": "low"
            },
            "quote_post": {
                "frequency": 0.15,  # 15% of posts
                "best_for": ["commentary", "reaction", "agreement"],
                "engagement": "medium",
                "time_investment": "low"
            },
            "reply": {
                "frequency": 0.05,  # 5% (but high volume strategy)
                "best_for": ["engagement", "visibility", "networking"],
                "engagement": "high",
                "time_investment": "medium"
            }
        }
        
    def get_daily_content_mix(self) -> Dict:
        """Generate optimal content mix for the day"""
        
        today = datetime.now().strftime("%A")
        
        # Adjust based on day
        if today in ["Monday", "Tuesday", "Wednesday"]:
            # Mid-week = higher engagement days
            mix = {
                "thread": 1,
                "single_post": 2,
                "carousel": 1,
                "poll": 0,
                "quote_post": 1,
                "replies": 5
            }
        elif today in ["Thursday", "Friday"]:
            # End of week = lighter content
            mix = {
                "thread": 0,
                "single_post": 3,
                "carousel": 0,
                "poll": 1,
                "quote_post": 2,
                "replies": 8
            }
        else:  # Weekend
            # Weekend = engagement focused
            mix = {
                "thread": 0,
                "single_post": 1,
                "carousel": 0,
                "poll": 0,
                "quote_post": 1,
                "replies": 10
            }
        
        return mix
    
    def generate_content_ideas(self, topic: str, content_type: str) -> List[str]:
        """Generate content ideas for a topic and type"""
        
        templates = {
            "thread": [
                f"The {topic} story in 5 tweets:\n\n1/ [Hook]",
                f"Why {topic} matters:\n\nA thread",
                f"Everyone's talking about {topic}.\n\nHere's what they're missing:"
            ],
            "single_post": [
                f"Hot take: {topic} is the most misunderstood opportunity in 2026.",
                f"Data point: {topic} growth just crossed an inflection point.",
                f"Unpopular opinion: {topic}",
                f"The {topic} thesis in one sentence:"
            ],
            "carousel": [
                f"5 charts that explain {topic}:",
                f"The {topic} playbook (visual thread):",
                f"Before/after: {topic}"
            ],
            "poll": [
                f"Which {topic} play are you most bullish on?",
                f"Where are we in the {topic} cycle?",
                f"What's the biggest risk to {topic}?"
            ],
            "quote_post": [
                f"This is the {topic} thesis in one tweet.",
                f"Underrated take on {topic}:",
                f"The {topic} angle nobody's talking about:"
            ]
        }
        
        return templates.get(content_type, ["Content idea placeholder"])
    
    def get_posting_schedule(self) -> List[Dict]:
        """Generate optimal posting schedule"""
        
        schedule = []
        
        # Morning slot (8-10am) - Original content
        schedule.append({
            "time": "08:30",
            "type": random.choice(["thread", "single_post", "carousel"]),
            "priority": "high",
            "description": "Original content (best engagement window)"
        })
        
        # Midday slot (12-2pm) - Engagement + single posts
        schedule.append({
            "time": "12:30",
            "type": random.choice(["single_post", "quote_post"]),
            "priority": "medium",
            "description": "Quick insight or commentary"
        })
        
        # Afternoon slot (4-6pm) - Polls or visual content
        if random.random() > 0.5:
            schedule.append({
                "time": "16:30",
                "type": random.choice(["poll", "carousel", "single_post"]),
                "priority": "medium",
                "description": "Interactive or visual content"
            })
        
        # Evening slot (7-9pm) - Replies and community
        schedule.append({
            "time": "19:30",
            "type": "replies",
            "priority": "high",
            "description": "Strategic replies to targets"
        })
        
        return schedule
    
    def should_post_thread_today(self) -> bool:
        """Determine if today is a thread day"""
        today = datetime.now()
        day_of_week = today.weekday()  # 0=Monday
        
        # Post threads Mon-Wed, skip Thu-Sun
        return day_of_week <= 2
    
    def get_next_thread_topic(self) -> Optional[str]:
        """Get next thread topic from queue"""
        try:
            with open("automation_config.json", 'r') as f:
                config = json.load(f)
                ready = config.get("content", {}).get("threads_ready", [])
                return ready[0] if ready else None
        except:
            return None


def main():
    strategist = ContentStrategist()
    
    print("=== Content Strategy Report ===\n")
    
    # Daily content mix
    mix = strategist.get_daily_content_mix()
    print(f"Date: {datetime.now().strftime('%Y-%m-%d %A')}")
    print(f"\nToday's Content Mix:")
    for content_type, count in mix.items():
        if count > 0:
            print(f"  - {content_type}: {count}")
    
    # Posting schedule
    schedule = strategist.get_posting_schedule()
    print(f"\nToday's Schedule:")
    for item in schedule:
        print(f"  {item['time']} - {item['type']} ({item['priority']})")
        print(f"     {item['description']}")
    
    # Thread decision
    if strategist.should_post_thread_today():
        topic = strategist.get_next_thread_topic()
        if topic:
            print(f"\nThread Today: YES - Topic: {topic}")
        else:
            print(f"\nThread Today: YES - No topics in queue")
    else:
        print(f"\nThread Today: NO - Focus on singles and replies")
    
    # Content ideas
    print(f"\nSample Content Ideas:")
    for content_type in ["single_post", "poll", "quote_post"]:
        ideas = strategist.generate_content_ideas("ETH treasury", content_type)
        print(f"  {content_type}: {random.choice(ideas)}")


if __name__ == "__main__":
    main()
