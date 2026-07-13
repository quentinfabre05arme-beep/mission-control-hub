#!/usr/bin/env python3
import json

with open('C:/Users/quent/.openclaw/workspace/ONEDRIVE_REORG_PROGRESS.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total Processed: {data['total_processed']:,}")
print(f"Target: {data['total_target']:,}")
print(f"Current Batch: {data['current_batch']}")
print(f"Status: {data['status']}")
print(f"Estimated Completion: {data.get('estimated_completion', 'N/A')}")
print(f"\nBreakdown by type:")
totals = {}
for batch in data.get('batches', []):
    for key, val in batch.get('stats', {}).items():
        totals[key] = totals.get(key, 0) + val
for key, val in sorted(totals.items()):
    if val > 0:
        print(f"  {key}: {val:,}")
print(f"\nLast Update: {data.get('last_update', 'N/A')}")
