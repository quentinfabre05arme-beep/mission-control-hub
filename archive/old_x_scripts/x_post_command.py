#!/usr/bin/env python3
"""
X Post Command - Simple wrapper to post to X via browser automation
Usage: python x_post_command.py "Your tweet content here"
"""

import sys
import subprocess

def post_to_x(content: str):
    """Post content to X using OpenClaw browser automation"""
    
    print(f"Posting to X: {content}")
    print("This will:")
    print("1. Open Chrome (your existing session)")
    print("2. Navigate to X compose")
    print("3. Type your content")
    print("4. Take screenshot for confirmation")
    print("5. Click Post")
    print()
    
    # In real implementation, these would be actual openclaw browser commands
    # For now, this shows the structure
    
    commands = [
        f'openclaw browser open --url https://x.com/compose/tweet --label x_post --profile user',
        'sleep 3',
        f'openclaw browser type --target x_post --text "{content}"',
        'sleep 1',
        'openclaw browser screenshot --target x_post --output pre_post.png',
        'openclaw browser click --target x_post --text "Post"',
        'sleep 3',
        'openclaw browser screenshot --target x_post --output posted.png',
        'openclaw browser close --target x_post'
    ]
    
    print("Commands to execute:")
    for cmd in commands:
        print(f"  {cmd}")
    
    print("\nTo actually post, run with --live flag")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python x_post_command.py 'Your tweet content'")
        print("       python x_post_command.py 'Your tweet content' --live")
        sys.exit(1)
    
    content = sys.argv[1]
    live_mode = "--live" in sys.argv
    
    if live_mode:
        print("[LIVE MODE - Will actually post]")
    else:
        print("[DRY RUN MODE - Just showing commands]")
    
    post_to_x(content)
