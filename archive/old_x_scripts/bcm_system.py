#!/usr/bin/env python3
"""
Brain-Coding-Muscles (BCM) System
Three-tier efficiency model for OpenClaw integration
"""

import json
import sys
from datetime import datetime
from pathlib import Path

class BCMSystem:
    """Brain-Coding-Muscles three-tier system"""
    
    def __init__(self):
        self.config = self._load_config()
        self.output_dir = Path("bcm_output")
        self.output_dir.mkdir(exist_ok=True)
    
    def _load_config(self):
        with open("brain_coding_muscles.json", 'r') as f:
            return json.load(f)
    
    def get_model_for_task(self, task_type):
        """Get optimal model for task type"""
        tier = self.config['tiers'].get(task_type, self.config['tiers']['muscles'])
        return tier['primary']
    
    def spawn_brain(self, task):
        """Spawn Brain-tier sub-agent for research/strategy"""
        model = self.get_model_for_task('brain')
        print(f"🧠 BRAIN: Spawning sub-agent with {model}")
        print(f"   Task: {task}")
        print(f"   Cost: HIGH - Use for complex analysis only")
        
        # Generate command for user
        cmd = f'sessions_spawn(task="{task}", model="ollama-cloud/{model}:cloud", context="fork")'
        print(f"\n   Command: {cmd}")
        return model
    
    def spawn_coding(self, task):
        """Spawn Coding-tier sub-agent for development"""
        model = self.get_model_for_task('coding')
        print(f"💻 CODING: Spawning sub-agent with {model}")
        print(f"   Task: {task}")
        print(f"   Cost: MEDIUM - Development work")
        
        cmd = f'sessions_spawn(task="{task}", model="ollama-cloud/{model}:cloud")'
        print(f"\n   Command: {cmd}")
        return model
    
    def spawn_muscles(self, task):
        """Spawn Muscles-tier sub-agent for execution"""
        model = self.get_model_for_task('muscles')
        print(f"💪 MUSCLES: Spawning sub-agent with {model}")
        print(f"   Task: {task}")
        print(f"   Cost: LOW - Fast execution")
        
        cmd = f'sessions_spawn(task="{task}", model="ollama-cloud/{model}:cloud")'
        print(f"\n   Command: {cmd}")
        return model
    
    def route_task(self, description):
        """Auto-route task to appropriate tier"""
        desc_lower = description.lower()
        
        # Brain indicators
        if any(kw in desc_lower for kw in ['research', 'analyze', 'strategy', 'plan', 'deep', 'complex', 'investigate']):
            return self.spawn_brain(description)
        
        # Coding indicators
        elif any(kw in desc_lower for kw in ['code', 'build', 'develop', 'website', 'app', 'program', 'script', 'api']):
            return self.spawn_coding(description)
        
        # Muscles default
        else:
            return self.spawn_muscles(description)
    
    def workflow_daily(self):
        """Daily workflow orchestration"""
        print("=" * 50)
        print("🔄 BCM DAILY WORKFLOW")
        print("=" * 50)
        print()
        print("MORNING (Brain + Coding):")
        print("  1. Research market trends → BRAIN")
        print("  2. Plan content strategy → BRAIN")
        print("  3. Build automation tools → CODING")
        print()
        print("AFTERNOON (Muscles):")
        print("  4. Execute social posts → MUSCLES")
        print("  5. Reply to mentions → MUSCLES")
        print("  6. Sales outreach → MUSCLES")
        print()
        print("EVENING (Brain):")
        print("  7. Review analytics → BRAIN")
        print("  8. Plan tomorrow → BRAIN")
        print()
        print("Cost Optimization:")
        print("  - 80% of tasks → MUSCLES (low cost)")
        print("  - 15% of tasks → CODING (medium cost)")
        print("  - 5% of tasks → BRAIN (high cost)")
    
    def cost_report(self):
        """Generate cost efficiency report"""
        report = f"""# BCM Cost Report

**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M")}

## Tier Costs (Ollama Cloud Pro)

| Tier | Model | Relative Cost | Best Use |
|------|-------|---------------|----------|
| 🧠 Brain | deepseek-v4-pro | 4x | Research, strategy |
| 💻 Coding | kimi-k2.7-code | 2x | Development |
| 💪 Muscles | kimi-k2.5 | 1x | Content, execution |

## Efficiency Formula

- **$20/month budget**
- Target: 80% muscles, 15% coding, 5% brain
- Est. daily tokens: ~50K muscles, ~10K coding, ~5K brain

## Quick Commands

```bash
# Brain (high cost, high value)
python bcm_system.py brain "Analyze ETH treasury trends"

# Coding (medium cost)
python bcm_system.py coding "Build website scraper"

# Muscles (low cost, high volume)
python bcm_system.py muscles "X thread about BTC"

# Auto-route
python bcm_system.py auto "Task description here"
```
"""
        
        filepath = self.output_dir / f"cost_report_{datetime.now().strftime('%Y%m%d')}.md"
        filepath.write_text(report, encoding='utf-8')
        print(f"Report saved: {filepath}")
        return str(filepath)
    
    def help(self):
        return """
Brain-Coding-Muscles (BCM) System

USAGE:
    python bcm_system.py <command> [args]

COMMANDS:
    brain <task>        - High-reasoning research/strategy
    coding <task>       - Development and technical work
    muscles <task>      - Fast execution and content
    auto <task>         - Auto-route based on task description
    workflow            - Show daily workflow
    cost                - Generate cost efficiency report
    help                - Show this help

EXAMPLES:
    python bcm_system.py brain "Research AI agent market size 2024"
    python bcm_system.py coding "Create Python script to scrape X data"
    python bcm_system.py muscles "Generate X thread about ETH staking"
    python bcm_system.py auto "Build a landing page for my service"
    python bcm_system.py workflow
    python bcm_system.py cost

TIER DESCRIPTIONS:
    🧠 Brain    - Deep reasoning, expensive, use sparingly
    💻 Coding   - Technical implementation, moderate cost
    💪 Muscles  - Fast execution, cheap, use for volume

COST OPTIMIZATION:
    - 80% of tasks → Muscles
    - 15% of tasks → Coding  
    - 5% of tasks → Brain
"""

def main():
    # Fix Windows encoding
    import sys
    if sys.platform == 'win32':
        sys.stdout.reconfigure(encoding='utf-8')
    
    bcm = BCMSystem()
    
    if len(sys.argv) < 2:
        print(bcm.help())
        return
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "brain":
        if not args:
            print("Usage: brain <task_description>")
            return
        bcm.spawn_brain(" ".join(args))
    
    elif command == "coding":
        if not args:
            print("Usage: coding <task_description>")
            return
        bcm.spawn_coding(" ".join(args))
    
    elif command == "muscles":
        if not args:
            print("Usage: muscles <task_description>")
            return
        bcm.spawn_muscles(" ".join(args))
    
    elif command == "auto":
        if not args:
            print("Usage: auto <task_description>")
            return
        bcm.route_task(" ".join(args))
    
    elif command == "workflow":
        bcm.workflow_daily()
    
    elif command == "cost":
        bcm.cost_report()
    
    elif command in ["help", "-h", "--help"]:
        print(bcm.help())
    
    else:
        print(f"Unknown command: {command}")
        print(bcm.help())

if __name__ == "__main__":
    main()
