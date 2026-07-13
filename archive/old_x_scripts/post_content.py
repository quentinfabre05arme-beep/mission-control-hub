#!/usr/bin/env python3
"""
Post specific content to X
Usage: python post_content.py [thread|single] [topic]
"""

import asyncio
import sys
from x_automation_system import XAutomationSystem
from x_automation_scheduler import ContentLibrary

async def post_thread(topic: str):
    """Post a thread on specific topic"""
    system = XAutomationSystem()
    
    try:
        await system.initialize(headless=False)
        logged_in = await system.login_if_needed()
        
        if not logged_in:
            print("❌ Not logged in")
            return
        
        # Get thread content
        if topic not in ContentLibrary.THREADS:
            print(f"❌ Unknown topic: {topic}")
            print(f"Available: {list(ContentLibrary.THREADS.keys())}")
            return
        
        thread_content = ContentLibrary.THREADS[topic]
        
        print(f"\n📝 Posting thread: {topic}")
        print(f"   {len(thread_content)} tweets")
        print("\nContent preview:")
        for i, tweet in enumerate(thread_content, 1):
            print(f"\n--- Tweet {i} ---")
            print(tweet[:100] + "..." if len(tweet) > 100 else tweet)
        
        confirm = input("\nPost this thread? (yes/no): ")
        if confirm.lower() == "yes":
            success = await system.post_thread(thread_content)
            if success:
                print("✅ Thread posted successfully!")
            else:
                print("❌ Failed to post thread")
        else:
            print("❌ Cancelled")
            
    finally:
        await system.close()

async def post_single(text: str):
    """Post a single tweet"""
    system = XAutomationSystem()
    
    try:
        await system.initialize(headless=False)
        logged_in = await system.login_if_needed()
        
        if not logged_in:
            print("❌ Not logged in")
            return
        
        print(f"\n📝 Posting tweet:")
        print(f"   {text[:100]}...")
        
        confirm = input("\nPost this tweet? (yes/no): ")
        if confirm.lower() == "yes":
            success = await system.post_tweet(text)
            if success:
                print("✅ Tweet posted successfully!")
            else:
                print("❌ Failed to post")
        else:
            print("❌ Cancelled")
            
    finally:
        await system.close()

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python post_content.py thread [hims_healthcare|ai_agentic_commerce|eth_treasury]")
        print("  python post_content.py single 'Your tweet text here'")
        return
    
    content_type = sys.argv[1]
    
    if content_type == "thread":
        if len(sys.argv) < 3:
            print("Available topics:")
            for topic in ContentLibrary.THREADS.keys():
                print(f"  - {topic}")
            return
        topic = sys.argv[2]
        asyncio.run(post_thread(topic))
        
    elif content_type == "single":
        if len(sys.argv) < 3:
            print("Usage: python post_content.py single 'Your tweet text'")
            return
        text = " ".join(sys.argv[2:])
        asyncio.run(post_single(text))
        
    else:
        print(f"❌ Unknown content type: {content_type}")

if __name__ == "__main__":
    main()
