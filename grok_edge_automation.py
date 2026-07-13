#!/usr/bin/env python3
"""
Grok Automation with Microsoft Edge
Uses your logged-in Edge profile (X already authenticated)
"""

import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def automate_grok_edge():
    """Automate Grok using Microsoft Edge with your logged-in profile"""
    
    print("=" * 60)
    print("GROK AUTOMATION WITH MICROSOFT EDGE")
    print("=" * 60)
    print()
    
    # Edge executable path
    edge_exe = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    if not edge_exe.exists():
        edge_exe = Path("C:/Program Files/Microsoft/Edge/Application/msedge.exe")
    
    # User data directory (your Edge profile)
    user_data = Path("C:/Users/quent/AppData/Local/Microsoft/Edge/User Data")
    
    print(f"Edge: {edge_exe}")
    print(f"Profile: {user_data}")
    print()
    
    async with async_playwright() as p:
        print("Launching Edge with your profile...")
        print("(This should have your X login already)")
        print()
        
        # Connect to your actual Edge browser
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            executable_path=str(edge_exe) if edge_exe.exists() else None,
            headless=False,
            args=[
                '--start-maximized',
                '--no-first-run',
                '--no-default-browser-check',
            ]
        )
        
        print("Edge launched!")
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
        
        title = await page.title()
        print(f"Page title: {title}")
        print()
        
        # Check if logged in
        content = await page.content()
        
        if "Sign in" in content or "Log in" in content or "Sign in with X" in content:
            print("⚠️  Grok shows sign-in page")
            print("Your Edge profile may need to authorize Grok.")
            print()
            print("Please click 'Sign in with X' in the browser window.")
            print("This should auto-login since you're already logged into X.")
            print()
            print("Press Enter when logged in...")
            input()
            
            # Check again
            content = await page.content()
            if "Sign in" not in content:
                print("✅ Successfully logged into Grok!")
        else:
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
    asyncio.run(automate_grok_edge())
