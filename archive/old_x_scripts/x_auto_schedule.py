"""
X Account Auto-Posting Schedule
3 Posts/Day - No Replies - Fully Automated
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

# Schedule Configuration
SCHEDULE = {
    "account": "@quentinvest1",
    "posts_per_day": 3,
    "reply_policy": "none",  # No replies, only original content
    "posting_times": ["08:00", "14:00", "19:00"],  # Morning, afternoon, evening (Paris time)
    "content_rotation": [
        "eth_treasury",           # Morning: ETH/BTC treasury
        "hims_healthcare",        # Afternoon: Healthcare/HIMS
        "ai_agentic_commerce"     # Evening: AI/Commerce
    ],
    "posting_rules": {
        "min_chars": 100,
        "max_chars": 280,
        "include_hook": True,
        "include_cta": True,
        "hashtag_count": 3,
        "media": "optional"
    }
}

# Weekly Content Calendar
WEEKLY_CALENDAR = {
    "Monday": {
        "08:00": {"pillar": "eth_treasury", "type": "single", "focus": "institutional adoption"},
        "14:00": {"pillar": "hims_healthcare", "type": "single", "focus": "infrastructure play"},
        "19:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "market size"}
    },
    "Tuesday": {
        "08:00": {"pillar": "hims_healthcare", "type": "single", "focus": "revenue metrics"},
        "14:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "portfolio plays"},
        "19:00": {"pillar": "eth_treasury", "type": "single", "focus": "staking yield"}
    },
    "Wednesday": {
        "08:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "timeline predictions"},
        "14:00": {"pillar": "eth_treasury", "type": "single", "focus": "comparisons"},
        "19:00": {"pillar": "hims_healthcare", "type": "single", "focus": "GLP-1 disruption"}
    },
    "Thursday": {
        "08:00": {"pillar": "eth_treasury", "type": "single", "focus": "data point"},
        "14:00": {"pillar": "hims_healthcare", "type": "single", "focus": "competitive moat"},
        "19:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "investment thesis"}
    },
    "Friday": {
        "08:00": {"pillar": "hims_healthcare", "type": "single", "focus": "weekly recap"},
        "14:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "forward looking"},
        "19:00": {"pillar": "eth_treasury", "type": "single", "focus": "weekend read"}
    },
    "Saturday": {
        "08:00": {"pillar": "eth_treasury", "type": "single", "focus": "deep dive"},
        "14:00": {"pillar": "ai_agentic_commerce", "type": "single", "focus": "analysis"},
        "19:00": None  # Rest day
    },
    "Sunday": {
        "08:00": None,  # Rest day
        "14:00": {"pillar": "hims_healthcare", "type": "single", "focus": "prep for week"},
        "19:00": None  # Rest day
    }
}

# Pre-written posts for each pillar (21 posts = 1 week supply)
POST_TEMPLATES = {
    "eth_treasury": [
        {
            "hook": "The BTC treasury playbook is proven. The next evolution is earning yield while holding — that's where ETH treasuries come in.",
            "body": "3-4% staking APR changes the math for CFOs. 19 public companies now hold ETH ($13B+). The treasury strategy is evolving from passive holding to productive assets. Staking yield is the unlock.",
            "cta": "What do you think — will ETH treasuries follow the BTC playbook?"
        },
        {
            "hook": "Saylor had to sell $216M BTC to fund operations.",
            "body": "ETH treasuries won't have to. 3% yield on $100M = $3M annual income. Fund operations WITHOUT selling core holdings. The next generation of treasury strategy is productive assets.",
            "cta": "The CFO math changes completely when yield enters the equation."
        },
        {
            "hook": "MicroStrategy holds $50B+ in BTC. But they can't earn yield on it.",
            "body": "ETH treasuries offer the same store of value + 3-4% staking returns. That's $2M per year on $50M holdings. Passive income without selling your stack.",
            "cta": "Productive treasuries are coming."
        }
    ],
    "hims_healthcare": [
        {
            "hook": "The drug gets the headlines. The infrastructure play is HIMS.",
            "body": "Telehealth rails for GLP-1 delivery. $725M revenue already, Novo Nordisk deal locked. HIMS isn't just telehealth — it's the distribution infrastructure for the obesity revolution.",
            "cta": "Healthcare infrastructure or just another pharma play?"
        },
        {
            "hook": "GLP-1s are disrupting healthcare. HIMS owns the rails.",
            "body": "The Novo Nordisk deal (March 2026) changed everything. HIMS pivoted from compounded drugs to FDA-approved: Ozempic, Wegovy, Zepbound, Mounjaro. That's infrastructure being built for the long haul.",
            "cta": "The real play is bigger than the drug."
        },
        {
            "hook": "$2.35B revenue in 2025 (+59% YoY). 2.5M subscribers.",
            "body": "The numbers tell the story. HIMS isn't a weight loss company. It's healthcare infrastructure for the GLP-1 revolution. $83/month revenue per subscriber, up from $65. Growing ARPU, growing market.",
            "cta": "The infrastructure wins."
        }
    ],
    "ai_agentic_commerce": [
        {
            "hook": "McKinsey says $3-5T in agentic commerce by 2030.",
            "body": "The winners won't be LLM makers — they'll be the intelligence companies that own customer relationships. Agents need data to be useful. Incumbents with existing relationships (banks, retailers, SaaS) have the moat here.",
            "cta": "Which companies are positioning for the agentic economy?"
        },
        {
            "hook": "We're entering the agentic economy faster than most realize.",
            "body": "By 2027, agent-mediated transactions will be normalized. By 2030, table stakes. Portfolio positioning: NBIS, PLTR, ZETA — the infrastructure plays for agentic commerce.",
            "cta": "The $3-5T opportunity is coming."
        },
        {
            "hook": "Agents will handle 30% of e-commerce transactions by 2028.",
            "body": "Not just chatbots. Autonomous agents that research, compare, negotiate, and purchase on your behalf. The customer relationship layer is where value accumulates.",
            "cta": "The next platform shift is agentic."
        }
    ]
}

# Hashtags per pillar
HASHTAGS = {
    "eth_treasury": ["#ETH", "#Treasury", "#Crypto"],
    "hims_healthcare": ["#HIMS", "#Healthcare", "#GLP1"],
    "ai_agentic_commerce": ["#AI", "#Agents", "#Commerce"]
}

def generate_post(pillar: str, template_idx: int = 0) -> str:
    """Generate a complete post from template"""
    template = POST_TEMPLATES[pillar][template_idx % len(POST_TEMPLATES[pillar])]
    hashtags = " ".join(HASHTAGS[pillar])
    
    post = f"{template['hook']}\n\n{template['body']}\n\n{template['cta']}\n\n{hashtags}"
    
    # Ensure under 280 chars
    if len(post) > 280:
        post = f"{template['hook']}\n\n{template['cta']}\n\n{hashtags}"
    
    return post

def get_today_schedule() -> dict:
    """Get today's posting schedule"""
    today = datetime.now().strftime("%A")
    return WEEKLY_CALENDAR.get(today, {})

def save_schedule():
    """Save the schedule configuration"""
    config = {
        "schedule": SCHEDULE,
        "weekly_calendar": WEEKLY_CALENDAR,
        "post_templates": POST_TEMPLATES,
        "hashtags": HASHTAGS,
        "updated_at": datetime.now().isoformat()
    }
    
    output_path = Path("C:/Users/quent/.openclaw/workspace/operations/x_posting_schedule.json")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Schedule saved to {output_path}")

if __name__ == "__main__":
    save_schedule()
    
    # Show example posts
    print("\n" + "="*70)
    print("3 POSTS/DAY SCHEDULE - NO REPLIES")
    print("="*70)
    
    today_schedule = get_today_schedule()
    print(f"\nToday ({datetime.now().strftime('%A')}):")
    
    for time_slot, config in today_schedule.items():
        if config:
            print(f"\n🕐 {time_slot}")
            print(f"   Pillar: {config['pillar']}")
            print(f"   Focus: {config['focus']}")
            post = generate_post(config['pillar'])
            print(f"   Preview: {post[:80]}...")
        else:
            print(f"\n🕐 {time_slot} - REST")
    
    print("\n" + "="*70)
    print(f"Total: 18-19 posts per week | Reply policy: NONE")
    print("="*70)
