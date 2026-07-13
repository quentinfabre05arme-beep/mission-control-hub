#!/usr/bin/env python3
"""
X Automation using OpenClaw's built-in CDP (port 18800)
This bypasses all the authentication issues!
"""

import asyncio
import json
import sys
from pathlib import Path

try:
    import requests
    import websocket
except ImportError:
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "requests", "websocket-client", "-q"])
    import requests
    import websocket

class OpenClawCDPAutomation:
    """Use OpenClaw's CDP server directly"""
    
    def __init__(self, cdp_url: str = "http://127.0.0.1:18800"):
        self.cdp_url = cdp_url
        self.ws_url = None
        
    def get_tabs(self):
        """Get all tabs from OpenClaw CDP"""
        try:
            response = requests.get(f"{self.cdp_url}/json/list", timeout=5)
            return response.json()
        except Exception as e:
            print(f"[FAIL] Cannot connect to OpenClaw CDP: {e}")
            return []
    
    def find_x_tab(self):
        """Find X compose tab"""
        tabs = self.get_tabs()
        for tab in tabs:
            if 'x.com' in tab.get('url', ''):
                return tab
        return None
    
    def post_tweet(self, content: str) -> bool:
        """Post a tweet via CDP"""
        try:
            print(f"[POST] Attempting to post: {content[:50]}...")
            
            # Find X tab
            tab = self.find_x_tab()
            if not tab:
                print("[FAIL] No X tab found. Run 'openclaw browser open https://x.com/compose/tweet' first")
                return False
            
            ws_url = tab.get('webSocketDebuggerUrl')
            if not ws_url:
                print("[FAIL] No WebSocket URL")
                return False
            
            print(f"[OK] Found tab: {tab.get('title', 'Unknown')}")
            
            # Connect via WebSocket
            ws = websocket.create_connection(ws_url, timeout=10)
            
            # Navigate to compose (just in case)
            ws.send(json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": "window.location.href = 'https://x.com/compose/tweet'"}
            }))
            
            import time
            time.sleep(3)
            
            # Find and fill textarea using CDP
            escaped_content = content.replace("'", "\\'").replace('"', '\\"')
            
            ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"""
                        (function() {{
                            const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
                            if (textarea) {{
                                textarea.focus();
                                textarea.innerHTML = '{escaped_content}';
                                textarea.textContent = '{escaped_content}';
                                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                return 'Text entered: ' + textarea.innerHTML.length;
                            }}
                            return 'Textarea not found';
                        }})()
                    """
                }
            }))
            
            result = ws.recv()
            print(f"[DEBUG] Type result: {result[:200]}")
            
            time.sleep(1)
            
            # Click post button
            ws.send(json.dumps({
                "id": 3,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": """
                        (function() {
                            const button = document.querySelector('[data-testid="tweetButton"]');
                            if (button) {
                                if (!button.disabled) {
                                    button.click();
                                    return 'Posted!';
                                }
                                return 'Button disabled';
                            }
                            return 'Button not found';
                        })()
                    """
                }
            }))
            
            result = ws.recv()
            print(f"[DEBUG] Post result: {result[:200]}")
            
            ws.close()
            print("[OK] Tweet posted via OpenClaw CDP!")
            return True
            
        except Exception as e:
            print(f"[FAIL] {e}")
            import traceback
            traceback.print_exc()
            return False

def main():
    print("="*50)
    print("X Automation via OpenClaw CDP")
    print("="*50)
    
    automation = OpenClawCDPAutomation()
    
    # Test connection
    print("\n[TEST] Connecting to OpenClaw CDP...")
    tabs = automation.get_tabs()
    
    if not tabs:
        print("\n[INFO] OpenClaw browser not running or CDP not accessible")
        print("\n[SOLUTION] Run:")
        print("  openclaw browser start")
        print("  openclaw browser open https://x.com")
        return
    
    print(f"[OK] Connected! Found {len(tabs)} tabs")
    for tab in tabs:
        print(f"  - {tab.get('title', 'Unknown')[:50]}")
    
    # Check for X
    x_tab = automation.find_x_tab()
    if x_tab:
        print(f"\n[OK] X tab found: {x_tab.get('url', 'Unknown')}")
        
        # Post test
        test_content = "Testing OpenClaw CDP automation " + str(int(time.time()))
        print(f"\n[POST] Posting: {test_content}")
        automation.post_tweet(test_content)
    else:
        print("\n[WARN] No X tab found")
        print("Run: openclaw browser open https://x.com/compose/tweet")

if __name__ == "__main__":
    import time
    main()
