import urllib.request
import json

try:
    # Test CDP connection
    req = urllib.request.Request('http://127.0.0.1:9222/json/list')
    with urllib.request.urlopen(req, timeout=5) as response:
        data = json.loads(response.read().decode())
        print(f"[OK] CDP Connected! Found {len(data)} tabs")
        for tab in data[:3]:
            print(f"  - {tab.get('title', 'Unknown')[:40]}")
except Exception as e:
    print(f"[FAIL] {e}")
    print("Chrome may have closed or CDP not enabled")
