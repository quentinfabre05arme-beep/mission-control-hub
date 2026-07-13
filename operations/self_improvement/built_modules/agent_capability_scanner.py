#!/usr/bin/env python3
"""
Agent Capability Scanner
Automatically scans workspace and suggests improvements
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any

class CapabilityScanner:
    """Scans Python files for patterns and improvement opportunities."""
    
    PATTERNS = {
        "reflection": ["review", "critic", "evaluate", "assess"],
        "tool_use": ["api", "request", "fetch", "search"],
        "planning": ["plan", "strategy", "roadmap", "steps"],
        "multi_agent": ["agent", "orchestrator", "coordinator"],
        "error_handling": ["try:", "except", "finally"],
        "logging": ["logging", "logger", "log."]
    }
    
    def __init__(self, workspace_dir: str = None):
        self.workspace = Path(workspace_dir) if workspace_dir else Path.cwd()
        self.findings = []
    
    def scan_file(self, file_path: Path) -> Dict[str, Any]:
        """Scan a single Python file for patterns."""
        try:
            content = file_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            
            result = {
                "file": str(file_path.relative_to(self.workspace)),
                "lines": len(lines),
                "patterns_found": {},
                "missing_patterns": [],
                "score": 0
            }
            
            # Check for patterns
            for pattern_name, keywords in self.PATTERNS.items():
                found = any(kw in content.lower() for kw in keywords)
                result["patterns_found"][pattern_name] = found
                if not found:
                    result["missing_patterns"].append(pattern_name)
            
            # Calculate score
            found_count = sum(1 for v in result["patterns_found"].values() if v)
            result["score"] = round((found_count / len(self.PATTERNS)) * 100, 1)
            
            return result
        except Exception as e:
            return {"file": str(file_path), "error": str(e)}
    
    def scan_workspace(self) -> List[Dict[str, Any]]:
        """Scan all Python files in workspace."""
        results = []
        for py_file in self.workspace.rglob("*.py"):
            if ".git" not in str(py_file):
                results.append(self.scan_file(py_file))
        return sorted(results, key=lambda x: x.get("score", 0))
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate markdown report."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        avg_score = sum(r.get("score", 0) for r in results) / len(results) if results else 0
        low_score = sum(1 for r in results if r.get("score", 0) < 50)
        
        report = f"""# Agent Capability Scan Report
**Generated:** {timestamp}
**Files Scanned:** {len(results)}

## Summary

| Metric | Value |
|--------|-------|
| Total Files | {len(results)} |
| Avg Score | {avg_score:.1f}% |
| Low Score Files | {low_score} |

## Files by Score

"""
        for r in results[:20]:
            if "error" not in r:
                report += f"- **{r['file']}**: {r['score']}% "
                if r.get("missing_patterns"):
                    report += f"(missing: {', '.join(r['missing_patterns'][:3])})"
                report += "\n"
        
        return report

if __name__ == "__main__":
    scanner = CapabilityScanner()
    results = scanner.scan_workspace()
    print(f"Scanned {len(results)} files")
    if results:
        avg = sum(r.get("score", 0) for r in results) / len(results)
        print(f"Average score: {avg:.1f}%")
