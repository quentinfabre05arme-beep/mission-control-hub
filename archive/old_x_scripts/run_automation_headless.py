#!/usr/bin/env python3
"""
Headless automation runner
Runs scheduler in background with no GUI
"""
import asyncio
import sys
import os

# Add workspace to path
sys.path.insert(0, 'C:\\Users\\quent\\.openclaw\\workspace')

from x_automation_scheduler import AutomationScheduler

async def main():
    """Run scheduler in headless mode"""
    print("[START] X Automation System - Headless Mode")
    print("=" * 50)
    print("Running in background. Check logs in automation_data/")
    
    scheduler = AutomationScheduler()
    
    try:
        # Force headless mode
        await scheduler.system.initialize(headless=True)
        
        # Ensure logged in (will fail if not, but that's expected)
        logged_in = await scheduler.system.login_if_needed()
        
        if not logged_in:
            print("[ERROR] Not logged in. Run test_automation.py first to login.")
            return 1
        
        # Start scheduler
        await scheduler.run()
        
    except KeyboardInterrupt:
        print("\n[STOP] Scheduler stopped")
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        with open('automation_data/error.log', 'a') as f:
            f.write(f"{datetime.now()}: {e}\n")
            f.write(traceback.format_exc())
    finally:
        await scheduler.system.close()
    
    return 0

if __name__ == "__main__":
    from datetime import datetime
    sys.exit(asyncio.run(main()))
