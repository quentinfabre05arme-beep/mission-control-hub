#!/usr/bin/env python3
"""
Grok X Research Module
Uses xAI API to search X/Twitter and analyze content
"""

import os
import json
import requests
from datetime import datetime
from typing import List, Dict, Optional

class GrokXResearcher:
    """Research X using Grok's real-time capabilities via xAI API"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('XAI_API_KEY')
        if not self.api_key:
            raise ValueError("xAI API key required. Set XAI_API_KEY environment variable.")
        
        self.base_url = "https://api.x.ai/v1"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
    
    def search_x(self, query: str, max_results: int = 10) -> Dict:
        """Search X/Twitter using Grok's real-time search"""
        
        prompt = f"""Search X (Twitter) for recent posts about: {query}

Find the {max_results} most relevant and recent posts from the last 24-48 hours.
For each post, provide:
1. Author (@username)
2. Post text (summary if long)
3. Engagement (likes, reposts if available)
4. Timestamp
5. Key insight or takeaway

Format as JSON list with these fields: author, text, engagement, time, insight"""

        response = self._call_grok(prompt, enable_search=True)
        return self._parse_search_results(response, query)
    
    def analyze_trend(self, topic: str) -> Dict:
        """Analyze trending narrative around a topic on X"""
        
        prompt = f"""Analyze the current narrative and sentiment on X (Twitter) about: {topic}

Provide:
1. Overall sentiment (bullish/bearish/neutral)
2. Key narratives being discussed
3. Notable accounts mentioning this
4. Volume of discussion (high/medium/low)
5. Most compelling data point or claim
6. Counter-arguments or skeptics
7. Investment thesis implications

Be specific with numbers, dates, and sources when available."""

        response = self._call_grok(prompt, enable_search=True)
        return {
            "topic": topic,
            "analysis": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_market_insights(self, tickers: List[str]) -> Dict:
        """Get real-time market insights for tickers"""
        
        prompt = f"""What are X (Twitter) traders and analysts saying right now about: {', '.join(tickers)}

Focus on:
- Breaking news or developments
- Institutional activity
- Technical analysis calls
- Unusual options flow mentions
- Smart money moves
- Earnings or catalyst discussions

Format as actionable intelligence with confidence levels."""

        response = self._call_grok(prompt, enable_search=True)
        return {
            "tickers": tickers,
            "insights": response,
            "timestamp": datetime.now().isoformat()
        }
    
    def generate_content_ideas(self, pillar: str, research_data: Dict) -> List[Dict]:
        """Generate post ideas based on research"""
        
        prompt = f"""Based on this research about {pillar}, generate 3 high-engagement post ideas:

Research Context:
{json.dumps(research_data, indent=2)}

For each post idea:
1. Hook (first line that stops the scroll)
2. Body (2-4 sentences with data/thesis)
3. Format (thread, single post, or poll)
4. Best time to post
5. Expected engagement level
6. Counter-argument to address

Make it authentic, thesis-driven, and high-signal. No clickbait."""

        response = self._call_grok(prompt, enable_search=False)
        return self._parse_content_ideas(response, pillar)
    
    def _call_grok(self, prompt: str, model: str = "grok-4.3", enable_search: bool = True) -> str:
        """Call xAI Responses API with prompt"""
        
        url = f"{self.base_url}/responses"
        
        data = {
            "model": model,
            "input": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Add web search tool if enabled
        if enable_search:
            data["tools"] = [
                {
                    "type": "web_search"
                }
            ]
        
        try:
            response = requests.post(url, headers=self.headers, json=data, timeout=60)
            response.raise_for_status()
            result = response.json()
            
            # Extract text from response structure
            if 'output_text' in result:
                return result['output_text']
            elif 'output' in result and len(result['output']) > 0:
                # Handle content blocks
                for block in result['output']:
                    if block.get('type') == 'message':
                        content = block.get('content', [])
                        if content and len(content) > 0:
                            return content[0].get('text', str(content))
                return str(result['output'])
            else:
                return str(result)
                
        except Exception as e:
            print(f"Error calling Grok API: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}")
            return f"Error: {str(e)}"
    
    def _parse_search_results(self, response: str, query: str) -> Dict:
        """Parse Grok search response into structured data"""
        
        return {
            "query": query,
            "results": response,
            "timestamp": datetime.now().isoformat(),
            "source": "grok_x_search"
        }
    
    def _parse_content_ideas(self, response: str, pillar: str) -> List[Dict]:
        """Parse content ideas from Grok response"""
        
        return [{
            "pillar": pillar,
            "ideas": response,
            "generated_at": datetime.now().isoformat()
        }]


def run_daily_research():
    """Run full daily research cycle"""
    
    api_key = os.getenv('XAI_API_KEY')
    if not api_key:
        print("Error: Set XAI_API_KEY environment variable")
        return
    
    researcher = GrokXResearcher(api_key)
    
    # Research our 3 content pillars
    pillars = [
        ("ETH Treasury", ["ETH", "Ethereum", "Bitmine", "staking yield"]),
        ("HIMS Healthcare", ["HIMS", "GLP-1", "telehealth", "JPMorgan facility"]),
        ("AI Agentic Commerce", ["AI agents", "MCP protocol", "A2A", "agentic commerce"])
    ]
    
    results = {}
    
    for pillar_name, keywords in pillars:
        print(f"\n{'='*60}")
        print(f"Researching: {pillar_name}")
        print('='*60)
        
        # Search X for recent posts
        query = ' OR '.join(keywords)
        search_results = researcher.search_x(query, max_results=10)
        
        # Analyze trend
        trend_analysis = researcher.analyze_trend(pillar_name)
        
        # Generate content ideas
        ideas = researcher.generate_content_ideas(pillar_name, {
            "search": search_results,
            "trend": trend_analysis
        })
        
        results[pillar_name] = {
            "search": search_results,
            "trend": trend_analysis,
            "ideas": ideas
        }
        
        print("[OK] Search complete")
        print("[OK] Trend analysis complete")
        print("[OK] Content ideas generated")
    
    # Save results
    os.makedirs('operations/research', exist_ok=True)
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    output_file = f'operations/research/grok_research_{timestamp}.json'
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\n{'='*60}")
    print(f"Research complete! Saved to: {output_file}")
    print('='*60)
    
    return results


if __name__ == '__main__':
    run_daily_research()
