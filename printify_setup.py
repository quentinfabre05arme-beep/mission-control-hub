#!/usr/bin/env python3
"""
Printify POD Setup Automation
Uses Playwright to automate Printify web interface
"""
import asyncio
from playwright.async_api import async_playwright
import json
import os

async def setup_printify():
    """Automate Printify product creation"""
    
    async with async_playwright() as p:
        # Launch browser with user data dir for persistence
        browser = await p.chromium.launch_persistent_context(
            user_data_dir="./chrome_data",
            headless=False,  # Set to True for production
            args=['--disable-blink-features=AutomationControlled']
        )
        
        page = await browser.new_page()
        
        print("🚀 Navigating to Printify...")
        await page.goto("https://printify.com/app/stores")
        
        # Wait for page to load
        await page.wait_for_load_state('networkidle')
        
        # Check if logged in
        if "login" in page.url or await page.query_selector('input[type="email"]') is not None:
            print("⚠️  Need to log in to Printify")
            print("Please log in manually, then press Enter to continue...")
            input()  # Wait for manual login
        
        print(f"✅ Current URL: {page.url}")
        
        # Take screenshot to see current state
        await page.screenshot(path="printify_status.png")
        print("📸 Screenshot saved: printify_status.png")
        
        # Check if we can see the shop
        shop_element = await page.query_selector('text=Quentinvestdesign')
        if shop_element:
            print("✅ Shop found: Quentinvestdesign")
        else:
            print("⚠️  Shop not visible, may need to select it")
        
        # List available actions
        print("\n📋 Available actions:")
        print("1. Create new product")
        print("2. View existing products")
        print("3. Check shop settings")
        print("4. Exit")
        
        await browser.close()
        return True

if __name__ == "__main__":
    result = asyncio.run(setup_printify())
    exit(0 if result else 1)
