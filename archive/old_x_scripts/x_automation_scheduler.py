#!/usr/bin/env python3
"""
X Automation Scheduler
Runs automation tasks at scheduled times
"""

import asyncio
import json
import random
from datetime import datetime, timedelta
from pathlib import Path
from x_automation_system import XAutomationSystem

class ContentLibrary:
    """Pre-built content templates"""
    
    THREADS = {
        "hims_healthcare": [
            "The GLP-1 revolution is bigger than the drug.\n\nThe real infrastructure play is HIMS — the telehealth rails delivering these treatments to millions.\n\nHere's why HIMS is healthcare's picks and shovels story 👇",
            "1/ The Problem\n\nTraditional healthcare can't handle GLP-1 demand:\n- Months-long wait times for specialists\n- Insurance nightmares\n- Limited access in rural areas\n\nHIMS solved this with direct-to-consumer telehealth.",
            "2/ The Scale\n\nHIMS 2024 numbers:\n- $725M revenue (+62% YoY)\n- 2.5M+ subscribers\n- 85% gross margins on subscriptions\n- Novo Nordisk partnership locked\n\nThis isn't a startup. This is infrastructure.",
            "3/ The GLP-1 Angle\n\nHIMS isn't just prescribing — they're building the logistics layer:\n- Personalized dosing protocols\n- Supply chain management\n- Patient monitoring systems\n- Insurance navigation\n\nWhen 50M Americans are on GLP-1s, who delivers them? HIMS.",
            "4/ The Valuation Disconnect\n\nHIMS trades at 3x revenue\n\nTeladoc (weaker business): 2.5x\nCVS (slow growth): 0.4x\nUnitedHealth (insurance): 1.3x\n\nThe market doesn't understand the infrastructure play yet.",
            "5/ The Thesis\n\nHIMS isn't a telehealth company.\n\nIt's the AWS of healthcare delivery — the infrastructure layer that enables the GLP-1 revolution to scale.\n\nPosition: Long HIMS\nTarget: $50B market cap (10x from here)",
        ],
        "ai_agentic_commerce": [
            "McKinsey says $3-5 TRILLION in agentic commerce by 2030.\n\nThat's larger than the entire e-commerce market today.\n\nHere's how to position for the AI agent revolution 👇",
            "1/ What is Agentic Commerce?\n\nInstead of YOU shopping, AI agents shop FOR you:\n- \"Book me a flight to NYC next Tuesday\"\n- \"Order groceries based on my meal plan\"\n- \"Find me the best rate on car insurance\"\n\nThe agent becomes the customer.",
            "2/ The Winners Won't Be LLM Makers\n\nOpenAI, Anthropic, Google — they provide the brain.\n\nThe winners will be the companies that OWN the customer relationship:\n- NBIS (banking agents)\n- ZETA (restaurant ordering)\n- PLTR (enterprise agents)",
            "3/ The Infrastructure Play\n\nEvery agent needs:\n- Data enrichment → PLTR, ZETA\n- Identity verification → NBIS\n- Payment rails → existing fintech\n- Orchestration → ServiceNow, Salesforce",
            "4/ Portfolio Positioning\n\nCore: NBIS (banking agent infrastructure)\nGrowth: PLTR (enterprise agents)\nEmerging: ZETA (restaurant/retail)\n\nAvoid: Pure LLM plays (commoditized)",
            "5/ The Timeline\n\n2025: Enterprise pilots\n2026-2027: Early consumer adoption\n2028-2030: Mass adoption\n\nWe're in the infrastructure build phase NOW.",
            "The $3-5T opportunity isn't hype.\n\nIt's the natural evolution of e-commerce → agentic commerce.\n\nPosition before the market understands the infrastructure layer.",
        ],
        "eth_treasury": [
            "19 public companies now hold ETH as treasury reserve.\n\nThe ETH treasury playbook is emerging — and it's more compelling than BTC.\n\nHere's why CFOs are choosing ETH over BTC 👇",
            "1/ The Yield Advantage\n\nBTC treasuries: Store of value, 0% yield\nETH treasuries: Store of value + 3-4% staking yield\n\nFor a $100M treasury:\n- BTC: $0 income\n- ETH: $3-4M annual yield\n\nThat's material to a balance sheet.",
            "2/ The Adoption Curve\n\nETH treasury adoption is 2 years behind BTC:\n- BTC: Started 2020, now 70+ companies\n- ETH: Started 2024, now 19 companies\n\nWe're early in the adoption curve.",
            "3/ The Regulatory Clarity\n\nETH ETF approval = regulatory clarity\nStaking services = revenue recognition\n\nCFOs can now justify ETH treasuries to boards with clear accounting.",
            "4/ The Companies Leading\n\nNotable ETH treasuries:\n- GameStop (GME) — $1.5B ETH\n- Ethereum Treasury Corp — $500M\n- Various DeFi protocols\n\nThis list will grow exponentially.",
            "5/ Why ETH > BTC for Treasuries\n\n✓ Native yield (3-4%)\n✓ Lower volatility (ETH/BTC ratio stable)\n✓ Growing ecosystem (DeFi, L2s)\n✓ Regulatory clarity (ETF approved)\n\nThe math favors ETH.",
            "The next wave of treasury adoption won't be BTC copycats.\n\nIt will be ETH-native companies leveraging yield + ecosystem growth.\n\nPosition: ETH treasury proxy plays\nWatch: Q3-Q4 2025 earnings calls for new adopters",
        ]
    }
    
    REPLIES = {
        "eth_treasury": [
            "The BTC treasury playbook is proven. The next evolution is earning yield while holding — that's where ETH treasuries come in. 3-4% staking APR changes the math for CFOs.",
            "Exactly. ETH treasuries give you the store of value + yield generation. For a $100M treasury, that's $3-4M annual income. Material difference.",
            "This is why ETH treasuries make sense. Same macro hedge as BTC, but with native yield. The accounting is clearer now too post-ETF approval.",
        ],
        "hims_healthcare": [
            "The drug gets the headlines. The infrastructure play is HIMS — telehealth rails for GLP-1 delivery. $725M revenue already, Novo Nordisk deal locked.",
            "HIMS isn't the drug maker, they're the delivery infrastructure. That's the picks and shovels play. When 50M Americans are on GLP-1s, who delivers them?",
            "This. Everyone focuses on Novo/Novo's drug. The real opportunity is the logistics layer — prescribing, monitoring, delivering. That's HIMS.",
        ],
        "ai_commerce": [
            "McKinsey says $3-5T in agentic commerce by 2030. The winners won't be LLM makers — they'll be the intelligence companies that own customer relationships.",
            "Exactly right. Infrastructure over models. NBIS for banking, PLTR for enterprise, ZETA for restaurant/retail. These are the picks and shovels.",
            "The timeline is key here — 2025 is infrastructure build phase. Position now before consumer adoption accelerates in 2027-2030.",
        ],
    }

