#!/usr/bin/env python3
"""
Launch Chrome with actual user profile
"""

import asyncio
from playwright.async_api import async_playwright

async def launch_user_chrome():
    """Launch Chrome with user's actual profile"""
    
    from pathlib import Path
    
    # Your actual Chrome profile path
    user_data = Path("C:/Users/quent/AppData/Local/Google/Chrome/User Data")
    
    print(f"Launching Chrome with profile: {user_data}")
    
    async with async_playwright() as p:
        # Launch with your actual Chrome profile
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            headless=False,
            args=[
                '--start-maximized',
                '--no-first-run',
                '--no-default-browser-check'
            ]
        )
        
        page = await browser.new_page()
        
        # Navigate to Grok
        print("Going to grok.com...")
        await page.goto("https://grok.com")
        await page.wait_for_load_state("networkidle")
        
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Check if logged in
        content = await page.content()
        if "Sign in" in content or "login" in content.lower():
            print("\n⚠️  Grok shows sign-in page")
            print("You may need to log in.")
            print("\nPress Enter when ready...")
            input()
        else:
            print("\n✅ Grok loaded!")
            print("You should be logged in.")
        
        print("\nBrowser ready. Press Ctrl+C to close...")
        try:
            while True:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            pass
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(launch_user_chrome())
