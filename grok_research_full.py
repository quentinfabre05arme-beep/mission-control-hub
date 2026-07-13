#!/usr/bin/env python3
"""
Grok Research Automation - Full Workflow
Runs research prompts and captures results
"""

import asyncio
import json
from datetime import datetime
from pathlib import Path
from playwright.async_api import async_playwright

async def run_grok_research():
    """Full Grok research automation"""
    
    print("=" * 60)
    print("GROK RESEARCH AUTOMATION")
    print("=" * 60)
    print()
    
    # Setup paths
    edge_exe = Path("C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
    user_data = Path("C:/Users/quent/AppData/Local/Microsoft/Edge/User Data")
    output_dir = Path("C:/Users/quent/.openclaw/workspace/operations/grok_research")
    output_dir.mkdir(exist_ok=True)
    
    async with async_playwright() as p:
        print("Launching Edge...")
        browser = await p.chromium.launch_persistent_context(
            user_data_dir=str(user_data),
            executable_path=str(edge_exe) if edge_exe.exists() else None,
            headless=False,
            args=['--start-maximized', '--no-first-run']
        )
        
        # Get existing pages or create new
        pages = browser.pages
        if pages:
            page = pages[0]
            print(f"Using existing page: {page.url}")
        else:
            page = await browser.new_page()
        
        # Navigate to Grok
        print("Navigating to Grok...")
        await page.goto("https://grok.com")
        await page.wait_for_load_state("networkidle")
        
        # Check if logged in
        print("Checking login status...")
        await asyncio.sleep(2)  # Wait for page to fully load
        
        # Check for chat input (means logged in)
        try:
            chat_input = await page.wait_for_selector('textarea, [placeholder*="Ask"], [contenteditable="true"]', timeout=5000)
            print("✅ Logged in to Grok!")
            logged_in = True
        except:
            print("⚠️  May need to log in. Looking for sign-in button...")
            logged_in = False
            
            # Try to click sign in
            try:
                sign_in = await page.wait_for_selector('text=Sign in, button:has-text("Sign in"), [data-testid*="signin"]', timeout=3000)
                if sign_in:
                    print("Clicking Sign in...")
                    await sign_in.click()
                    await asyncio.sleep(3)
                    print("Please complete login manually, then press Enter here...")
                    input()
            except:
                print("No sign-in button found. Assuming logged in or anonymous mode.")
        
        if not logged_in:
            print("\nCannot proceed without login. Exiting.")
            await browser.close()
            return
        
        # Research prompts
        prompts = [
            ("eth_treasury", "What's trending on X about ETH treasuries and institutional adoption? Show me the top 5 most engaged posts from the last 24 hours with specific numbers and data."),
            ("hims_healthcare", "Latest X sentiment on HIMS stock, GLP-1 developments, and telehealth infrastructure. Top posts from today with any price targets or analyst calls."),
            ("ai_commerce", "X trends on AI agentic commerce, autonomous agents, and infrastructure plays like NBIS, ZETA, PLTR. Key developments from the last 24 hours.")
        ]
        
        results = {}
        
        for topic, prompt in prompts:
            print(f"\n{'='*60}")
            print(f"Researching: {topic.upper()}")
            print('='*60)
            
            # Find chat input
            try:
                input_box = await page.wait_for_selector('textarea, [contenteditable="true"]', timeout=5000)
                
                # Clear existing text
                await input_box.click()
                await input_box.fill("")
                
                # Type prompt
                print(f"Prompt: {prompt[:80]}...")
                await input_box.fill(prompt)
                
                # Submit (usually Enter key)
                await input_box.press("Enter")
                
                # Wait for response
                print("Waiting for Grok response...")
                await asyncio.sleep(15)  # Wait for response
                
                # Capture response
                try:
                    # Look for response content
                    response_selector = '[data-testid="conversation-turn"]'
                    responses = await page.query_selector_all(response_selector)
                    if responses:
                        last_response = responses[-1]
                        response_text = await last_response.inner_text()
                        results[topic] = {
                            "prompt": prompt,
                            "response": response_text[:2000],  # First 2000 chars
                            "timestamp": datetime.now().isoformat()
                        }
                        print(f"✅ Captured response ({len(response_text)} chars)")
                    else:
                        results[topic] = {"error": "No response found", "prompt": prompt}
                except Exception as e:
                    results[topic] = {"error": str(e), "prompt": prompt}
                    print(f"❌ Error capturing response: {e}")
                
            except Exception as e:
                print(f"❌ Error interacting with chat: {e}")
                results[topic] = {"error": str(e), "prompt": prompt}
            
            # Wait between prompts
            await asyncio.sleep(5)
        
        # Save results
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_file = output_dir / f"grok_research_{timestamp}.json"
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"\n{'='*60}")
        print(f"✅ Research complete!")
        print(f"Results saved to: {output_file}")
        print('='*60)
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(run_grok_research())