class AutomationScheduler:
    """Schedule and execute automation tasks"""
    
    def __init__(self):
        self.system = None
        self.running = True
        
    async def run(self):
        """Main scheduler loop"""
        print("🤖 X Automation Scheduler Started")
        print("=" * 50)
        
        # Initialize system
        self.system = XAutomationSystem()
        await self.system.initialize(headless=True)
        
        # Ensure logged in
        logged_in = await self.system.login_if_needed()
        if not logged_in:
            print("❌ Login required. Please run in non-headless mode first.")
            return
        
        print("✅ Scheduler running. Press Ctrl+C to stop.")
        
        try:
            while self.running:
                await self.check_scheduled_tasks()
                await asyncio.sleep(60)  # Check every minute
        except KeyboardInterrupt:
            print("\n🛑 Stopping scheduler...")
        finally:
            await self.system.close()
    
    async def check_scheduled_tasks(self):
        """Check and execute scheduled tasks"""
        now = datetime.now()
        
        # Check if it's time for morning digest (8:00 AM)
        if now.hour == 8 and now.minute == 0:
            await self.morning_digest()
        
        # Check trend monitoring times (9:00, 13:00, 19:00)
        if now.hour in [9, 13, 19] and now.minute == 0:
            await self.trend_monitor()
        
        # Check posting times
        await self.check_posting_schedule()
        
        # Check engagement
        if now.hour == 9 and now.minute == 30:
            await self.engagement_round()
    
    async def morning_digest(self):
        """Generate and log morning digest"""
        print(f"\n📊 Morning Digest - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        # Get follower count
        followers = await self.system.get_follower_count()
        
        # Search for trending topics
        trends = await self.system.search_tweets("ETH treasury", count=5)
        
        # Log digest
        digest = {
            "date": datetime.now().isoformat(),
            "followers": followers,
            "trending_count": len(trends),
        }
        
        with open("automation_data/digests.json", "a") as f:
            f.write(json.dumps(digest) + "\n")
        
        print(f"✅ Digest logged: {followers} followers, {len(trends)} trending items")
    
    async def trend_monitor(self):
        """Monitor trends and log findings"""
        print(f"\n🔍 Trend Monitor - {datetime.now().strftime('%H:%M')}")
        
        topics = ["ETH treasury", "HIMS healthcare", "GLP-1", "AI agent", "agentic commerce"]
        
        for topic in topics:
            tweets = await self.system.search_tweets(topic, count=3)
            print(f"  {topic}: {len(tweets)} tweets found")
            await asyncio.sleep(1)  # Rate limiting
    
    async def check_posting_schedule(self):
        """Check if it's time to post"""
        now = datetime.now()
        day_name = now.strftime("%A")
        time_str = now.strftime("%H:%M")
        
        config = self.system.config
        
        # Check if it's a posting time
        if time_str not in config["posting_schedule"]["times"]:
            return
        
        # Check day type
        if day_name in config["posting_schedule"]["threads"]:
            await self.post_thread_content()
        elif day_name in config["posting_schedule"]["singles"]:
            await self.post_single_content()
    
    async def post_thread_content(self):
        """Post a thread based on content pillars"""
        print(f"\n📝 Posting thread...")
        
        # Select random thread type
        thread_type = random.choice(list(ContentLibrary.THREADS.keys()))
        thread_content = ContentLibrary.THREADS[thread_type]
        
        # Post thread
        success = await self.system.post_thread(thread_content)
        
        if success:
            # Log post
            log = {
                "date": datetime.now().isoformat(),
                "type": "thread",
                "topic": thread_type,
                "count": len(thread_content)
            }
            with open("automation_data/posts.json", "a") as f:
                f.write(json.dumps(log) + "\n")
    
    async def post_single_content(self):
        """Post a single tweet"""
        print(f"\n📝 Posting single tweet...")
        
        # This would pull from a content library
        # For now, placeholder
        content = f"Daily market update - testing automation system {datetime.now().strftime('%H:%M')}"
        
        success = await self.system.post_tweet(content)
        
        if success:
            log = {
                "date": datetime.now().isoformat(),
                "type": "single",
                "content": content[:50]
            }
            with open("automation_data/posts.json", "a") as f:
                f.write(json.dumps(log) + "\n")
    
    async def engagement_round(self):
        """Engage with target accounts"""
        print(f"\n💬 Engagement round...")
        
        targets = self.system.config["engagement_targets"]
        
        for target in targets[:2]:  # Limit to 2 per round
            # Search for recent tweets from target
            tweets = await self.system.search_tweets(f"from:{target}", count=1)
            
            if tweets:
                # Reply with template
                reply = random.choice(ContentLibrary.REPLIES.get("eth_treasury", ["Interesting perspective!"]))
                await self.system.reply_to_tweet(tweets[0]["url"], reply)
                await asyncio.sleep(30)  # Rate limiting

if __name__ == "__main__":
    scheduler = AutomationScheduler()
    asyncio.run(scheduler.run())
