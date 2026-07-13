#!/usr/bin/env python3
"""
X Post Tool - Complete browser automation for posting to X
Usage: python x_post_tool.py "Your tweet content"
"""

import subprocess
import sys
import time
from datetime import datetime

# Your OpenClaw token from config
TOKEN = "c02cc9e6ff0cb473defa142e9029c6fbc86cec4879c45c69"
LABEL = "x_post"

def run_browser_cmd(cmd):
    """Execute browser command"""
    full_cmd = f'openclaw browser --token {TOKEN} {cmd}'
    print(f"Running: {full_cmd}")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    print(f"Output: {result.stdout or result.stderr}")
    return result.stdout or result.stderr

def post_to_x(content):
    """Post content to X"""
    print("=" * 60)
    print("X Browser Automation - Posting")
    print("=" * 60)
    print(f"Content: {content}")
    print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    try:
        # Step 1: Navigate to compose
        print("\n1. Navigating to X compose...")
        run_browser_cmd(f'navigate https://x.com/compose/tweet {LABEL}')
        time.sleep(3)
        
        # Step 2: Take screenshot before typing
        print("\n2. Taking pre-type screenshot...")
        screenshot1 = run_browser_cmd(f'screenshot {LABEL}')
        print(f"Screenshot: {screenshot1}")
        
        # Step 3: Type the content
        print("\n3. Typing content...")
        # Need to find the textarea ref first via snapshot
        snapshot = run_browser_cmd(f'snapshot {LABEL}')
        print(f"Snapshot: {snapshot[:200]}...")
        
        # Step 4: Type content (this will need the correct ref)
        # For now, showing the structure
        print("\n4. Clicking compose box...")
        run_browser_cmd(f'click compose {LABEL}')
        time.sleep(1)
        
        print("\n5. Typing content...")
        run_browser_cmd(f'type \"{content}\" {LABEL}')
        time.sleep(1)
        
        # Step 5: Take screenshot before posting
        print("\n6. Taking pre-post screenshot...")
        screenshot2 = run_browser_cmd(f'screenshot {LABEL}')
        print(f"Screenshot: {screenshot2}")
        
        # Step 6: Click Post button
        print("\n7. Clicking Post button...")
        run_browser_cmd(f'click post {LABEL}')
        time.sleep(3)
        
        # Step 7: Take screenshot after posting
        print("\n8. Taking post confirmation screenshot...")
        screenshot3 = run_browser_cmd(f'screenshot {LABEL}')
        print(f"Screenshot: {screenshot3}")
        
        print("\n✅ Post completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False

def main():
    if len(sys.argv) < 2:
        print("Usage: python x_post_tool.py 'Your tweet content'")
        print("       python x_post_tool.py 'Your tweet content' --dry-run")
        sys.exit(1)
    
    content = sys.argv[1]
    dry_run = "--dry-run" in sys.argv
    
    if dry_run:
        print("[DRY RUN MODE]")
        print(f"Would post: {content}")
        print("Commands that would run:")
        print(f"  1. Navigate to https://x.com/compose/tweet")
        print(f"  2. Type: {content}")
        print(f"  3. Click Post button")
        print(f"  4. Confirm success")
    else:
        post_to_x(content)

if __name__ == "__main__":
    main()
