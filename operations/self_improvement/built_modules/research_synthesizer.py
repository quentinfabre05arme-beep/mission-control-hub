#!/usr/bin/env python3
"""
Research Synthesis Engine
Combines multiple research outputs into actionable briefs
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class ResearchSynthesizer:
    """Synthesizes research from multiple sources into actionable outputs."""
    
    def __init__(self, research_dir: str = None):
        self.research_dir = Path(research_dir) if research_dir else Path("operations/self_improvement")
        self.outputs = []
    
    def load_research_files(self) -> List[Dict]:
        """Load all research JSON files."""
        findings = []
        if self.research_dir.exists():
            for json_file in self.research_dir.glob("*.json"):
                try:
                    with open(json_file, "r") as f:
                        data = json.load(f)
                        findings.append({
                            "source": json_file.name,
                            "data": data
                        })
                except:
                    pass
        return findings
    
    def synthesize(self, findings: List[Dict]) -> Dict[str, Any]:
        """Synthesize findings into actionable brief."""
        synthesis = {
            "generated_at": datetime.now().isoformat(),
            "sources_count": len(findings),
            "key_themes": [],
            "action_items": [],
            "priority_matrix": {
                "high_impact_low_effort": [],
                "high_impact_high_effort": [],
                "low_impact_low_effort": [],
                "low_impact_high_effort": []
            }
        }
        
        # Extract themes
        for finding in findings:
            if "research_tasks" in finding["data"]:
                for task in finding["data"]["research_tasks"]:
                    if task.get("priority") == "high":
                        synthesis["priority_matrix"]["high_impact_high_effort"].append(
                            task.get("query", "Unknown")
                        )
        
        return synthesis
    
    def generate_brief(self, synthesis: Dict) -> str:
        """Generate executive brief."""
        quick_wins = synthesis["priority_matrix"]["high_impact_low_effort"]
        strategic = synthesis["priority_matrix"]["high_impact_high_effort"]
        
        brief = f"""# Research Synthesis Brief
**Generated:** {synthesis["generated_at"]}
**Sources:** {synthesis["sources_count"]}

## Priority Matrix

### Quick Wins (High Impact, Low Effort)
"""
        if quick_wins:
            for item in quick_wins[:5]:
                brief += f"- {item}\n"
        else:
            brief += "- No quick wins identified\n"
        
        brief += """
### Strategic Investments (High Impact, High Effort)
"""
        if strategic:
            for item in strategic[:5]:
                brief += f"- {item}\n"
        else:
            brief += "- No strategic items identified\n"
        
        brief += """
## Recommended Actions
1. Focus on quick wins first
2. Plan strategic investments for next quarter
3. Review low-priority items monthly
"""
        return brief

if __name__ == "__main__":
    synthesizer = ResearchSynthesizer()
    findings = synthesizer.load_research_files()
    print(f"Loaded {len(findings)} research files")
    if findings:
        synthesis = synthesizer.synthesize(findings)
        print(synthesizer.generate_brief(synthesis))
