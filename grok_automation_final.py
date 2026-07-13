#!/usr/bin/env python3
"""
Grok Automation - Direct Playwright with User Profile
Connects to your actual Chrome with all logins
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def automate_grok():
    """Automate Grok using your Chrome profile"""
    
    print("=" * 60)
    print("GROK AUTOMATION SYSTEM")
    print("=" * 60)
    print()
    
    # Chrome executable path
    chrome_exe = Path("C:/Program Files/Google/Chrome/Application/chrome.exe")
    if not chrome_exe.exists():
        chrome_exe = Path("C:/Program Files (x86)/Google/Chrome/Application/chrome.exe")
    
    # User data directory (your profile)
    user_data = Path("C:/Users/quent/AppData/Local/Google/Chrome/User Data")
    
    print(f"Chrome: {chrome_exe}")
    print(f"Profile: {user_data}")
    print()
    
    async with async_playwright() as p:
        print("Launching Chrome with your profile...")
        
        # Connect to your actual Chrome
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            executable_path=str(chrome_exe) if chrome_exe.exists() else None,
            headless=False,
            args=[
                '--start-maximized',
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )
        
        print("Chrome launched!")
        print()
        
        # Create new page
        page = await browser.new_page()
        
        # Navigate to Grok
        print("Navigating to grok.com...")
        await page.goto("https://grok.com")
        await page.wait_for_load_state("networkidle")
        
        # Check current state
        current_url = page.url
        print(f"Current URL: {current_url}")
        
        # Check if we need to log in
        title = await page.title()
        print(f"Page title: {title}")
        
        # Look for login button or chat interface
        content = await page.content()
        
        if "Sign in" in content or "Log in" in content:
            print()
            print("⚠️  Sign-in required")
            print("Your Chrome profile may not be logged into X.")
            print()
            print("To fix this:")
            print("1. Log into X in your regular Chrome browser")
            print("2. Then run this script again")
            print()
            print("Keeping browser open for manual login...")
            print("Press Ctrl+C to close")
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                pass
        else:
            print()
            print("✅ Successfully connected to Grok!")
            print("You should be logged in.")
            print()
            print("Ready for research automation.")
            print()
            print("Press Ctrl+C to close browser...")
            
            try:
                while True:
                    await asyncio.sleep(1)
            except KeyboardInterrupt:
                pass
        
        await browser.close()
        print("\nBrowser closed.")

if __name__ == "__main__":
    asyncio.run(automate_grok())
