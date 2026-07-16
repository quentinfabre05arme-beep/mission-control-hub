import json

with open('ingestion_batch_4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Fix remaining bad names
for r in data['recipes']:
    if any(ord(c) > 127 for c in r['name'][:5]) or r['name'].startswith('1,2 kg'):
        r['name'] = r['file'].replace('.docx', '').replace('.doc', '').replace('.odt', '').replace('_', ' ').strip()
    # Fix gratin pommes de terre
    if r['name'] == '1,2 kg de pommes de terre à chair ferme':
        r['name'] = 'GRATIN POMMES DE TERRE CHÈVRE'

for m in data['menus']:
    if any(ord(c) > 127 for c in m['name'][:10]):
        m['name'] = m['file'].replace('.docx', '').replace('.doc', '').replace('_', ' ').strip()

with open('ingestion_batch_4.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print('Final fixes applied!')
print(f"Recipes: {len(data['recipes'])}")
print(f"Menus: {len(data['menus'])}")
print()
print('=== RECIPE NAMES ===')
for r in data['recipes']:
    print(f"  - {r['name']}")
print()
print('=== MENU NAMES ===')
for m in data['menus']:
    print(f"  - {m['name'][:60]}")
