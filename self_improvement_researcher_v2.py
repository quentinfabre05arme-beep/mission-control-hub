#!/usr/bin/env python3
"""
Self-Improvement Research System - v2 (Functional)
Performs actual web research and generates actionable findings
"""

import os
import json
import requests
import sys
from datetime import datetime

# Fix encoding for Windows
sys.stdout.reconfigure(encoding='utf-8')

SERPER_API_KEY = "1a32d04a8215dde72b67e554c94409ce580094f3"
SERPER_URL = "https://google.serper.dev/search"

def clean_text(text: str) -> str:
    """Clean text for safe console output"""
    if not text:
        return ""
    # Replace problematic unicode chars with ASCII equivalents
    replacements = {
        '\u2011': '-',  # non-breaking hyphen
        '\u2013': '-',  # en dash
        '\u2014': '-',  # em dash
        '\u2018': "'",  # left single quote
        '\u2019': "'",  # right single quote
        '\u201c': '"',  # left double quote
        '\u201d': '"',  # right double quote
        '\u2026': '...', # ellipsis
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text

def web_search(query: str, count: int = 5) -> list:
    """Search web using Serper.dev API"""
    try:
        headers = {"X-API-KEY": SERPER_API_KEY, "Content-Type": "application/json"}
        payload = {"q": query, "num": count}
        response = requests.post(SERPER_URL, json=payload, headers=headers, timeout=15)
        data = response.json()
        
        results = []
        for r in data.get("organic", [])[:count]:
            results.append({
                "title": clean_text(r.get("title", "")),
                "link": r.get("link", ""),
                "snippet": clean_text(r.get("snippet", ""))
            })
        return results
    except Exception as e:
        return [{"error": str(e)}]

def check_dashboard_status(url: str) -> dict:
    """Check if dashboard is accessible"""
    try:
        resp = requests.get(url, timeout=10, allow_redirects=True)
        return {"url": url, "status": resp.status_code, "accessible": resp.status_code == 200}
    except Exception as e:
        return {"url": url, "status": 0, "accessible": False, "error": str(e)}

def research_topic(topic: str, queries: list) -> dict:
    """Research a topic with multiple queries"""
    findings = []
    for q in queries:
        results = web_search(q, count=3)
        findings.extend(results)
    
    return {
        "topic": topic,
        "queries": queries,
        "findings": findings,
        "timestamp": datetime.now().isoformat()
    }

def generate_research_report() -> dict:
    """Generate actual research report with live data"""
    
    # Research topics
    ai_research = research_topic(
        "AI Agent Capabilities 2025",
        ["AI agent frameworks 2025", "autonomous AI tools latest", "AI automation trends July 2026"]
    )
    
    content_research = research_topic(
        "Content Creation & Social Media",
        ["X Twitter algorithm 2026", "social media content strategy 2026", "Twitter engagement tactics"]
    )
    
    automation_research = research_topic(
        "Automation Best Practices",
        ["workflow automation tools 2026", "cron job best practices", "productivity automation AI"]
    )
    
    # Check dashboard status
    dashboards = [
        "https://mission-control-hub-lovat.vercel.app",
        "https://mission-control-hub-lovat.vercel.app/mission_control/index.html",
        "https://mission-control-hub-lovat.vercel.app/mission_control_risk_management.html"
    ]
    
    dashboard_status = [check_dashboard_status(d) for d in dashboards]
    
    report = {
        "generated_at": datetime.now().strftime('%Y-%m-%d %H:%M %Z'),
        "timezone": "Europe/Paris",
        "research_topics": [ai_research, content_research, automation_research],
        "dashboard_status": dashboard_status,
        "next_actions": [
            "Review top 3 AI frameworks found for integration potential",
            "Analyze content strategies for X growth (currently 219 followers)",
            "Update dashboard routing fix (vercel.json pending deploy)",
            "Implement automated posting workflow with manual approval gate"
        ]
    }
    
    return report

if __name__ == '__main__':
    print("=== Self-Improvement Research v2 ===")
    print("Running live research queries...\n")
    
    report = generate_research_report()
    
    print(f"Generated: {report['generated_at']}")
    print(f"Timezone: {report['timezone']}\n")
    
    print("--- RESEARCH FINDINGS ---")
    for topic in report['research_topics']:
        print(f"\n[{topic['topic']}]")
        for finding in topic['findings'][:3]:  # Show top 3
            if 'title' in finding:
                print(f"  - {finding['title']}")
                snippet = finding.get('snippet', '')
                if snippet:
                    print(f"    {snippet[:120]}...")
            else:
                print(f"  - Error: {finding.get('error', 'Unknown')}")
    
    print("\n--- DASHBOARD STATUS ---")
    for dash in report['dashboard_status']:
        status = "OK" if dash['accessible'] else "FAIL"
        print(f"  [{status}] {dash['url']} (HTTP {dash['status']})")
    
    print("\n--- NEXT ACTIONS ---")
    for i, action in enumerate(report['next_actions'], 1):
        print(f"  {i}. {action}")
    
    print("\n=== END REPORT ===")
    
    # Save to file for later use
    with open('research_output_latest.json', 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2)
    print("\nFull report saved to: research_output_latest.json")