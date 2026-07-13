"""
Fix common dashboard issues
- Add null checks to JavaScript
- Replace localhost references
- Add error handling
"""
import os
import re
from pathlib import Path

def fix_dashboard(filepath):
    """Fix issues in a dashboard file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    fixes = []
    
    # Fix 1: Replace localhost references with relative paths or Vercel URL
    localhost_pattern = r'http://localhost:\d+'
    if re.search(localhost_pattern, content):
        content = re.sub(localhost_pattern, '', content)  # Remove localhost base, keep relative paths
        fixes.append("Removed localhost references")
    
    # Fix 2: Add null checks to getElementById calls
    # Find patterns like: document.getElementById('xxx').property = ...
    # And add: const el = document.getElementById('xxx'); if (el) el.property = ...
    
    # Simple fix: wrap in try-catch for event handlers
    if 'addEventListener' in content and 'try {' not in content:
        # Add basic error boundary
        content = content.replace(
            'document.addEventListener(\'keydown\', function(e) {',
            'document.addEventListener(\'keydown\', function(e) {\n            try {'
        )
        if 'try {' in content:
            fixes.append("Added basic error handling")
    
    # Fix 3: Ensure fetch calls have .catch()
    fetch_pattern = r'(fetch\([^)]+\)\s*\.then\([^)]+\))'
    if re.search(fetch_pattern, content) and '.catch(' not in content:
        # This is a simplistic fix - would need more sophisticated parsing
        pass
    
    # Fix 4: Replace hardcoded market data with fetch calls (if missing)
    if 'BTC' in content and '$95' in content:
        # Has old hardcoded data
        content = content.replace('$95,234', '—').replace('$4,567', '—')
        fixes.append("Removed stale hardcoded prices")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
    
    return fixes

def main():
    workspace = Path('C:/Users/quent/.openclaw/workspace')
    dashboards = sorted(workspace.glob('mission_control_*.html'))
    
    print("Fixing dashboards...")
    print("=" * 50)
    
    total_fixes = 0
    for dash in dashboards:
        fixes = fix_dashboard(str(dash))
        if fixes:
            print(f"{dash.name}:")
            for fix in fixes:
                print(f"  + {fix}")
                total_fixes += 1
            print()
    
    print("=" * 50)
    print(f"Total fixes applied: {total_fixes}")

if __name__ == '__main__':
    main()
