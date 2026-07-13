#!/usr/bin/env python3
"""
Grok Automation - Cookie-Based
Uses saved cookies to access Grok
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def run_grok_research():
    """Run Grok research using saved cookies"""
    
    cookie_file = Path("C:/Users/quent/.openclaw/workspace/operations/grok_cookies.json")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        # Load cookies if they exist
        if cookie_file.exists():
            with open(cookie_file) as f:
                cookies = json.load(f)
            await context.add_cookies(cookies)
            print(f"Loaded {len(cookies)} cookies")
        
        page = await context.new_page()
        
        # Navigate to Grok
        print("Navigating to Grok...")
        await page.goto("https://grok.com")
        await page.wait_for_load_state("networkidle")
        
        # Check if logged in
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        if "login" in current_url.lower():
            print("\n⚠️  Not logged in. Please log in manually.")
            print("Press Enter when logged in...")
            input()
            
            # Save new cookies
            cookies = await context.cookies()
            with open(cookie_file, 'w') as f:
                json.dump(cookies, f, indent=2)
            print(f"Saved {len(cookies)} cookies")
        else:
            print("\n✅ Logged in! Ready for automation.")
        
        # Run research prompts
        prompts = [
            ("eth", "What's trending on X about ETH treasuries? Top 5 posts from last 24 hours."),
            ("hims", "Latest X sentiment on HIMS stock, GLP-1s, telehealth. Top posts from today."),
            ("ai", "X trends on AI agentic commerce, autonomous agents. Key developments today.")
        ]
        
        results = {}
        
        for topic, prompt in prompts:
            print(f"\n--- Running {topic.upper()} research ---")
            
            # Click on chat input (this will vary based on Grok's UI)
            # For now, we'll pause and let user run manually
            print(f"Prompt: {prompt}")
            print("Please paste this into Grok and run it...")
        
        print("\n\nPress Enter to close browser...")
        input()
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_grok_research())
