#!/usr/bin/env python3
"""
Grok Browser - Fresh Profile
Creates new browser session, navigates to Grok
"""

import asyncio
from playwright.async_api import async_playwright

async def launch_fresh_browser():
    """Launch fresh browser for Grok"""
    
    print("Launching fresh browser for Grok...")
    print("=" * 50)
    
    async with async_playwright() as p:
        # Launch fresh browser (not persistent context)
        browser = await p.chromium.launch(
            headless=False,
            args=['--start-maximized']
        )
        
        context = await browser.new_context(
            viewport={'width': 1920, 'height': 1080}
        )
        
        page = await context.new_page()
        
        # Navigate to Grok
        print("Navigating to grok.com...")
        await page.goto("https://grok.com")
        
        # Wait for page
        await page.wait_for_load_state("networkidle")
        
        print("\n" + "=" * 50)
        print("Browser opened!")
        print("\nPlease log into Grok.")
        print("Once logged in, I'll save the session cookies.")
        print("\nPress Enter when you're logged in to Grok...")
        input()
        
        # Save cookies
        cookies = await context.cookies()
        print(f"\nCaptured {len(cookies)} cookies")
        
        # Save to file
        import json
        from pathlib import Path
        
        cookie_file = Path("C:/Users/quent/.openclaw/workspace/operations/grok_cookies.json")
        with open(cookie_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        
        print(f"Cookies saved to: {cookie_file}")
        
        # Keep browser open for automation
        print("\nBrowser will stay open. Press Ctrl+C to close...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        
        await browser.close()
        print("\nDone!")

if __name__ == "__main__":
    asyncio.run(launch_fresh_browser())
