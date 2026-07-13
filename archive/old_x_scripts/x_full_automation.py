#!/usr/bin/env python3
"""
X Full Browser Automation - Complete posting workflow
Uses Playwright-like automation with element detection
"""

import subprocess
import time
import json
from datetime import datetime
from typing import Dict, Optional

TOKEN = "c02cc9e6ff0cb473defa142e9029c6fbc86cec4879c45c69"
LABEL = "x_automation"

class XFullAutomation:
    def __init__(self):
        self.token = TOKEN
        self.label = LABEL
        
    def run_cmd(self, cmd: str) -> str:
        """Execute browser command"""
        full_cmd = f'openclaw browser --token {self.token} {cmd}'
        print(f"CMD: {full_cmd[:80]}...")
        
        result = subprocess.run(
            full_cmd,
            shell=True,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout or result.stderr
        print(f"OUT: {output[:100]}")
        return output
    
    def open_x_compose(self) -> bool:
        """Open X compose in new tab"""
        print("\n[1/6] Opening X compose...")
        result = self.run_cmd(f'open https://x.com/compose/tweet --label {self.label}')
        time.sleep(3)
        return "opened" in result.lower()
    
    def get_page_elements(self) -> Dict:
        """Get accessible elements from page"""
        print("\n[2/6] Getting page elements...")
        
        # Try different snapshot formats
        for fmt in ["aria", "ai"]:
            result = self.run_cmd(f'snapshot --format {fmt} --label {self.label}')
            if result and len(result) > 50:
                print(f"Got {fmt} snapshot")
                return {"format": fmt, "data": result}
        
        return {}
    
    def find_text_input(self, elements: Dict) -> Optional[str]:
        """Find the tweet text input element"""
        print("\n[3/6] Finding text input...")
        
        # For now, use JavaScript evaluation to find and fill the input
        # This is more reliable than aria refs for X's complex UI
        
        js_code = '''
        (function() {
            // X compose uses contenteditable divs
            const inputs = document.querySelectorAll('[contenteditable="true"]');
            if (inputs.length > 0) {
                inputs[0].focus();
                return "found";
            }
            return "not_found";
        })()
        '''
        
        # Evaluate JavaScript
        result = self.run_cmd(f'evaluate --fn "{js_code}" --label {self.label}')
        print(f"Text input search: {result}")
        
        return "found" if "found" in result else None
    
    def type_content(self, content: str) -> bool:
        """Type tweet content using multiple methods"""
        print(f"\n[4/6] Typing content: {content[:50]}...")
        
        # Method 1: JavaScript injection (most reliable for X)
        js_code = f'''
        (function() {{
            const input = document.querySelector('[contenteditable="true"]');
            if (input) {{
                input.innerHTML = "{content.replace('"', '\\"')}";
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
                return "typed";
            }}
            return "failed";
        }})()
        '''
        
        result = self.run_cmd(f'evaluate --fn "{js_code}" --label {self.label}')
        print(f"Type result: {result}")
        
        time.sleep(1)
        return "typed" in result
    
    def click_post_button(self) -> bool:
        """Click the Post button"""
        print("\n[5/6] Clicking Post button...")
        
        # Use JavaScript to find and click Post button
        js_code = '''
        (function() {
            const buttons = document.querySelectorAll('button');
            for (let btn of buttons) {
                if (btn.textContent.includes('Post') && !btn.disabled) {
                    btn.click();
                    return "clicked";
                }
            }
            return "not_found";
        })()
        '''
        
        result = self.run_cmd(f'evaluate --fn "{js_code}" --label {self.label}')
        print(f"Click result: {result}")
        
        time.sleep(2)
        return "clicked" in result
    
    def take_screenshot(self, prefix: str) -> str:
        """Take screenshot"""
        print(f"\n[*] Taking {prefix} screenshot...")
        result = self.run_cmd(f'screenshot --label {self.label}')
        
        if '.png' in result:
            path = result.strip().split('\n')[-1]
            print(f"Screenshot: {path}")
            return path
        return ""
    
    def post_tweet(self, content: str) -> Dict:
        """Full posting workflow"""
        print("=" * 60)
        print("X FULL AUTOMATION - POSTING")
        print("=" * 60)
        print(f"Content: {content[:60]}...")
        print(f"Time: {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 60)
        
        result = {
            "success": False,
            "content": content,
            "screenshots": [],
            "error": None,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            # 1. Open X compose
            if not self.open_x_compose():
                result["error"] = "Failed to open X"
                return result
            
            # 2. Get page elements
            elements = self.get_page_elements()
            
            # 3. Take pre-type screenshot
            pre_type = self.take_screenshot("pre_type")
            if pre_type:
                result["screenshots"].append(pre_type)
            
            # 4. Find text input
            input_found = self.find_text_input(elements)
            if not input_found:
                result["error"] = "Could not find text input"
                # Still take screenshot to debug
                debug = self.take_screenshot("debug")
                if debug:
                    result["screenshots"].append(debug)
                return result
            
            # 5. Type content
            if not self.type_content(content):
                result["error"] = "Failed to type content"
                return result
            
            # 6. Take pre-post screenshot
            pre_post = self.take_screenshot("pre_post")
            if pre_post:
                result["screenshots"].append(pre_post)
            
            # 7. Click post
            if not self.click_post_button():
                result["error"] = "Failed to click Post"
                return result
            
            # 8. Take confirmation screenshot
            time.sleep(3)
            confirmation = self.take_screenshot("confirmation")
            if confirmation:
                result["screenshots"].append(confirmation)
            
            result["success"] = True
            print("\n✅ POSTED SUCCESSFULLY!")
            
        except Exception as e:
            result["error"] = str(e)
            print(f"\n❌ Error: {e}")
        
        finally:
            # Close tab
            print("\n[6/6] Closing tab...")
            self.run_cmd(f'close {self.label}')
        
        return result
    
    def test(self):
        """Test automation"""
        print("Testing X automation...")
        print(f"Token: {self.token[:10]}...")
        
        # Just open and take screenshot
        self.open_x_compose()
        screenshot = self.take_screenshot("test")
        print(f"Test screenshot: {screenshot}")
        
        # Close
        self.run_cmd(f'close {self.label}')


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python x_full_automation.py [test|post 'content']")
        sys.exit(1)
    
    automation = XFullAutomation()
    
    if sys.argv[1] == "test":
        automation.test()
    
    elif sys.argv[1] == "post" and len(sys.argv) > 2:
        content = sys.argv[2]
        result = automation.post_tweet(content)
        print(json.dumps(result, indent=2))
    
    else:
        print(f"Unknown command: {sys.argv[1]}")


if __name__ == "__main__":
    main()
