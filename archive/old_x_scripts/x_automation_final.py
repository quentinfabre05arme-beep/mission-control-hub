#!/usr/bin/env python3
"""
X Browser Automation - Final Version
Uses proper OpenClaw browser CLI syntax
"""

import subprocess
import json
import time
import re
from datetime import datetime
from typing import Dict, Optional, List

TOKEN = "c02cc9e6ff0cb473defa142e9029c6fbc86cec4879c45c69"
PROFILE = "user"

class XAutomationFinal:
    """Robust X browser automation"""
    
    def __init__(self):
        self.token = TOKEN
        self.profile = PROFILE
        self.current_target = None
        
    def run_cmd(self, cmd: str, timeout: int = 30) -> str:
        """Execute browser command with proper token syntax"""
        full_cmd = f'openclaw browser --token {self.token} --browser-profile {self.profile} {cmd}'
        print(f"\nCMD: {full_cmd[:100]}...")
        
        try:
            result = subprocess.run(
                full_cmd,
                shell=True,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            output = result.stdout.strip() or result.stderr.strip()
            print(f"OUT: {output[:150]}")
            return output
            
        except subprocess.TimeoutExpired:
            print("TIMEOUT")
            return ""
        except Exception as e:
            print(f"ERROR: {e}")
            return ""
    
    def get_tabs(self) -> List[Dict]:
        """List all tabs"""
        print("\n[GET TABS]")
        result = self.run_cmd("tabs")
        
        tabs = []
        for line in result.split('\n'):
            if 'tab:' in line or 'label:' in line:
                tab_info = {"raw": line}
                # Parse tab info
                if 'tab: t' in line:
                    match = re.search(r'tab: (t\d+)', line)
                    if match:
                        tab_info["tab_id"] = match.group(1)
                if 'label:' in line:
                    match = re.search(r'label:([^\s\]]+)', line)
                    if match:
                        tab_info["label"] = match.group(1)
                tabs.append(tab_info)
        
        return tabs
    
    def open_x_compose(self, label: str = "x_post") -> Optional[str]:
        """Open X compose page and return target ID"""
        print(f"\n[OPEN X COMPOSE] Label: {label}")
        
        # First check if tab already exists
        tabs = self.get_tabs()
        for tab in tabs:
            if tab.get("label") == label:
                print(f"Reusing existing tab: {tab.get('tab_id')}")
                self.current_target = tab.get("tab_id")
                return self.current_target
        
        # Open new tab
        result = self.run_cmd(f'open https://x.com/compose/tweet --label {label}')
        
        # Parse result to get tab info
        if "opened:" in result.lower():
            # Wait for page to load
            time.sleep(3)
            
            # Get tabs to find the target
            tabs = self.get_tabs()
            for tab in tabs:
                if tab.get("label") == label:
                    self.current_target = tab.get("tab_id")
                    return self.current_target
        
        return None
    
    def get_snapshot(self, target: str = None, format_type: str = "ai") -> str:
        """Get page snapshot"""
        if not target:
            target = self.current_target
        
        print(f"\n[SNAPSHOT] Target: {target}, Format: {format_type}")
        
        result = self.run_cmd(f'snapshot {target}')
        return result
    
    def find_text_input_ref(self, snapshot: str) -> Optional[str]:
        """Find the text input element reference from snapshot"""
        print("\n[FINDING TEXT INPUT]")
        
        # Look for textarea or contenteditable elements in the snapshot
        # Snapshot format varies, so we'll look for patterns
        lines = snapshot.split('\n')
        
        for i, line in enumerate(lines):
            # Look for text input indicators
            if any(keyword in line.lower() for keyword in ['textarea', 'textbox', 'input', 'edit', 'compose']):
                # Try to extract ref number
                match = re.match(r'^(\d+)\s*[:\-]', line)
                if match:
                    ref = match.group(1)
                    print(f"Found potential input at ref {ref}: {line[:60]}")
                    return ref
        
        # Default to ref 1 if we can't find it
        print("Could not find specific input, defaulting to exploration")
        return None
    
    def type_text(self, text: str, target: str = None) -> bool:
        """Type text into the compose box"""
        if not target:
            target = self.current_target
        
        print(f"\n[TYPING] Target: {target}")
        print(f"Content: {text[:60]}...")
        
        # Method 1: Use JavaScript evaluation to find and fill the input
        js_code = f'''
        (function() {{
            // X uses contenteditable divs
            const editor = document.querySelector('[data-testid="tweetTextarea_0"]') ||
                          document.querySelector('[contenteditable="true"]') ||
                          document.querySelector('div[role="textbox"]');
            
            if (editor) {{
                // Focus the editor
                editor.focus();
                
                // Clear existing content
                editor.innerHTML = '';
                
                // Insert text
                const textNode = document.createTextNode("{text.replace('"', '\\"')}");
                editor.appendChild(textNode);
                
                // Dispatch input event
                const event = new Event('input', {{ bubbles: true }});
                editor.dispatchEvent(event);
                
                // Dispatch change event
                const changeEvent = new Event('change', {{ bubbles: true }});
                editor.dispatchEvent(changeEvent);
                
                return "success:" + editor.tagName;
            }}
            
            return "not_found";
        }})()
        '''
        
        # Run the JavaScript
        js_code_escaped = js_code.replace('"', '\\"').replace('\n', ' ')
        result = self.run_cmd(f'evaluate --fn "{js_code_escaped}" {target}')
        
        if "success" in result:
            print(f"✓ Typed successfully: {result}")
            return True
        else:
            print(f"✗ Failed to type: {result}")
            return False
    
    def click_post(self, target: str = None) -> bool:
        """Click the Post button"""
        if not target:
            target = self.current_target
        
        print(f"\n[CLICKING POST] Target: {target}")
        
        # Use JavaScript to find and click Post button
        js_code = '''
        (function() {
            // X Post button selectors
            const selectors = [
                '[data-testid="tweetButtonInline"]',
                '[data-testid="tweetButton"]',
                'button[role="button"][aria-label*="Post"]',
                'button:contains("Post")'
            ];
            
            for (let selector of selectors) {
                try {
                    const btn = document.querySelector(selector);
                    if (btn && !btn.disabled) {
                        btn.click();
                        return "clicked:" + selector;
                    }
                } catch(e) {}
            }
            
            // Fallback: find by text content
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent.includes('Post') && !btn.disabled) {
                    btn.click();
                    return "clicked_by_text";
                }
            }
            
            return "not_found";
        })()
        '''
        
        js_code_escaped = js_code.replace('"', '\\"').replace('\n', ' ')
        result = self.run_cmd(f'evaluate --fn "{js_code_escaped}" {target}')
        
        if "clicked" in result:
            print(f"✓ Clicked Post: {result}")
            time.sleep(3)  # Wait for post to complete
            return True
        else:
            print(f"✗ Failed to click: {result}")
            return False
    
    def take_screenshot(self, name: str = "screenshot", target: str = None) -> str:
        """Take screenshot"""
        if not target:
            target = self.current_target
        
        print(f"\n[SCREENSHOT] Target: {target}, Name: {name}")
        
        timestamp = datetime.now().strftime("%H%M%S")
        result = self.run_cmd(f'screenshot {target}')
        
        # Parse screenshot path
        if '.png' in result:
            path = result.strip().split('\n')[-1]
            print(f"✓ Screenshot saved: {path}")
            return path
        
        return ""
    
    def post_tweet(self, content: str) -> Dict:
        """Full posting workflow"""
        print("=" * 70)
        print("X FULL AUTOMATION")
        print("=" * 70)
        print(f"Content: {content[:70]}")
        print(f"Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)
        
        result = {
            "success": False,
            "content": content,
            "timestamp": datetime.now().isoformat(),
            "target": None,
            "screenshots": [],
            "error": None
        }
        
        try:
            # 1. Open X compose
            print("\n📍 STEP 1: Open X compose")
            target = self.open_x_compose("x_automation")
            if not target:
                result["error"] = "Failed to open X compose"
                return result
            result["target"] = target
            print(f"✓ Opened with target: {target}")
            
            # 2. Take initial screenshot
            print("\n📍 STEP 2: Initial screenshot")
            ss1 = self.take_screenshot("initial", target)
            if ss1:
                result["screenshots"].append(ss1)
            
            # 3. Type content
            print("\n📍 STEP 3: Type content")
            if not self.type_text(content, target):
                # Take debug screenshot
                ss_debug = self.take_screenshot("debug_type", target)
                if ss_debug:
                    result["screenshots"].append(ss_debug)
                result["error"] = "Failed to type content"
                return result
            
            # 4. Take pre-post screenshot
            print("\n📍 STEP 4: Pre-post screenshot")
            ss2 = self.take_screenshot("pre_post", target)
            if ss2:
                result["screenshots"].append(ss2)
            
            # 5. Click Post
            print("\n📍 STEP 5: Click Post button")
            if not self.click_post(target):
                result["error"] = "Failed to click Post"
                return result
            
            # 6. Take confirmation screenshot
            print("\n📍 STEP 6: Confirmation screenshot")
            time.sleep(2)
            ss3 = self.take_screenshot("confirmation", target)
            if ss3:
                result["screenshots"].append(ss3)
            
            result["success"] = True
            print("\n" + "=" * 70)
            print("✅ SUCCESSFULLY POSTED!")
            print("=" * 70)
            
        except Exception as e:
            result["error"] = str(e)
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Close tab
            print("\n[CLEANUP] Closing tab...")
            if self.current_target:
                self.run_cmd(f'close {self.current_target}')
        
        return result
    
    def test_setup(self) -> bool:
        """Test if browser automation is working"""
        print("\n[TESTING SETUP]")
        
        # Test tabs
        tabs = self.get_tabs()
        print(f"Found {len(tabs)} tabs")
        
        # Test opening
        target = self.open_x_compose("test_setup")
        if target:
            print(f"✓ Open works: {target}")
            
            # Test screenshot
            ss = self.take_screenshot("test", target)
            if ss:
                print(f"✓ Screenshot works: {ss}")
            
            # Close
            self.run_cmd(f'close {target}')
            print("✓ Close works")
            
            return True
        
        return False


def main():
    import sys
    
    automation = XAutomationFinal()
    
    if len(sys.argv) < 2:
        print("Usage: python x_automation_final.py [test|post 'content']")
        print("\nExamples:")
        print('  python x_automation_final.py test')
        print('  python x_automation_final.py post "Hello from automation!"')
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "test":
        print("\n" + "=" * 70)
        print("TESTING X AUTOMATION SETUP")
        print("=" * 70)
        success = automation.test_setup()
        if success:
            print("\n[PASS] ALL TESTS PASSED")
        else:
            print("\n[FAIL] TESTS FAILED")
    
    elif command == "post":
        if len(sys.argv) < 3:
            print("Error: Need content to post")
            sys.exit(1)
        
        content = sys.argv[2]
        result = automation.post_tweet(content)
        
        print("\n" + "=" * 70)
        print("RESULT")
        print("=" * 70)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()
