#!/usr/bin/env python3
"""
Grok Browser Automation - Direct Playwright
Opens browser, navigates to Grok, ready for login
"""

import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def setup_grok_session():
    """Open browser and navigate to Grok"""
    
    print("Opening browser for Grok setup...")
    print("=" * 50)
    
    async with async_playwright() as p:
        # Launch browser with user profile to keep login
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(Path.home() / ".claw_grok_browser"),
            headless=False,  # Show browser so user can log in
            args=['--start-maximized']
        )
        
        page = await browser.new_page()
        
        # Navigate to Grok
        print("Navigating to grok.com...")
        await page.goto("https://grok.com")
        
        # Wait for page to load
        await page.wait_for_load_state("networkidle")
        
        print("\n" + "=" * 50)
        print("Browser opened!")
        print("\nPlease log into Grok if not already logged in.")
        print("Once logged in, close the browser and I'll save the session.")
        print("\nPress Enter when done...")
        input()
        
        # Check if logged in
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Save session info
        session_file = Path("C:/Users/quent/.openclaw/workspace/operations/grok_session.json")
        session_info = {
            "setup_date": str(asyncio.get_event_loop().time()),
            "url": current_url,
            "logged_in": "grok.com" in current_url and "login" not in current_url
        }
        
        with open(session_file, 'w') as f:
            json.dump(session_info, f, indent=2)
        
        print(f"\nSession saved to: {session_file}")
        
        await browser.close()
        print("Setup complete!")

if __name__ == "__main__":
    asyncio.run(setup_grok_session())
