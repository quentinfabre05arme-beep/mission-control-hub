"""
Social Media Operations System - Engagement Pipeline
Phase 3: Engagement Workflow

Workflow: Monitor → Context Gathering → Draft Response → Approval Gate → Execute → Log
"""

import json
import re
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

sys.stdout.reconfigure(encoding='utf-8')

class EngagementType(Enum):
    REPLY = "reply"
    QUOTE = "quote"
    LIKE = "like"
    RETWEET = "retweet"
    DM = "dm"

@dataclass
class EngagementTarget:
    """Represents a target account for engagement"""
    handle: str
    name: str
    focus: str
    tier: int  # 1, 2, 3
    follower_count: int
    avg_engagement: float
    last_engaged: Optional[str] = None
    priority_score: float = 0.0
    notes: List[str] = field(default_factory=list)

@dataclass
class EngagementOpportunity:
    """Represents an opportunity to engage"""
    id: str
    target_handle: str
    target_post_url: Optional[str]
    post_content: str
    engagement_type: EngagementType
    suggested_reply: str
    context: Dict
    priority: str  # high, medium, low
    created_at: str
    status: str  # discovered, drafted, approved, executed, rejected
    template_used: Optional[str] = None

class EngagementPipeline:
    """
    Engagement Operations Pipeline
    
    Monitors targets, drafts replies, queues for approval, executes
    """
    
    def __init__(self, workspace_path: str = None):
        self.workspace = Path(workspace_path) if workspace_path else Path(__file__).parent
        self.targets_file = self.workspace / "operations" / "engagement_targets.json"
        self.opportunities_file = self.workspace / "operations" / "engagement_opportunities.json"
        self.templates_file = self.workspace / "operations" / "engagement_templates.json"
        
        # Ensure directories exist
        self.targets_file.parent.mkdir(parents=True, exist_ok=True)
        
        self.targets: Dict[str, EngagementTarget] = {}
        self.opportunities: Dict[str, EngagementOpportunity] = {}
        self.templates: Dict[str, Dict] = self._load_templates()
        
        self._load_targets()
        self._load_opportunities()
    
    def _load_templates(self) -> Dict[str, Dict]:
        """Load engagement reply templates"""
        default_templates = {
            "eth_treasury": {
                "strategy_sale": "The BTC treasury playbook is proven. The next evolution is earning yield while holding — that's where ETH treasuries come in. 3-4% staking APR changes the math for CFOs.",
                "microstrategy_evolution": "Saylor had to sell $216M BTC to fund operations. ETH treasuries with staking yield wouldn't face this dilemma — 3% on $100M = $3M annual income.",
                "institutional_adoption": "19 public companies now hold ETH ($13B+). The treasury strategy is evolving from passive holding to productive assets. Staking yield is the unlock."
            },
            "hims_healthcare": {
                "infrastructure_play": "Exactly right on the infrastructure play. HIMS isn't just telehealth — it's the rails for GLP-1 distribution at scale. The $725M revenue run rate proves it.",
                "regulatory_clarity": "The Novo Nordisk deal was the signal. HIMS pivoted from regulatory gray area to FDA-approved drugs. That's infrastructure being built for the long haul.",
                "picks_and_shovels": "The drug gets headlines. The infrastructure wins. HIMS owns the patient relationship, the logistics, the prescription flow. That's the durable moat."
            },
            "ai_agentic_commerce": {
                "mckinsey_thesis": "McKinsey's $3-5T by 2030 projection is directionally right. The winners won't be LLM makers — they'll be the companies that own customer relationships at scale.",
                "customer_relationships": "Agents need data to be useful. The incumbents with existing customer relationships (banks, retailers, SaaS) have the moat here.",
                "timeline_prediction": "We're entering the agentic economy faster than most realize. By 2027, agent-mediated transactions will be normalized. By 2030, table stakes."
            },
            "engagement_hooks": {
                "curiosity_open": "Interesting angle. What do you think about...",
                "agreement_build": "Exactly. And what's fascinating is...",
                "conviction_close": "This is the signal most are missing. The next 12 months will validate this thesis.",
                "data_point": "The numbers tell the story: {stat}",
                "question_pivot": "Great point. Have you considered {alternative_angle}?"
            }
        }
        
        if self.templates_file.exists():
            with open(self.templates_file, 'r', encoding='utf-8') as f:
                return {**default_templates, **json.load(f)}
        
        with open(self.templates_file, 'w', encoding='utf-8') as f:
            json.dump(default_templates, f, indent=2, ensure_ascii=False)
        
        return default_templates
    
    def _load_targets(self):
        """Load engagement targets from memory"""
        default_targets = [
            EngagementTarget("@TheLongInvestor", "The Long Investor", "ETH technical analysis, treasury plays", 1, 85000, 3.2),
            EngagementTarget("@DrTomsLens", "Dr Tom", "Healthcare/biotech, Data Awareness portfolio", 1, 45000, 4.1),
            EngagementTarget("@DylanLeClair_", "Dylan LeClair", "BTC analysis, market structure", 1, 120000, 5.8),
            EngagementTarget("@RaoulGMI", "Raoul Pal", "Macro, crypto, exponential age", 1, 1420000, 2.4),
            EngagementTarget("@DocumentingBTC", "Documenting Bitcoin", "BTC news, treasury tracking", 2, 580000, 1.8),
            EngagementTarget("@DeFi_Cheetah", "DeFi Cheetah", "DeFi analysis, ETH ecosystem", 2, 32000, 3.5),
            EngagementTarget("@HIMS_IR", "HIMS & Hers Health", "Official HIMS account", 2, 89000, 2.1),
            EngagementTarget("@naval", "Naval", "Tech, wealth, philosophy", 3, 2400000, 1.5),
            EngagementTarget("@pmarca", "Marc Andreessen", "VC, tech trends", 3, 1900000, 1.2),
        ]
        
        if self.targets_file.exists():
            with open(self.targets_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for item in data:
                    self.targets[item['handle']] = EngagementTarget(**item)
        else:
            for target in default_targets:
                self.targets[target.handle] = target
            self._save_targets()
    
    def _save_targets(self):
        """Save targets to disk"""
        data = []
        for target in self.targets.values():
            data.append({
                'handle': target.handle,
                'name': target.name,
                'focus': target.focus,
                'tier': target.tier,
                'follower_count': target.follower_count,
                'avg_engagement': target.avg_engagement,
                'last_engaged': target.last_engaged,
                'priority_score': target.priority_score,
                'notes': target.notes
            })
        
        with open(self.targets_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def _load_opportunities(self):
        """Load engagement opportunities"""
        if self.opportunities_file.exists():
            with open(self.opportunities_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for opp_id, opp_data in data.items():
                    opp_data['engagement_type'] = EngagementType(opp_data['engagement_type'])
                    self.opportunities[opp_id] = EngagementOpportunity(**opp_data)
    
    def _save_opportunities(self):
        """Save opportunities to disk"""
        data = {}
        for opp_id, opp in self.opportunities.items():
            opp_dict = {
                'id': opp.id,
                'target_handle': opp.target_handle,
                'target_post_url': opp.target_post_url,
                'post_content': opp.post_content,
                'engagement_type': opp.engagement_type.value,
                'suggested_reply': opp.suggested_reply,
                'context': opp.context,
                'priority': opp.priority,
                'created_at': opp.created_at,
                'status': opp.status,
                'template_used': opp.template_used
            }
            data[opp_id] = opp_dict
        
        with open(self.opportunities_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def discover_opportunity(self, target_handle: str, post_content: str,
                          post_url: str = None, context: Dict = None) -> EngagementOpportunity:
        """
        Discover and draft an engagement opportunity
        Workflow: Monitor → Context → Draft
        """
        if target_handle not in self.targets:
            print(f"[ENGAGEMENT] Unknown target: {target_handle}")
            return None
        
        target = self.targets[target_handle]
        
        # Determine priority based on target tier and content relevance
        priority = self._calculate_priority(target, post_content)
        
        # Draft reply using templates and context
        suggested_reply = self._draft_reply(target, post_content, context)
        
        # Create opportunity
        opp_id = f"eng_{self._slugify(target_handle)}_{int(datetime.now().timestamp())}"
        
        opportunity = EngagementOpportunity(
            id=opp_id,
            target_handle=target_handle,
            target_post_url=post_url,
            post_content=post_content[:500],  # Truncate for storage
            engagement_type=EngagementType.REPLY,
            suggested_reply=suggested_reply,
            context=context or {},
            priority=priority,
            created_at=datetime.now().isoformat(),
            status="drafted"
        )
        
        self.opportunities[opp_id] = opportunity
        self._save_opportunities()
        
        print(f"[ENGAGEMENT] Opportunity discovered: {opp_id} [{priority}] for {target_handle}")
        
        return opportunity
    
    def _calculate_priority(self, target: EngagementTarget, post_content: str) -> str:
        """Calculate priority based on target tier and content match"""
        score = 0
        
        # Tier bonus
        tier_bonus = {1: 30, 2: 20, 3: 10}
        score += tier_bonus.get(target.tier, 10)
        
        # Content relevance keywords
        keywords = {
            'eth': ['eth', 'ethereum', 'treasury', 'staking'],
            'hims': ['hims', 'glp-1', 'healthcare', 'telehealth', 'novo nordisk'],
            'ai': ['ai', 'agent', 'agentic', 'mckinsey', 'automation']
        }
        
        content_lower = post_content.lower()
        for category, words in keywords.items():
            if any(word in content_lower for word in words):
                score += 20
        
        # Engagement history (never engaged = higher priority)
        if target.last_engaged:
            days_since = (datetime.now() - datetime.fromisoformat(target.last_engaged)).days
            if days_since > 7:
                score += 15
        else:
            score += 20
        
        if score >= 60:
            return "high"
        elif score >= 40:
            return "medium"
        return "low"
    
    def _draft_reply(self, target: EngagementTarget, post_content: str, 
                    context: Dict) -> str:
        """Draft a reply using templates and context"""
        # Select template based on target focus
        templates = []
        
        if 'eth' in target.focus.lower() or 'treasury' in target.focus.lower():
            templates = self.templates.get('eth_treasury', {}).values()
        elif 'health' in target.focus.lower() or 'biotech' in target.focus.lower():
            templates = self.templates.get('hims_healthcare', {}).values()
        elif 'macro' in target.focus.lower() or 'crypto' in target.focus.lower():
            templates = self.templates.get('eth_treasury', {}).values()
        
        if not templates:
            templates = self.templates.get('engagement_hooks', {}).values()
        
        # Pick best template (in real implementation, would use LLM matching)
        import random
        base_reply = random.choice(list(templates)) if templates else "Interesting perspective. Thanks for sharing."
        
        return base_reply
    
    def _slugify(self, text: str) -> str:
        """Convert text to slug"""
        return re.sub(r'[^\w\s-]', '', text).strip().lower().replace(' ', '_')[:30]
    
    def queue_for_approval(self, opp_id: str) -> Dict:
        """Queue engagement for human approval"""
        if opp_id not in self.opportunities:
            raise ValueError(f"Opportunity {opp_id} not found")
        
        opp = self.opportunities[opp_id]
        opp.status = "awaiting_approval"
        self._save_opportunities()
        
        review_package = {
            "id": opp.id,
            "target": opp.target_handle,
            "type": opp.engagement_type.value,
            "priority": opp.priority,
            "original_post": opp.post_content[:200] + "..." if len(opp.post_content) > 200 else opp.post_content,
            "suggested_reply": opp.suggested_reply,
            "context": opp.context
        }
        
        print(f"[ENGAGEMENT] Queued for approval: {opp_id}")
        return review_package
    
    def approve_engagement(self, opp_id: str, approved_by: str = "human"):
        """Approve engagement for execution"""
        if opp_id not in self.opportunities:
            raise ValueError(f"Opportunity {opp_id} not found")
        
        opp = self.opportunities[opp_id]
        opp.status = "approved"
        self._save_opportunities()
        
        # Update target last engaged
        if opp.target_handle in self.targets:
            self.targets[opp.target_handle].last_engaged = datetime.now().isoformat()
            self._save_targets()
        
        print(f"[ENGAGEMENT] Approved: {opp_id} by {approved_by}")
    
    def execute_engagement(self, opp_id: str, dry_run: bool = True) -> Dict:
        """Execute approved engagement"""
        if opp_id not in self.opportunities:
            raise ValueError(f"Opportunity {opp_id} not found")
        
        opp = self.opportunities[opp_id]
        
        if opp.status != "approved":
            raise ValueError(f"Opportunity {opp_id} not approved")
        
        if dry_run:
            result = {
                "status": "dry_run",
                "action": f"Would reply to {opp.target_handle}",
                "content": opp.suggested_reply
            }
        else:
            # Here would call Zernio/X skills to actually post
            result = {
                "status": "executed",
                "action": f"Replied to {opp.target_handle}",
                "timestamp": datetime.now().isoformat()
            }
            opp.status = "executed"
            self._save_opportunities()
        
        return result
    
    def get_daily_engagement_plan(self) -> List[Dict]:
        """Generate daily engagement recommendations"""
        recommendations = []
        
        # Get tier 1 targets not engaged recently
        for handle, target in self.targets.items():
            if target.tier == 1:
                days_since = 999
                if target.last_engaged:
                    days_since = (datetime.now() - datetime.fromisoformat(target.last_engaged)).days
                
                if days_since >= 2:  # Don't engage same target within 2 days
                    recommendations.append({
                        "handle": handle,
                        "name": target.name,
                        "focus": target.focus,
                        "priority": "high" if days_since > 7 else "medium",
                        "reason": f"Tier 1 target, {days_since} days since last engagement"
                    })
        
        # Sort by priority
        recommendations.sort(key=lambda x: 0 if x['priority'] == 'high' else 1)
        
        return recommendations[:5]  # Top 5
    
    def list_pending_approvals(self) -> List[EngagementOpportunity]:
        """List all engagements awaiting approval"""
        return [opp for opp in self.opportunities.values() if opp.status == "awaiting_approval"]

if __name__ == "__main__":
    # Test engagement pipeline
    pipeline = EngagementPipeline("C:\\Users\\quent\\.openclaw\\workspace")
    
    # Test: Discover opportunity
    opp = pipeline.discover_opportunity(
        target_handle="@RaoulGMI",
        post_content="We're entering the economic singularity. Bitcoin becomes humanity's pension plan.",
        post_url="https://x.com/RaoulGMI/status/...",
        context={"topic": "economic_singularity", "sentiment": "bullish"}
    )
    
    if opp:
        # Queue for approval
        review = pipeline.queue_for_approval(opp.id)
        
        print("\n" + "="*60)
        print("ENGAGEMENT REVIEW PACKAGE")
        print("="*60)
        print(f"Target: {review['target']}")
        print(f"Type: {review['type']}")
        print(f"Priority: {review['priority'].upper()}")
        print(f"\nOriginal Post:\n{review['original_post'][:150]}...")
        print(f"\nSuggested Reply:\n{review['suggested_reply']}")
        print("="*60)
        print("\nStatus: AWAITING APPROVAL")
        print("Action: Review and approve to queue for posting")
        
        # Show daily plan
        print("\n" + "="*60)
        print("DAILY ENGAGEMENT RECOMMENDATIONS")
        print("="*60)
        for rec in pipeline.get_daily_engagement_plan():
            print(f"• {rec['handle']} ({rec['name']})")
            print(f"  Focus: {rec['focus']}")
            print(f"  Priority: {rec['priority']} | {rec['reason']}")
            print()
