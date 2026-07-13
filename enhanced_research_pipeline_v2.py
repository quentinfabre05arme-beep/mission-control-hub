#!/usr/bin/env python3
"""
Enhanced Research Pipeline v2.0
Integrated with 2025-2026 AI agent research findings
Features: Multi-angle content, algorithm optimization, rich media suggestions
"""

import json
import subprocess
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional
import random

class EnhancedResearchPipelineV2:
    """
    Production research pipeline with algorithm-aware content generation
    Based on 2025-2026 best practices research
    """
    
    def __init__(self):
        self.workspace = Path("C:/Users/quent/.openclaw/workspace")
        self.research_dir = self.workspace / "operations" / "research"
        self.research_dir.mkdir(parents=True, exist_ok=True)
        self.daily_content_dir = self.workspace / "daily_content"
        self.daily_content_dir.mkdir(exist_ok=True)
        self.posts_dir = self.workspace / "daily_content" / "posts"
        self.posts_dir.mkdir(exist_ok=True)
        
        # XTF path (for when Nitter is configured)
        self.xtf_path = Path("C:/Users/quent/AppData/Roaming/Python/Python314/Scripts/xtf.exe")
        
        # Algorithm insights from research
        self.engagement_weights = {
            "retweet": 20,
            "reply": 13.5,
            "profile_click": 12,
            "link_click": 11,
            "like": 1  # Baseline
        }
        
        # Content configuration with research-backed enhancements
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
                    {
                        "hook": "ETH treasuries are scaling faster than expected. Here's the data that matters:",
                        "type": "data-driven",
                        "engagement_score": 18
                    },
                    {
                        "hook": "While Bitcoin treasuries get headlines, Ethereum treasuries earn yield. The math:",
                        "type": "comparison",
                        "engagement_score": 16
                    },
                    {
                        "hook": "One company now holds 5% of all ETH. The treasury thesis is accelerating.",
                        "type": "surprise-factor",
                        "engagement_score": 19
                    },
                    {
                        "hook": "The ETH treasury play nobody's talking about. Thread",
                        "type": "thread-hook",
                        "engagement_score": 20
                    }
                ],
                "key_data": {
                    "bitmine_holdings": "5.74M ETH",
                    "annual_yield": "$277M",
                    "supply_percentage": "4.8%",
                    "staking_rate": "~3.5%"
                },
                "hashtags": ["#ETH", "#Ethereum", "#Treasury", "#Crypto", "#BTC"],
                "media_suggestions": [
                    "ETH price chart showing treasury accumulation",
                    "Bitmine ETH holdings visualization",
                    "Staking yield comparison infographic"
                ],
                "time": "11:00 AM",
                "optimal_days": ["Tuesday", "Wednesday", "Thursday"]
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
                    {
                        "hook": "HIMS secured $400M from JPMorgan. Not for M&A. For working capital. The infrastructure play:",
                        "type": "data-driven",
                        "engagement_score": 17
                    },
                    {
                        "hook": "HIMS isn't a GLP-1 stock. It's healthcare infrastructure. The thesis:",
                        "type": "reframe",
                        "engagement_score": 18
                    },
                    {
                        "hook": "Telehealth + GLP-1s = infrastructure moment. Why HIMS owns the patient relationship:",
                        "type": "insight",
                        "engagement_score": 16
                    },
                    {
                        "hook": "The $400M nobody's analyzing. Why HIMS just leapfrogged the competition",
                        "type": "thread-hook",
                        "engagement_score": 20
                    }
                ],
                "key_data": {
                    "facility_size": "$400M",
                    "stock_run": "45%",
                    "subscribers": "2.6M",
                    "lender": "JPMorgan"
                },
                "hashtags": ["#HIMS", "#Healthcare", "#GLP1", "#Telehealth", "#Investing"],
                "media_suggestions": [
                    "HIMS stock price chart with facility announcement",
                    "GLP-1 market size infographic",
                    "Telehealth growth comparison"
                ],
                "time": "3:00 PM",
                "optimal_days": ["Tuesday", "Wednesday", "Thursday"]
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
                    {
                        "hook": "McKinsey's 6-level automation curve is here. We're at Level 1-2. The $3-5T opportunity:",
                        "type": "data-driven",
                        "engagement_score": 19
                    },
                    {
                        "hook": "Agentic commerce isn't coming. It's being built now. The infrastructure:",
                        "type": "insight",
                        "engagement_score": 17
                    },
                    {
                        "hook": "$3-5T agentic commerce by 2030. The winners won't be LLM makers. They'll be the intelligence layer:",
                        "type": "contrarian",
                        "engagement_score": 20
                    },
                    {
                        "hook": "The 6 levels of agentic automation. Where we are vs. where we're going",
                        "type": "thread-hook",
                        "engagement_score": 21
                    }
                ],
                "key_data": {
                    "market_projection": "$3-5T",
                    "target_year": "2030",
                    "automation_level": "Level 1-2",
                    "protocols": ["MCP", "A2A"]
                },
                "hashtags": ["#AI", "#AgenticCommerce", "#McKinsey", "#Infrastructure", "#Investing"],
                "media_suggestions": [
                    "McKinsey automation curve visualization",
                    "Agentic commerce market size chart",
                    "MCP/A2A protocol architecture diagram"
                ],
                "time": "7:00 PM",
                "optimal_days": ["Monday", "Tuesday", "Wednesday"]
            }
        }
        
        # Thread templates for high-engagement content
        self.thread_templates = {
            "standard": [
                "{hook}\n\nKey developments emerging in this space:",
                "1/ The data shows {key_point_1}",
                "2/ {key_point_2}",
                "3/ {key_point_3}",
                "The pattern is clear: {conclusion}\n\n{hashtags}"
            ],
            "data_driven": [
                "{hook}",
                "",
                "Key numbers:",
                "- {metric_1}",
                "- {metric_2}",
                "- {metric_3}",
                "",
                "What this means: {insight}\n\n{hashtags}"
            ],
            "insight": [
                "{hook}",
                "",
                "Most people miss this:",
                "",
                "{insight_point}",
                "",
                "The implication: {implication}\n\n{hashtags}"
            ]
        }
    
    def select_best_angle(self, topic_key: str) -> Dict:
        """Select highest-scoring angle based on engagement research"""
        topic = self.topics[topic_key]
        angles = topic["angles"]
        
        # Weight toward thread hooks (highest engagement per research)
        weights = [a["engagement_score"] for a in angles]
        selected = random.choices(angles, weights=weights, k=1)[0]
        
        return selected
    
    def generate_thread_structure(self, topic_key: str, angle: Dict) -> Dict:
        """Generate thread structure optimized for engagement"""
        topic = self.topics[topic_key]
        data = topic["key_data"]
        
        if angle["type"] == "thread-hook":
            # Full thread structure
            if topic_key == "eth_treasury":
                return {
                    "format": "thread",
                    "posts": [
                        f"{angle['hook']}\n\n(Thread)",
                        f"1/ Bitmine holds {data['bitmine_holdings']} ({data['supply_percentage']} of supply)\n\nAt 3.5% staking yield = ${data['annual_yield']} annual income\n\nThey get paid to hold. BTC treasuries don't.",
                        f"2/ The institutional shift:\n\n- MicroStrategy: BTC treasury (no yield)\n- Bitmine: ETH treasury (earning yield)\n\nSame conviction. Different economics.",
                        f"3/ Why this matters:\n\nETH staking = productive asset\nBTC holding = speculative asset\n\nProductive assets compound. Speculative assets don't.",
                        f"The data is clear: early movers in productive infrastructure win the next cycle.\n\n{' '.join(topic['hashtags'][:3])}"
                    ]
                }
            elif topic_key == "hims":
                return {
                    "format": "thread",
                    "posts": [
                        f"{angle['hook']}\n\n(Thread)",
                        f"1/ {data['facility_size']} from {data['lender']}\n\nNot for acquisitions. For working capital.\n\nThis is infrastructure scaling, not growth buying.",
                        f"2/ The GLP-1 demand is real:\n\n- {data['subscribers']} and growing\n- Stock up {data['stock_run']}\n- Infrastructure constrained, not demand\n\nHIMS solves the constraint.",
                        f"3/ Why infrastructure > product:\n\nGLP-1 makers = commodity\nPatient relationships = moat\n\nHIMS owns the relationship layer.",
                        f"Infrastructure build phase = investment phase.\n\n{' '.join(topic['hashtags'][:3])}"
                    ]
                }
            elif topic_key == "ai_commerce":
                return {
                    "format": "thread",
                    "posts": [
                        f"{angle['hook']}\n\n(Thread)",
                        f"1/ Level 0-1: Rules-based automation\nLevel 2-3: AI-assisted tasks\nLevel 4-5: Autonomous agents\nLevel 6: Fully autonomous commerce\n\nWe're at 1-2.",
                        f"2/ The {data['market_projection']} by {data['target_year']} isn't about chatbots.\n\nIt's about agents that:\n- Perceive environments\n- Plan multi-step actions\n- Execute without humans\n\nInfrastructure being built now.",
                        f"3/ Winners won't be LLM makers.\n\nThey'll be the intelligence layer that connects agents to commerce.\n\nProtocols like {', '.join(data['protocols'])} are the TCP/IP of agentic commerce.",
                        f"The infrastructure build phase = the investment phase.\n\n{' '.join(topic['hashtags'][:3])}"
                    ]
                }
        else:
            # Single post with engagement hooks
            return {
                "format": "single",
                "content": self._generate_single_post(topic_key, angle)
            }
    
    def _generate_single_post(self, topic_key: str, angle: Dict) -> str:
        """Generate single post optimized for engagement"""
        topic = self.topics[topic_key]
        data = topic["key_data"]
        hashtags = " ".join(topic["hashtags"])
        
        # Add engagement hook
        engagement_hooks = [
            "Thoughts?",
            "Agree or disagree?",
            "What am I missing?",
            "Who else sees this?"
        ]
        hook = random.choice(engagement_hooks)
        
        post = f"""{angle['hook']}

Key developments emerging in this space. Infrastructure build phase = investment phase.

The data is clear: early movers in infrastructure win the next cycle.

{hook}

{hashtags}"""
        
        return post
    
    def generate_reply_hooks(self, topic_key: str) -> List[str]:
        """Generate reply hooks to drive engagement (13.5x weight)"""
        hooks = {
            "eth_treasury": [
                "What's your ETH treasury target price?",
                "BTC vs ETH treasury - which side are you on?",
                "Who else is stacking ETH for yield?",
                "What other companies should adopt ETH treasuries?"
            ],
            "hims": [
                "What's your HIMS price target?",
                "GLP-1 stocks: who's positioned best?",
                "Telehealth or pharma - which wins?",
                "Who's your pick for healthcare infrastructure?"
            ],
            "ai_commerce": [
                "Which AI infrastructure play are you watching?",
                "What level of automation excites you most?",
                "MCP or A2A - which protocol wins?",
                "Who's building the intelligence layer?"
            ]
        }
        return hooks.get(topic_key, ["Thoughts?"])
    
    def run_full_pipeline(self):
        """Execute complete enhanced research and content pipeline"""
        date_str = datetime.now().strftime("%Y-%m-%d")
        time_str = datetime.now().strftime("%H:%M")
        day_name = datetime.now().strftime("%A")
        
        print("=" * 70)
        print(f"ENHANCED RESEARCH PIPELINE v2.0 - {date_str} {time_str}")
        print("=" * 70)
        print("Algorithm-optimized | Multi-angle | Engagement-focused")
        print("=" * 70)
        print()
        
        # Phase 1: Content Generation with Algorithm Insights
        print("PHASE 1: ALGORITHM-OPTIMIZED CONTENT GENERATION")
        print("-" * 70)
        posts = self.generate_all_content(day_name)
        for topic, post_data in posts.items():
            print(f"  [OK] {post_data['name']} (Score: {post_data['engagement_score']}/21)")
        print()
        
        # Phase 2: Reply Hooks
        print("PHASE 2: ENGAGEMENT HOOKS (13.5x weight)")
        print("-" * 70)
        reply_hooks = {}
        for topic_key in self.topics.keys():
            hooks = self.generate_reply_hooks(topic_key)
            reply_hooks[topic_key] = hooks
            print(f"  [OK] {self.topics[topic_key]['name']}: {len(hooks)} hooks ready")
        print()
        
        # Phase 3: Media Suggestions
        print("PHASE 3: RICH MEDIA SUGGESTIONS")
        print("-" * 70)
        media_suggestions = {}
        for topic_key, config in self.topics.items():
            media_suggestions[topic_key] = config["media_suggestions"]
            print(f"  [OK] {config['name']}: {len(config['media_suggestions'])} suggestions")
        print()
        
        # Phase 4: Briefing
        print("PHASE 4: ENHANCED BRIEFING")
        print("-" * 70)
        briefing = self.create_enhanced_briefing(posts, reply_hooks, media_suggestions, date_str, day_name)
        print(f"  [OK] Briefing created with algorithm insights")
        print()
        
        # Phase 5: Save
        print("PHASE 5: SAVING OUTPUTS")
        print("-" * 70)
        self.save_all_outputs(posts, reply_hooks, media_suggestions, briefing, date_str)
        print()
        
        print("=" * 70)
        print("PIPELINE COMPLETE - v2.0")
        print("=" * 70)
        print(f"Posts generated: {len(posts)}")
        print(f"Reply hooks ready: {sum(len(h) for h in reply_hooks.values())}")
        print(f"Media suggestions: {sum(len(m) for m in media_suggestions.values())}")
        print("=" * 70)
        
        return briefing
    
    def generate_all_content(self, day_name: str) -> Dict:
        """Generate all content with day optimization"""
        posts = {}
        
        for topic_key, config in self.topics.items():
            # Skip if not optimal day (optional optimization)
            # if day_name not in config.get("optimal_days", []):
            #     continue
            
            # Select best angle
            angle = self.select_best_angle(topic_key)
            
            # Generate content structure
            content_structure = self.generate_thread_structure(topic_key, angle)
            
            # Calculate engagement score
            base_score = angle["engagement_score"]
            format_bonus = 3 if content_structure["format"] == "thread" else 0
            total_score = base_score + format_bonus
            
            posts[topic_key] = {
                "name": config["name"],
                "time": config["time"],
                "format": content_structure["format"],
                "content": content_structure.get("posts") or content_structure.get("content"),
                "angle_type": angle["type"],
                "engagement_score": total_score,
                "hashtags": " ".join(config["hashtags"]),
                "key_data": config["key_data"],
                "timestamp": datetime.now().isoformat()
            }
        
        return posts
    
    def create_enhanced_briefing(self, posts: Dict, reply_hooks: Dict, 
                                  media_suggestions: Dict, date_str: str, day_name: str) -> str:
        """Create algorithm-aware daily briefing"""
        
        briefing = f"""[ENHANCED DAILY BRIEFING v2.0 - {date_str}]
Generated: {datetime.now().strftime('%H:%M')} Paris time | Day: {day_name}
Algorithm-Optimized | Research-Backed | Engagement-Focused

================================================================================
[ALGORITHM INSIGHTS] (2025-2026 Research)
================================================================================

Engagement Hierarchy (by weight):
  - Retweets: 20x (HIGHEST VALUE - prioritize shareable content)
  - Replies: 13.5x (Use engagement hooks to drive discussion)
  - Profile clicks: 12x (Strong hooks increase curiosity)
  - Link clicks: 11x (Data-rich content drives clicks)
  - Likes: 1x (Baseline - not prioritized by algorithm)

Optimal Strategy:
  [x] Post 3-10x daily for visibility
  [x] Use rich media (images boost engagement)
  [x] Thread format for complex topics
  [x] Ask questions to drive replies
  [x] Morning posting (8-10 AM) for original content

================================================================================
[TODAY'S CONTENT] (Algorithm-Optimized)
================================================================================

"""
        
        for i, (topic_key, post_data) in enumerate(posts.items(), 1):
            briefing += f"""
--------------------------------------------------------------------------------
[POST {i}] {post_data['name'].upper()}
--------------------------------------------------------------------------------
Time: {post_data['time']} | Format: {post_data['format'].upper()}
Angle Type: {post_data['angle_type']} | Engagement Score: {post_data['engagement_score']}/24

"""
            if post_data['format'] == 'thread':
                briefing += "THREAD CONTENT:\n\n"
                for j, post in enumerate(post_data['content'], 1):
                    briefing += f"[{j}/{len(post_data['content'])}]\n{post}\n\n"
            else:
                briefing += f"SINGLE POST:\n{post_data['content']}\n"
            
            briefing += f"""
[REPLY HOOKS] (Use to drive 13.5x engagement):
"""
            for hook in reply_hooks.get(topic_key, ["Thoughts?"]):
                briefing += f"  - {hook}\n"
            
            briefing += f"""
[MEDIA SUGGESTIONS]:
"""
            for suggestion in media_suggestions.get(topic_key, []):
                briefing += f"  - {suggestion}\n"
            
            briefing += "\n"
        
        briefing += f"""
================================================================================
[POSTING SCHEDULE]
================================================================================

11:00 AM - Post 1 (ETH Treasury) - {posts.get('eth_treasury', {}).get('format', 'single').upper()}
3:00 PM  - Post 2 (HIMS Healthcare) - {posts.get('hims', {}).get('format', 'single').upper()}
7:00 PM  - Post 3 (AI Agentic Commerce) - {posts.get('ai_commerce', {}).get('format', 'single').upper()}

================================================================================
[ENGAGEMENT TACTICS] (From Research)
================================================================================

1. After posting, wait 30-60 minutes then reply to early engagers
2. Use reply hooks (provided above) to drive discussion
3. Quote tweet with additional context if engagement is high
4. Cross-reference between pillars when relevant
5. Reply DONE after posting so I can track

================================================================================
[CHECKLIST]
================================================================================

Before posting:
  [ ] Review content for accuracy
  [ ] Prepare media (if using rich content)
  [ ] Set up reply hooks in notes
  
After posting:
  [ ] Monitor first 30 minutes for engagement
  [ ] Reply to early comments with hooks
  [ ] Track which hook drove most replies
  [ ] Report back: engagement metrics + what worked

================================================================================

Generated by EnhancedResearchPipelineV2
Research-backed | Algorithm-optimized | Mission: 212 -> 10,000 followers

"""
        
        return briefing
    
    def save_all_outputs(self, posts: Dict, reply_hooks: Dict, 
                         media_suggestions: Dict, briefing: str, date_str: str):
        """Save all pipeline outputs"""
        
        # Save posts with full structure
        posts_data = {
            "date": date_str,
            "posts": posts,
            "reply_hooks": reply_hooks,
            "media_suggestions": media_suggestions,
            "metadata": {
                "version": "2.0",
                "algorithm_optimized": True,
                "engagement_focused": True,
                "generated_at": datetime.now().isoformat()
            }
        }
        
        posts_json = self.posts_dir / f"{date_str}_enhanced_posts_v2.json"
        with open(posts_json, 'w', encoding='utf-8') as f:
            json.dump(posts_data, f, indent=2, ensure_ascii=False)
        print(f"  [OK] Posts: {posts_json}")
        
        # Save individual post files
        for topic_key, post_data in posts.items():
            post_file = self.posts_dir / f"{date_str}_{topic_key}_v2.txt"
            with open(post_file, 'w', encoding='utf-8') as f:
                if isinstance(post_data['content'], list):
                    f.write(f"THREAD: {post_data['name']}\n")
                    f.write(f"Time: {post_data['time']}\n")
                    f.write(f"Engagement Score: {post_data['engagement_score']}/24\n\n")
                    for i, post in enumerate(post_data['content'], 1):
                        f.write(f"[{i}] {post}\n\n")
                else:
                    f.write(f"SINGLE POST: {post_data['name']}\n")
                    f.write(f"Time: {post_data['time']}\n")
                    f.write(f"Engagement Score: {post_data['engagement_score']}/24\n\n")
                    f.write(post_data['content'])
        
        # Save briefing
        briefing_file = self.daily_content_dir / f"{date_str}_briefing_v2.txt"
        with open(briefing_file, 'w', encoding='utf-8') as f:
            f.write(briefing)
        print(f"  [OK] Briefing: {briefing_file}")
        
        # Save to legacy location for compatibility
        legacy_briefing = self.daily_content_dir / f"{date_str}_briefing_production.txt"
        with open(legacy_briefing, 'w', encoding='utf-8') as f:
            f.write(briefing)
        print(f"  [OK] Legacy briefing: {legacy_briefing}")

def main():
    """Run enhanced production pipeline"""
    pipeline = EnhancedResearchPipelineV2()
    briefing = pipeline.run_full_pipeline()
    print("\n" + briefing)

if __name__ == "__main__":
    main()
