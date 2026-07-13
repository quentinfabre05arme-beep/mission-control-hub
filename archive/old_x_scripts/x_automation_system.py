#!/usr/bin/env python3
"""
X/Twitter Full Automation System
Using Playwright for browser automation - no API needed
"""

import asyncio
import json
import os
import random
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, List, Dict

from playwright.async_api import async_playwright, Page, Browser, BrowserContext

# Configuration
CONFIG_FILE = "automation_config.json"
DATA_DIR = Path("automation_data")
DATA_DIR.mkdir(exist_ok=True)

class XAutomationSystem:
    def __init__(self):
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
        self.config = self._load_config()
        
    def _load_config(self) -> dict:
        """Load configuration from file"""
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                return json.load(f)
        return {
            "account": "quentinvest1",
            "target_followers": 10000,
            "current_followers": 212,
            "content_pillars": [
                "ETH Treasury Reserves",
                "HIMS Healthcare Infrastructure", 
                "AI Agentic Commerce"
            ],
            "posting_schedule": {
                "threads": ["Monday", "Tuesday", "Wednesday"],
                "singles": ["Thursday", "Friday", "Saturday", "Sunday"],
                "times": ["08:00", "13:00", "19:00"]
            },
            "engagement_targets": [
                "TheLongInvestor",
                "DrTomsLens",
                "DylanLeClair_",
                "RaoulGMI"
            ]
        }
    
    async def initialize(self, headless: bool = False):
        """Initialize browser with user profile"""
        self.playwright = await async_playwright().start()
        
        # Launch Chrome with user's actual profile
        chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
        user_data_dir = Path.home() / "AppData" / "Local" / "Google" / "Chrome" / "User Data"
        
        if headless:
            # Headless mode - use persistent context
            profile_dir = DATA_DIR / "chrome_profile"
            profile_dir.mkdir(exist_ok=True)
            
            self.context = await self.playwright.chromium.launch_persistent_context(
                str(profile_dir),
                headless=True,
                viewport={"width": 1280, "height": 800},
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            )
        else:
            # Visible mode - connect to user's Chrome
            try:
                self.browser = await self.playwright.chromium.launch(
                    executable_path=chrome_path,
                    headless=False,
                    args=[f"--user-data-dir={user_data_dir}"]
                )
                self.context = await self.browser.new_context(
                    viewport={"width": 1280, "height": 800}
                )
            except:
                # Fallback to regular chromium
                self.browser = await self.playwright.chromium.launch(headless=False)
                self.context = await self.browser.new_context(
                    viewport={"width": 1280, "height": 800}
                )
        
        self.page = await self.context.new_page()
        print("[OK] Browser initialized")
        
    async def login_if_needed(self):
        """Navigate to X and check if logged in"""
        print("[INFO] Checking login status...")
        await self.page.goto("https://x.com")
        await asyncio.sleep(3)
        
        # Check if we're logged in by looking for compose button
        try:
            await self.page.wait_for_selector('[data-testid="SideNav_NewTweet_Button"]', timeout=5000)
            print("[OK] Already logged in")
            return True
        except:
            print("[WARN] Not logged in - manual login required")
            print("[INFO] Please log in to X in the browser window")
            await asyncio.sleep(30)  # Give time to login
            return False
    
    async def post_tweet(self, content: str) -> bool:
        """Post a single tweet"""
        try:
            print(f"[POST] Posting tweet: {content[:50]}...")
            
            # Navigate to compose
            await self.page.goto("https://x.com/compose/tweet")
            await asyncio.sleep(2)
            
            # Find and fill the tweet input
            tweet_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
            await tweet_input.fill(content)
            await asyncio.sleep(1)
            
            # Click post button
            post_button = await self.page.wait_for_selector('[data-testid="tweetButton"]', timeout=10000)
            await post_button.click()
            await asyncio.sleep(3)
            
            print("[OK] Tweet posted successfully")
            return True
            
        except Exception as e:
            print(f"[FAIL] Failed to post tweet: {e}")
            return False
    
    async def post_thread(self, tweets: List[str]) -> bool:
        """Post a thread (multiple connected tweets)"""
        try:
            print(f"[POST] Posting thread with {len(tweets)} tweets...")
            
            # Navigate to compose
            await self.page.goto("https://x.com/compose/tweet")
            await asyncio.sleep(2)
            
            for i, tweet in enumerate(tweets):
                # Fill current tweet
                print(f"[INFO] Tweet {i+1}/{len(tweets)}")
                textarea = await self.page.wait_for_selector(f'[data-testid="tweetTextarea_{i}"]', timeout=10000)
                await textarea.fill(tweet)
                await asyncio.sleep(1)
                
                # Add another tweet if not the last one
                if i < len(tweets) - 1:
                    add_button = await self.page.wait_for_selector('[data-testid="addButton"]', timeout=10000)
                    await add_button.click()
                    await asyncio.sleep(1)
            
            # Click post all
            post_button = await self.page.wait_for_selector('[data-testid="tweetButton"]', timeout=10000)
            await post_button.click()
            await asyncio.sleep(5)
            
            print(f"[OK] Thread posted successfully ({len(tweets)} tweets)")
            return True
            
        except Exception as e:
            print(f"[FAIL] Failed to post thread: {e}")
            return False
    
    async def like_tweet(self, tweet_url: str) -> bool:
        """Like a specific tweet"""
        try:
            await self.page.goto(tweet_url)
            await asyncio.sleep(2)
            
            like_button = await self.page.wait_for_selector('[data-testid="like"]', timeout=10000)
            await like_button.click()
            await asyncio.sleep(1)
            
            print("[OK] Liked tweet")
            return True
            
        except Exception as e:
            print(f"[FAIL] Failed to like tweet: {e}")
            return False
    
    async def reply_to_tweet(self, tweet_url: str, reply_text: str) -> bool:
        """Reply to a specific tweet"""
        try:
            await self.page.goto(tweet_url)
            await asyncio.sleep(2)
            
            # Click reply
            reply_button = await self.page.wait_for_selector('[data-testid="reply"]', timeout=10000)
            await reply_button.click()
            await asyncio.sleep(1)
            
            # Fill reply
            reply_input = await self.page.wait_for_selector('[data-testid="tweetTextarea_0"]', timeout=10000)
            await reply_input.fill(reply_text)
            await asyncio.sleep(1)
            
            # Post reply
            post_button = await self.page.wait_for_selector('[data-testid="tweetButton"]', timeout=10000)
            await post_button.click()
            await asyncio.sleep(3)
            
            print("[OK] Reply posted")
            return True
            
        except Exception as e:
            print(f"[FAIL] Failed to reply: {e}")
            return False
    
    async def get_follower_count(self) -> int:
        """Get current follower count"""
        try:
            await self.page.goto(f"https://x.com/{self.config['account']}")
            await asyncio.sleep(3)
            
            # Look for followers count
            followers_element = await self.page.wait_for_selector(f'a[href="/{self.config["account"]}/followers"] span span', timeout=10000)
            followers_text = await followers_element.inner_text()
            
            # Parse number
            followers_text = followers_text.replace(',', '').replace('K', '000').replace('M', '000000')
            followers = int(followers_text)
            
            print(f"[STATS] Current followers: {followers}")
            return followers
            
        except Exception as e:
            print(f"[FAIL] Failed to get follower count: {e}")
            return self.config.get('current_followers', 212)
    
    async def search_tweets(self, query: str, count: int = 10) -> List[Dict]:
        """Search for tweets by query"""
        try:
            await self.page.goto(f"https://x.com/search?q={query}&f=live")
            await asyncio.sleep(3)
            
            tweets = []
            tweet_elements = await self.page.query_selector_all('article[data-testid="tweet"]')
            
            for element in tweet_elements[:count]:
                try:
                    text_element = await element.query_selector('[data-testid="tweetText"]')
                    text = await text_element.inner_text() if text_element else ""
                    
                    link_element = await element.query_selector('a[href*="/status/"]')
                    href = await link_element.get_attribute('href') if link_element else ""
                    
                    tweets.append({
                        'text': text[:100],
                        'url': f"https://x.com{href}" if href else ""
                    })
                except:
                    continue
            
            print(f"[SEARCH] Found {len(tweets)} tweets for '{query}'")
            return tweets
            
        except Exception as e:
            print(f"[FAIL] Failed to search tweets: {e}")
            return []
    
    async def close(self):
        """Close browser"""
        if self.context:
            await self.context.close()
        if self.browser:
            await self.browser.close()
        if self.playwright:
            await self.playwright.stop()
        print("[OK] Browser closed")

async def test_system():
    """Test the automation system"""
    print("[START] Starting X Automation System Test")
    print("=" * 50)
    
    system = XAutomationSystem()
    
    try:
        # Initialize with visible browser for first login
        await system.initialize(headless=False)
        
        # Check login
        logged_in = await system.login_if_needed()
        
        if logged_in:
            # Test follower count
            followers = await system.get_follower_count()
            
            # Test search
            tweets = await system.search_tweets("ETH treasury", count=3)
            
            print("\n" + "=" * 50)
            print("[SUCCESS] System Test Results:")
            print(f"  Login: Working")
            print(f"  Follower Count: {followers}")
            print(f"  Search: Found {len(tweets)} tweets")
            print("\nSystem ready for full automation!")
            
        else:
            print("\n[WARN] Please login manually and run again")
            
    except Exception as e:
        print(f"\n[FAIL] System test failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        await system.close()

if __name__ == "__main__":
    asyncio.run(test_system())
