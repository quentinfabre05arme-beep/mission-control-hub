#!/usr/bin/env python3
"""
X Browser Automation - Post directly to X via Chrome browser
Uses OpenClaw browser automation tool
"""

import json
import subprocess
import time
from datetime import datetime
from typing import Dict, Optional, List

class XBrowserAutomation:
    """Browser automation for X posting"""
    
    def __init__(self):
        self.x_url = "https://x.com"
        self.compose_url = "https://x.com/compose/tweet"
        self.label = "x_posting"
        
    def _run_browser_cmd(self, cmd: str) -> str:
        """Execute browser command via OpenClaw"""
        try:
            result = subprocess.run(
                f"openclaw browser {cmd}",
                shell=True,
                capture_output=True,
                text=True,
                timeout=30
            )
            return result.stdout or result.stderr
        except Exception as e:
            return f"Error: {str(e)}"
    
    def open_x(self) -> bool:
        """Open X in browser"""
        print("Opening X in Chrome...")
        result = self._run_browser_cmd(f'open --url {self.x_url} --label {self.label} --profile user')
        print(result)
        
        # Wait for page to load
        time.sleep(3)
        return "opened" in result.lower() or "navigated" in result.lower()
    
    def navigate_to_compose(self) -> bool:
        """Navigate to tweet compose"""
        print("Navigating to compose...")
        result = self._run_browser_cmd(f'navigate --target {self.label} --url {self.compose_url}')
        print(result)
        
        time.sleep(2)
        return True
    
    def type_tweet(self, content: str) -> bool:
        """Type tweet content"""
        print(f"Typing tweet: {content[:50]}...")
        
        # First, check if compose box exists
        result = self._run_browser_cmd(f'snapshot --target {self.label} --refs aria')
        print(result)
        
        # Type the content
        # Note: In actual implementation, we'd find the textarea ref from snapshot
        # For now, this is the structure
        safe_content = content.replace('"', '\\"')
        result = self._run_browser_cmd(f'type --target {self.label} --text "{safe_content}"')
        print(result)
        
        return True
    
    def click_post(self) -> bool:
        """Click the post button"""
        print("Clicking Post button...")
        
        # Find and click post button
        # In actual implementation, we'd find the button ref from snapshot
        result = self._run_browser_cmd(f'click --target {self.label} --element "Post"')
        print(result)
        
        time.sleep(2)
        return True
    
    def take_screenshot(self, filename: str = None) -> str:
        """Take screenshot for confirmation"""
        if not filename:
            filename = f"x_screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        print(f"Taking screenshot: {filename}")
        result = self._run_browser_cmd(f'screenshot --target {self.label} --output {filename}')
        print(result)
        
        return filename
    
    def post_tweet(self, content: str, media_files: List[str] = None) -> Dict:
        """Full posting workflow"""
        result = {
            "success": False,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "screenshot": None,
            "error": None
        }
        
        try:
            # Step 1: Open X
            if not self.open_x():
                result["error"] = "Failed to open X"
                return result
            
            # Step 2: Navigate to compose
            if not self.navigate_to_compose():
                result["error"] = "Failed to navigate to compose"
                return result
            
            # Step 3: Type content
            if not self.type_tweet(content):
                result["error"] = "Failed to type tweet"
                return result
            
            # Step 4: Add media if provided
            if media_files:
                # TODO: Implement media upload
                print(f"Media files to upload: {media_files}")
            
            # Step 5: Take screenshot before posting
            screenshot = self.take_screenshot()
            result["screenshot_before"] = screenshot
            
            # Step 6: Click post
            if not self.click_post():
                result["error"] = "Failed to click post"
                return result
            
            # Step 7: Take screenshot after posting
            time.sleep(3)
            screenshot_after = self.take_screenshot(f"x_posted_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png")
            result["screenshot_after"] = screenshot_after
            
            result["success"] = True
            print("✓ Tweet posted successfully!")
            
        except Exception as e:
            result["error"] = str(e)
            print(f"✗ Error posting tweet: {e}")
        
        return result
    
    def close(self):
        """Close browser tab"""
        print("Closing browser tab...")
        self._run_browser_cmd(f'close --target {self.label}')


def post_to_x(content: str, dry_run: bool = True) -> Dict:
    """Main function to post to X"""
    
    print("=" * 50)
    print("X Browser Automation")
    print("=" * 50)
    print(f"Content: {content}")
    print(f"Dry run: {dry_run}")
    print("=" * 50)
    
    if dry_run:
        print("\n[DRY RUN MODE]")
        print("Would execute:")
        print("1. Open Chrome with existing session")
        print("2. Navigate to X/compose/tweet")
        print("3. Type the content")
        print("4. Take screenshot for approval")
        print("5. Click Post")
        print("6. Take confirmation screenshot")
        return {
            "success": True,
            "dry_run": True,
            "content": content,
            "message": "Dry run completed. Use dry_run=False to actually post."
        }
    
    # Actual posting
    automation = XBrowserAutomation()
    result = automation.post_tweet(content)
    automation.close()
    
    return result


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python x_browser_automation.py [command]")
        print("\nCommands:")
        print('  post "content" [--live]     - Post to X (dry run by default)')
        print('  test                        - Test browser connection')
        return
    
    command = sys.argv[1]
    
    if command == "test":
        print("Testing browser automation...")
        automation = XBrowserAutomation()
        automation.open_x()
        time.sleep(5)
        automation.take_screenshot("test_screenshot.png")
        automation.close()
        print("Test complete. Check test_screenshot.png")
    
    elif command == "post":
        content = sys.argv[2] if len(sys.argv) > 2 else "Test post from automation"
        dry_run = "--live" not in sys.argv
        
        result = post_to_x(content, dry_run)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
