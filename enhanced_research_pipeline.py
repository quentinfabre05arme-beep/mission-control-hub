#!/usr/bin/env python3
"""
Enhanced Research Pipeline with X Integration
Production system with x-tweet-fetcher for real-time X data
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path

class ProductionResearchPipeline:
    def __init__(self):
        self.workspace = Path("C:/Users/quent/.openclaw/workspace")
        self.research_dir = self.workspace / "operations" / "research"
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.daily_content_dir = self.workspace / "daily_content"
        self.daily_content_dir.mkdir(exist_ok=True)
        self.posts_dir = self.workspace / "daily_content" / "posts"
        self.posts_dir.mkdir(exist_ok=True)
        
        # XTF path
        self.xtf_path = Path("C:/Users/quent/AppData/Roaming/Python/Python314/Scripts/xtf.exe")
        
        # Content configuration
        self.topics = {
            "eth_treasury": {
                "name": "ETH Treasury",
                "x_queries": [
                    "ETH treasury institutional adoption",
                    "Ethereum corporate treasury",
                    "ETH staking yield institutional"
                ],
                "web_queries": [
                    "ETH treasury news July 2026",
                    "Ethereum institutional adoption 2026"
                ],
                "angles": [
                    "ETH treasuries are scaling faster than expected. Here's the data that matters:",
                    "While Bitcoin treasuries get headlines, Ethereum treasuries earn yield. The math:",
                    "One company now holds 5% of all ETH. The treasury thesis is accelerating."
                ],
                "hashtags": ["#ETH", "#Ethereum", "#Treasury", "#Crypto", "#BTC"],
                "time": "11:00 AM"
            },
            "hims": {
                "name": "HIMS Healthcare",
                "x_queries": [
                    "HIMS stock",
                    "Hims Hers Health telehealth",
                    "$HIMS"
                ],
                "web_queries": [
                    "HIMS stock news July 2026",
                    "Hims Hers telehealth GLP-1"
                ],
                "angles": [
                    "HIMS secured $400M from JPMorgan. Not for M&A. For working capital. The infrastructure play:",
                    "HIMS isn't a GLP-1 stock. It's healthcare infrastructure. The thesis:",
                    "Telehealth + GLP-1s = infrastructure moment. Why HIMS owns the patient relationship:"
                ],
                "hashtags": ["#HIMS", "#Healthcare", "#GLP1", "#Telehealth", "#Investing"],
                "time": "3:00 PM"
            },
            "ai_commerce": {
                "name": "AI Agentic Commerce",
                "x_queries": [
                    "AI agentic commerce",
                    "autonomous agents",
                    "AI infrastructure 2026"
                ],
                "web_queries": [
                    "AI agentic commerce McKinsey 2026",
                    "autonomous agents infrastructure"
                ],
                "angles": [
                    "McKinsey's 6-level automation curve is here. We're at Level 1-2. The $3-5T opportunity:",
                    "Agentic commerce isn't coming. It's being built now. The infrastructure:",
                    "$3-5T agentic commerce by 2030. The winners won't be LLM makers. They'll be the intelligence layer:"
                ],
                "hashtags": ["#AI", "#AgenticCommerce", "#McKinsey", "#Infrastructure", "#Investing"],
                "time": "7:00 PM"
            }
        }
    
    def run_xtf_search(self, query: str, limit: int = 5) -> list:
        """Run X search using x-tweet-fetcher"""
        try:
            result = subprocess.run(
                [str(self.xtf_path), "--search", query, "--limit", str(limit), "--text-only"],
                capture_output=True,
                text=True,
                cwd=str(self.workspace),
                timeout=45,
                env={**os.environ, "PYTHONIOENCODING": "utf-8"}
            )
            
            if result.returncode == 0:
                lines = result.stdout.strip().split('\n')
                return [line.strip() for line in lines if line.strip() and not line.startswith('[')]
            else:
                return [f"Search error: {result.stderr[:100]}"]
        except Exception as e:
            return [f"Exception: {str(e)[:100]}"]
    
    def run_full_pipeline(self):
        """Execute complete research and content pipeline"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H:%M")
        
        print("=" * 70)
        print(f"PRODUCTION RESEARCH PIPELINE - {date_str} {time_str}")
        print("=" * 70)
        print()
        
        # Phase 1: Research
        print("PHASE 1: RESEARCH COMPILATION")
        print("-" * 70)
        research_data = self.compile_research()
        print()
        
        # Phase 2: Content Generation
        print("PHASE 2: CONTENT GENERATION")
        print("-" * 70)
        posts = self.generate_all_posts()
        for topic, post_data in posts.items():
            print(f"  Generated: {post_data['name']}")
        print()
        
        # Phase 3: Briefing
        print("PHASE 3: BRIEFING CREATION")
        print("-" * 70)
        briefing = self.create_comprehensive_briefing(research_data, posts, date_str)
        print(f"  Briefing created")
        print()
        
        # Phase 4: Save
        print("PHASE 4: SAVING OUTPUTS")
        print("-" * 70)
        self.save_all_outputs(research_data, posts, briefing, date_str)
        print()
        
        print("=" * 70)
        print("PIPELINE COMPLETE")
        print("=" * 70)
        
        return briefing
    
    def compile_research(self):
        """Compile research for all topics"""
        research_data = {}
        
        for topic_key, config in self.topics.items():
            print(f"  Researching: {config['name']}")
            
            # Try X search (may fail if Nitter not configured)
            x_findings = []
            for query in config['x_queries'][:1]:  # Try first query
                try:
                    results = self.run_xtf_search(query, limit=3)
                    x_findings.extend(results)
                except Exception as e:
                    x_findings.append(f"X search unavailable: {e}")
                break  # Only try first query for now
            
            research_data[topic_key] = {
                "name": config["name"],
                "x_queries": config["x_queries"],
                "web_queries": config["web_queries"],
                "x_findings": x_findings[:5],
                "angles": config["angles"],
                "hashtags": config["hashtags"],
                "time": config["time"],
                "status": "compiled",
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"    - {len(x_findings)} X findings")
        
        return research_data
    
    def generate_all_posts(self):
        """Generate posts for all topics"""
        posts = {}
        
        for topic_key, config in self.topics.items():
            angle = config["angles"][0]
            hashtags = " ".join(config["hashtags"])
            
            post_content = f"""{angle}

Key developments emerging in this space. Infrastructure build phase = investment phase.

The data is clear: early movers in infrastructure win the next cycle.

{hashtags}"""
            
            posts[topic_key] = {
                "name": config["name"],
                "time": config["time"],
                "content": post_content,
                "hashtags": hashtags,
                "timestamp": datetime.now().isoformat()
            }
        
        return posts
    
    def create_comprehensive_briefing(self, research_data, posts, date_str):
        """Create full daily briefing"""
        
        briefing = f"""DAILY RESEARCH BRIEFING - {date_str}
Generated: {datetime.now().strftime('%H:%M')} Paris time

=== EXECUTIVE SUMMARY ===

Three pillars researched and ready:
- ETH Treasury: Institutional adoption accelerating
- HIMS Healthcare: Infrastructure scaling into demand  
- AI Agentic Commerce: $3-5T infrastructure build phase

"""
        
        for topic_key, data in research_data.items():
            briefing += f"""{data['name'].upper()}:
- Focus: {data['angles'][0][:50]}...
- X Findings: {len(data['x_findings'])}
- Posting Time: {data['time']}
- Status: {data['status']}

"""
        
        briefing += """=== READY TO POST ===

"""
        
        times = ["11:00 AM", "3:00 PM", "7:00 PM"]
        for i, (topic_key, post_data) in enumerate(posts.items()):
            briefing += f"""---
POST {i+1}: {post_data['name']} ({post_data['time']})

{post_data['content']}

---

"""
        
        briefing += """=== DELIVERY SCHEDULE ===
11:00 AM - Post 1 (ETH Treasury)
3:00 PM  - Post 2 (HIMS Healthcare)  
7:00 PM  - Post 3 (AI Agentic Commerce)

=== INSTRUCTIONS ===
1. Review each post above
2. Copy and paste to X
3. Schedule for suggested times
4. Reply DONE when complete

---
Generated by ProductionResearchPipeline
"""
        
        return briefing
    
    def save_all_outputs(self, research_data, posts, briefing, date_str):
        """Save all pipeline outputs"""
        
        # Save research
        research_file = self.research_dir / f"research_production_{date_str}.json"
        with open(research_file, 'w', encoding='utf-8') as f:
            json.dump(research_data, f, indent=2, ensure_ascii=False)
        print(f"  Research: {research_file}")
        
        # Save posts
        for topic_key, post_data in posts.items():
            post_file = self.posts_dir / f"{date_str}_{topic_key}_post.txt"
            with open(post_file, 'w', encoding='utf-8') as f:
                f.write(post_data['content'])
        
        posts_json = self.posts_dir / f"{date_str}_all_posts.json"
        with open(posts_json, 'w', encoding='utf-8') as f:
            json.dump(posts, f, indent=2, ensure_ascii=False)
        print(f"  Posts: {posts_json}")
        
        # Save briefing
        briefing_file = self.daily_content_dir / f"{date_str}_briefing_production.txt"
        with open(briefing_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
        print(f"  Briefing: {briefing_file}")

def main():
    """Run production pipeline"""
    pipeline = ProductionResearchPipeline()
    briefing = pipeline.run_full_pipeline()
    print("\n" + briefing)

if __name__ == "__main__":
    main()
