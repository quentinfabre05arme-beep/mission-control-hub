"""
Dashboard Audit Script
Checks all mission_control_*.html files for common issues
"""
import os
import re
from pathlib import Path

def audit_dashboard(filepath):
    """Audit a single dashboard file"""
    issues = []
    warnings = []
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    filename = os.path.basename(filepath)
    
    # Check 1: Proper HTML structure
    if not content.strip().startswith('<!DOCTYPE html>'):
        issues.append("Missing DOCTYPE declaration")
    
    if '<html' not in content:
        issues.append("Missing <html> tag")
    
    if '</html>' not in content:
        issues.append("Missing closing </html> tag")
    
    # Check 2: Has title
    if '<title>' not in content:
        issues.append("Missing <title> tag")
    
    # Check 3: Mobile viewport
    if 'viewport' not in content:
        warnings.append("Missing viewport meta tag (mobile won't work well)")
    
    # Check 4: External links (localhost references)
    localhost_refs = re.findall(r'http://localhost[^\s\"\'\>]*', content)
    if localhost_refs:
        issues.append(f"Has {len(localhost_refs)} localhost references (won't work on Vercel)")
        for ref in localhost_refs[:3]:
            issues.append(f"  - {ref}")
    
    # Check 5: Missing linked files
    linked_files = re.findall(r'href=["\']([^"\']+\.html)["\']', content)
    for linked in linked_files:
        if linked.startswith('http'):
            continue
        linked_path = os.path.join(os.path.dirname(filepath), linked)
        if not os.path.exists(linked_path):
            issues.append(f"Broken link: {linked} (file not found)")
    
    # Check 6: JavaScript errors potential
    if 'innerHTML' in content and 'getElementById' in content:
        # Check for null reference potential
        null_checks = content.count('if (') + content.count('?.')
        if null_checks < 5:
            warnings.append("Potential null reference issues (limited error checking)")
    
    # Check 7: Hardcoded data
    if re.search(r'\$\d{2,},?\d*', content) and 'fetch(' not in content:
        warnings.append("May have hardcoded prices/data (no live data fetching)")
    
    # Check 8: Responsive design
    if '@media' not in content and 'minmax(' not in content:
        warnings.append("No responsive CSS detected")
    
    return {
        'filename': filename,
        'size_kb': round(len(content) / 1024, 1),
        'issues': issues,
        'warnings': warnings,
        'status': 'ERROR' if issues else ('WARNING' if warnings else 'OK')
    }

def main():
    workspace = Path('C:/Users/quent/.openclaw/workspace')
    dashboards = sorted(workspace.glob('mission_control_*.html'))
    
    print("=" * 70)
    print("DASHBOARD AUDIT REPORT")
    print("=" * 70)
    print(f"Total dashboards found: {len(dashboards)}\n")
    
    results = []
    for dash in dashboards:
        result = audit_dashboard(str(dash))
        results.append(result)
    
    # Summary
    ok_count = sum(1 for r in results if r['status'] == 'OK')
    warning_count = sum(1 for r in results if r['status'] == 'WARNING')
    error_count = sum(1 for r in results if r['status'] == 'ERROR')
    
    print(f"Status Summary:")
    print(f"  [OK]        {ok_count}")
    print(f"  [WARNING]   {warning_count}")
    print(f"  [ERROR]     {error_count}")
    print()
    
    # Detailed report
    for result in results:
        icon = '[OK]' if result['status'] == 'OK' else ('[WARN]' if result['status'] == 'WARNING' else '[ERR]')
        print(f"{icon} {result['filename']} ({result['size_kb']} KB)")
        
        for issue in result['issues']:
            print(f"   [ERR] {issue}")
        for warning in result['warnings']:
            print(f"   [WARN] {warning}")
        
        if not result['issues'] and not result['warnings']:
            print(f"   [OK] No issues found")
        print()
    
    # Critical issues summary
    print("=" * 70)
    print("CRITICAL ISSUES TO FIX:")
    print("=" * 70)
    
    critical_found = False
    for result in results:
        if result['issues']:
            critical_found = True
            print(f"\n{result['filename']}:")
            for issue in result['issues']:
                print(f"  - {issue}")
    
    if not critical_found:
        print("  [OK] No critical issues found!")
    
    print()
    return results

if __name__ == '__main__':
    main()
