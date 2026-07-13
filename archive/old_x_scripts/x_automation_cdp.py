#!/usr/bin/env python3
"""
X Automation using Chrome DevTools Protocol
Connects to your already-running Chrome with existing login
"""

import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Dict

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests -q")
    import requests

class XAutomationCDP:
    """Control Chrome via CDP using existing logged-in browser"""
    
    def __init__(self, cdp_url: str = "http://127.0.0.1:9222"):
        self.cdp_url = cdp_url
        self.session = requests.Session()
        
    def get_tabs(self) -> List[Dict]:
        """Get all open tabs"""
        try:
            response = self.session.get(f"{self.cdp_url}/json/list")
            return response.json()
        except Exception as e:
            print(f"[FAIL] Cannot connect to Chrome: {e}")
            print("[INFO] Make sure Chrome is running with --remote-debugging-port=9222")
            return []
    
    def navigate(self, tab_id: str, url: str) -> bool:
        """Navigate tab to URL"""
        try:
            ws_url = None
            tabs = self.get_tabs()
            for tab in tabs:
                if tab.get('id') == tab_id or tab.get('title') == tab_id:
                    ws_url = tab.get('webSocketDebuggerUrl')
                    break
            
            if not ws_url:
                print(f"[FAIL] Tab not found: {tab_id}")
                return False
            
            # Use CDP to navigate
            import websocket
            ws = websocket.create_connection(ws_url)
            ws.send(json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": f"window.location.href = '{url}'"}
            }))
            ws.close()
            return True
            
        except Exception as e:
            print(f"[FAIL] Navigation failed: {e}")
            return False
    
    def post_tweet(self, content: str) -> bool:
        """Post a tweet using CDP"""
        try:
            print(f"[POST] Posting: {content[:50]}...")
            
            # First, navigate to compose
            tabs = self.get_tabs()
            x_tab = None
            for tab in tabs:
                if 'x.com' in tab.get('url', ''):
                    x_tab = tab
                    break
            
            if not x_tab:
                print("[FAIL] No X tab found. Open x.com first.")
                return False
            
            ws_url = x_tab.get('webSocketDebuggerUrl')
            if not ws_url:
                print("[FAIL] Cannot get WebSocket URL")
                return False
            
            import websocket
            ws = websocket.create_connection(ws_url)
            
            # Navigate to compose
            ws.send(json.dumps({
                "id": 1,
                "method": "Runtime.evaluate",
                "params": {"expression": "window.location.href = 'https://x.com/compose/tweet'"}
            }))
            
            import time
            time.sleep(3)  # Wait for page load
            
            # Find and fill the textarea
            ws.send(json.dumps({
                "id": 2,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": f"""
                        (function() {{
                            const textarea = document.querySelector('[data-testid="tweetTextarea_0"]');
                            if (textarea) {{
                                textarea.innerHTML = '{content.replace("'", "\\'")}';
                                textarea.dispatchEvent(new Event('input', {{ bubbles: true }}));
                                return 'Text entered';
                            }}
                            return 'Textarea not found';
                        }})()
                    """
                }
            }))
            
            time.sleep(1)
            
            # Click post button
            ws.send(json.dumps({
                "id": 3,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": """
                        (function() {
                            const button = document.querySelector('[data-testid="tweetButton"]');
                            if (button && !button.disabled) {
                                button.click();
                                return 'Clicked post';
                            }
                            return 'Button not found or disabled';
                        })()
                    """
                }
            }))
            
            ws.close()
            print("[OK] Tweet posted via CDP")
            return True
            
        except Exception as e:
            print(f"[FAIL] Failed to post: {e}")
            return False

def test_cdp():
    """Test CDP connection"""
    print("[TEST] Testing Chrome DevTools Protocol connection...")
    print("=" * 50)
    
    automation = XAutomationCDP()
    
    # Get tabs
    tabs = automation.get_tabs()
    
    if not tabs:
        print("\n[FAIL] Cannot connect to Chrome CDP")
        print("\n[SOLUTION] Close Chrome completely, then restart with:")
        print("\"C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe\" --remote-debugging-port=9222")
        print("\nThen open x.com and log in.")
        return False
    
    print(f"[OK] Connected! Found {len(tabs)} tabs:")
    for tab in tabs:
        print(f"  - {tab.get('title', 'Unknown')[:40]}... ({tab.get('url', '')[:50]}...)")
    
    # Check if X is open
    x_tabs = [t for t in tabs if 'x.com' in t.get('url', '')]
    if x_tabs:
        print(f"\n[OK] Found {len(x_tabs)} X tab(s)")
        print("[OK] CDP connection working!")
        return True
    else:
        print("\n[WARN] No X tabs found. Open x.com first.")
        return False

if __name__ == "__main__":
    import sys
    
    # Check for websocket-client
    try:
        import websocket
    except ImportError:
        print("Installing websocket-client...")
        os.system("pip install websocket-client -q")
        import websocket
    
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test_cdp()
    elif len(sys.argv) > 2 and sys.argv[1] == "post":
        automation = XAutomationCDP()
        content = " ".join(sys.argv[2:])
        automation.post_tweet(content)
    else:
        print("Usage:")
        print("  python x_automation_cdp.py test")
        print("  python x_automation_cdp.py post 'Your tweet text'")
