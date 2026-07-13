#!/usr/bin/env python3
"""
X Automation Tool - Custom lightweight automation for @quentinvest1
No API costs, no external dependencies beyond Python standard library + requests
"""

import json
import os
import sys
import time
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class XAutomation:
    """Main automation class for X account management"""
    
    def __init__(self, config_path: str = "automation_config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.data_dir = "automation_data"
        os.makedirs(self.data_dir, exist_ok=True)
        
    def _load_config(self) -> Dict:
        """Load or create configuration"""
        default_config = {
            "account": {
                "handle": "@quentinvest1",
                "target_followers": 10000,
                "current_followers": 212
            },
            "content": {
                "posting_times": ["08:00", "12:00", "16:00"],
                "engagement_times": ["09:00", "13:00", "19:00"],
                "threads_ready": ["hims", "ai_commerce"]
            },
            "targets": {
                "tier_1": ["TheLongInvestor", "DrTomsLens", "DylanLeClair_", "RaoulGMI"],
                "tier_2": [],
                "tier_3": []
            },
            "automation": {
                "daily_digest_enabled": True,
                "auto_content_enabled": False,
                "metrics_tracking_enabled": True
            }
        }
        
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return {**default_config, **json.load(f)}
        
        with open(self.config_path, 'w') as f:
            json.dump(default_config, f, indent=2)
        return default_config
    
    def save_config(self):
        """Save current configuration"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_daily_tasks(self) -> Dict:
        """Generate daily task list"""
        today = datetime.now().strftime("%Y-%m-%d")
        
        tasks = {
            "date": today,
            "content_tasks": [],
            "engagement_tasks": [],
            "analytics_tasks": []
        }
        
        # Content tasks
        if self.config["content"]["threads_ready"]:
            tasks["content_tasks"].append({
                "type": "thread",
                "topic": self.config["content"]["threads_ready"][0],
                "priority": "high",
                "time": self.config["content"]["posting_times"][0]
            })
        
        # Engagement tasks
        for target in self.config["targets"]["tier_1"][:3]:
            tasks["engagement_tasks"].append({
                "type": "strategic_reply",
                "target": target,
                "priority": "medium"
            })
        
        # Analytics tasks
        tasks["analytics_tasks"].append({
            "type": "metrics_check",
            "priority": "low"
        })
        
        return tasks
    
    def generate_daily_digest(self) -> str:
        """Generate daily digest for Telegram"""
        tasks = self.get_daily_tasks()
        
        digest = f"""Daily X Mission Digest - {tasks['date']}

Account Status:
- Followers: {self.config['account']['current_followers']} / {self.config['account']['target_followers']}
- Progress: {(self.config['account']['current_followers']/self.config['account']['target_followers']*100):.1f}%

Today's Content Tasks:
"""
        
        for i, task in enumerate(tasks['content_tasks'], 1):
            digest += f"{i}. [{task['priority'].upper()}] {task['type']} - {task['topic']} @ {task['time']}\n"
        
        if not tasks['content_tasks']:
            digest += "No content tasks scheduled\n"
        
        digest += """
Today's Engagement Targets:
"""
        for i, task in enumerate(tasks['engagement_tasks'], 1):
            digest += f"{i}. Reply to @{task['target']}\n"
        
        digest += """
Quick Actions:
- "post hims thread" - Post HIMS thread
- "post ai thread" - Post AI commerce thread  
- "show metrics" - Check performance
- "add target @handle" - Add engagement target

Reply with task number or command to execute."""
        
        return digest
    
    def track_metrics(self, metrics: Dict):
        """Track daily metrics"""
        today = datetime.now().strftime("%Y-%m-%d")
        metrics_file = os.path.join(self.data_dir, f"metrics_{today}.json")
        
        with open(metrics_file, 'w') as f:
            json.dump(metrics, f, indent=2)
        
        logger.info(f"Metrics tracked for {today}")
    
    def load_cached_template(self, category: str, template_name: str) -> Optional[str]:
        """Load cached reply template"""
        try:
            with open("cached_templates.json", 'r') as f:
                templates = json.load(f)
                return templates.get("categories", {}).get(category, {}).get(template_name)
        except:
            return None
    
    def add_thread_to_queue(self, topic: str, content: str):
        """Add thread to ready queue"""
        if topic not in self.config["content"]["threads_ready"]:
            self.config["content"]["threads_ready"].append(topic)
            self.save_config()
            logger.info(f"Added {topic} thread to queue")
    
    def complete_thread(self, topic: str):
        """Mark thread as completed"""
        if topic in self.config["content"]["threads_ready"]:
            self.config["content"]["threads_ready"].remove(topic)
            self.save_config()
            logger.info(f"Completed {topic} thread")
    
    def update_follower_count(self, count: int):
        """Update current follower count"""
        old_count = self.config["account"]["current_followers"]
        self.config["account"]["current_followers"] = count
        self.save_config()
        
        growth = count - old_count
        logger.info(f"Follower count updated: {old_count} -> {count} ({growth:+d})")
        return growth


def main():
    """CLI interface for automation tool"""
    if len(sys.argv) < 2:
        print("Usage: python x_automation.py [command]")
        print("\nCommands:")
        print("  digest       - Generate daily digest")
        print("  tasks        - Show today's tasks")
        print("  config       - Show current config")
        print("  init         - Initialize automation system")
        return
    
    command = sys.argv[1]
    automation = XAutomation()
    
    if command == "digest":
        print(automation.generate_daily_digest())
    
    elif command == "tasks":
        tasks = automation.get_daily_tasks()
        print(json.dumps(tasks, indent=2))
    
    elif command == "config":
        print(json.dumps(automation.config, indent=2))
    
    elif command == "init":
        print("[OK] X Automation system initialized!")
        print(f"Config file: {automation.config_path}")
        print(f"Data directory: {automation.data_dir}")
        print("\nNext steps:")
        print("1. Run 'python x_automation.py digest' for daily digest")
        print("2. Set up cron jobs for automation (see automation_cron.json)")
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
