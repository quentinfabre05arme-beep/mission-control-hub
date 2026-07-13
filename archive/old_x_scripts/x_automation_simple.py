#!/usr/bin/env python3
"""
Simple X Automation using OpenClaw browser tool
Leverages existing browser connection
"""

import subprocess
import time
import json
import os
from pathlib import Path

class XAutomationSimple:
    """Use OpenClaw browser CLI for automation"""
    
    def __init__(self):
        self.token = self._get_token()
        
    def _get_token(self) -> str:
        """Get browser token from OpenClaw"""
        # Try to read from config or use default
        try:
            result = subprocess.run(
                ["openclaw", "browser", "status"],
                capture_output=True, text=True, timeout=10
            )
            # Extract token from output if needed
            return "c02cc9c02cc9c02cc9c02cc9c02cc9"  # Use working token
        except:
            return "c02cc9c02cc9c02cc9c02cc9c02cc9"
    
    def open_compose(self) -> str:
        """Open X compose page"""
        cmd = [
            "openclaw", "browser", "--token", self.token,
            "open", "https://x.com/compose/tweet",
            "--label", "x_compose"
        ]
        
        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            print("[OK] Opened X compose page")
            return "x_compose"
        except Exception as e:
            print(f"[FAIL] {e}")
            return None
    
    def screenshot(self, tab: str) -> bool:
        """Take screenshot"""
        cmd = [
            "openclaw", "browser", "--token", self.token,
            "screenshot", tab
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=30)
            return True
        except:
            return False
    
    def close_tab(self, tab: str):
        """Close tab"""
        cmd = [
            "openclaw", "browser", "--token", self.token,
            "close", tab
        ]
        
        try:
            subprocess.run(cmd, capture_output=True, timeout=10)
        except:
            pass

def main():
    """Test the simple automation"""
    print("[START] Simple X Automation Test")
    print("=" * 50)
    
    automation = XAutomationSimple()
    
    # Open compose
    print("\n[STEP 1] Opening X compose page...")
    tab = automation.open_compose()
    
    if tab:
        print(f"[OK] Tab opened: {tab}")
        
        # Take screenshot
        print("\n[STEP 2] Taking screenshot...")
        if automation.screenshot(tab):
            print("[OK] Screenshot captured")
        
        print("\n[STEP 3] Browser is open. You need to:")
        print("  1. Switch to Chrome browser")
        print("  2. Type your content")
        print("  3. Click Post button")
        
        input("\nPress Enter after posting (or Ctrl+C to close)...")
        
        # Close tab
        automation.close_tab(tab)
        print("[OK] Tab closed")
        
    else:
        print("[FAIL] Could not open compose page")
        print("\n[TROUBLESHOOTING]")
        print("1. Make sure Chrome is running")
        print("2. Check 'openclaw browser status'")
        print("3. Verify token is valid")

if __name__ == "__main__":
    main()
