#!/usr/bin/env python3
"""
Quick test of the X automation system
"""

import asyncio
from x_automation_system import XAutomationSystem

async def main():
    print("Testing X Automation System")
    print("=" * 50)
    
    system = XAutomationSystem()
    
    try:
        # Initialize with visible browser
        print("\n1. Initializing browser...")
        await system.initialize(headless=False)
        
        # Check login
        print("\n2. Checking login status...")
        logged_in = await system.login_if_needed()
        
        if logged_in:
            print("\n3. Testing features...")
            
            # Test follower count
            print("   Getting follower count...")
            followers = await system.get_follower_count()
            print(f"   Followers: {followers}")
            
            # Test search
            print("\n   Searching tweets...")
            tweets = await system.search_tweets("ETH treasury", count=3)
            print(f"   Found {len(tweets)} tweets")
            for tweet in tweets[:2]:
                print(f"   - {tweet['text'][:60]}...")
            
            print("\n" + "=" * 50)
            print("All systems operational!")
            print("\nNext steps:")
            print("1. Run: python x_automation_scheduler.py")
            print("2. Or test posting: python post_content.py")
            
        else:
            print("\nPlease log in manually and re-run")
            
    except Exception as e:
        print(f"\nTest failed: {e}")
        import traceback
        traceback.print_exc()
        
    finally:
        print("\nClosing browser...")
        await system.close()
        print("Test complete")

if __name__ == "__main__":
    asyncio.run(main())
