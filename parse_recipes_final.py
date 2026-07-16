import json, re, sys

sys.stdout.reconfigure(encoding='utf-8')

with open('ingestion_batch_4_raw.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

recipes_raw = raw_data['recipes']
menus_raw = raw_data['menus']

# Known bad names and their fixes
RECIPE_NAME_FIXES = {
    'Oeufs pochés aux Morilles.doc': 'Oeufs pochés aux Morilles',
    'Recette Nems Duc.doc': 'Recette Nems Duc',
    'Bolognaise.doc': 'SAUCE BOLOGNAISE',
    'brandade de morue.doc': 'Brandade de Morue',
    'CASSOLETTES DE NOIX DE SAINT-JACQUES A LA SAUCE NORMANDE.docx': 'CASSOLETTES DE NOIX DE SAINT-JACQUES A LA SAUCE NORMANDE',
    'CASSOLETTES DE NOIX DE SAINT JACQUES SAUCE NORMANDE.doc': 'CASSOLETTES DE NOIX DE SAINT JACQUES SAUCE NORMANDE',
    'gratin pommes de terre chèvre.doc': 'GRATIN POMMES DE TERRE CHÈVRE',
    '1,2 kg de pommes de terre à chair ferme.doc': 'GRATIN POMMES DE TERRE CHÈVRE',
    'brandade de morue.doc': 'Brandade de Morue',
    'CASSOLETTES DE NOIX DE SAINT-JACQUES A LA SAUCE NORMANDE.docx': 'CASSOLETTES DE NOIX DE SAINT-JACQUES A LA SAUCE NORMANDE',
    'CASSOLETTES DE NOIX DE SAINT JACQUES SAUCE NORMANDE.doc': 'CASSOLETTES DE NOIX DE SAINT JACQUES SAUCE NORMANDE',
    'Escalope de dinde aux radis noirs.odt': 'Escalope de dinde aux radis noirs',
    'pate pizza.docx': 'Pâte à Pizza',
    'endives aux oranges.docx': 'Endives aux oranges',
    'confit d\'oignon.docx': 'Confit d\'oignon',
    'GRATIN DE POTIRON.docx': 'GRATIN DE POTIRON',
}

def clean_text(text):
    text = re.sub(r'\n{3,}', '\n\n', text)
    text = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f]', '', text)
    return text.strip()

def extract_name(text, filename):
    # Check if we have a manual fix
    if filename in RECIPE_NAME_FIXES:
        return RECIPE_NAME_FIXES[filename]
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Try first 5 lines for a good name
    for i, line in enumerate(lines[:5]):
        l = line.strip()
        if len(l) < 3 or len(l) > 100:
            continue
        
        l_lower = l.lower()
        
        # Skip equipment/utensils that start with numbers
        if re.match(r'^\d+\s+(casserole|saladier|fouet|moule|plat|cuillère|verre|grosses?)', l_lower):
            continue
        
        # Skip generic headers
        skip_words = ['ingrédients', 'ingredients', 'préparation', 'preparation', 'pour', 'matériel', 
                      'methode', 'méthode', 'temps', 'quantité', 'coût', 'niveau', 'facile', 'moyen',
                      'difficile', 'portion', 'personnes', 'personne', 'min', 'mn', 'heure', 'étoiles',
                      'cuisson', 'description']
        if any(s in l_lower for s in skip_words):
            continue
            
        # Skip if starts with number + unit
        if re.match(r'^\d+[,.\s]*\s*(g|cl|ml|cuillères?|c\.à|c\.à\.s|c\.à\.c|kg|grs?|litres?)', l_lower):
            continue
        
        # Skip if starts with "Etape"
        if l_lower.startswith('etape') or l_lower.startswith('étape'):
            continue
        
        # Clean up
        l = re.sub(r'^pour\s+', '', l, flags=re.IGNORECASE).strip()
        
        if len(l) >= 3:
            return l
    
    # Fallback to filename
    return filename.replace('.docx', '').replace('.doc', '').replace('.odt', '').replace('_', ' ').strip()

def extract_ingredients(text):
    ingredients = []
    lines = text.split('\n')
    
    in_ingredients = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        if re.search(r'^ingr[eé]dients', stripped.lower()):
            in_ingredients = True
            continue
        
        if re.search(r'^(pr[eé]paration|pr[eé]paration\s*:|methode|méthode|realisation|réalisation)', stripped.lower()):
            if in_ingredients:
                break
        
        if in_ingredients and stripped:
            if stripped.lower() in ['pour', 'matériel', 'garniture', 'béchamel']:
                continue
            ingredients.append(stripped)
    
    return ingredients

def extract_instructions(text):
    instructions = []
    lines = text.split('\n')
    
    in_prep = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        if re.search(r'^(pr[eé]paration|pr[eé]paration\s*:|methode|méthode|realisation|réalisation)', stripped.lower()):
            in_prep = True
            continue
        
        if re.search(r'^(suggestions?|conseils?|note|remarques?|astuces?)', stripped.lower()):
            if in_prep:
                break
        
        if in_prep and stripped:
            instructions.append(stripped)
    
    return instructions

def extract_suggestions(text):
    suggestions = []
    lines = text.split('\n')
    
    in_suggestions = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        if re.search(r'^(suggestions?\s*(et|\&)?\s*conseils?|conseils?|notes?|astuces?)', stripped.lower()):
            in_suggestions = True
            continue
        
        if in_suggestions and stripped:
            clean = re.sub(r'^[\s•\-◦\*]+', '', stripped)
            if clean:
                suggestions.append(clean)
    
    return suggestions

def extract_servings(text):
    for pattern in [
        r'pour\s+(\d+)\s*(?:personnes?|pers?)',
        r'(\d+)\s*(?:personnes?|pers?)',
        r'(?:quantité|quantite)\s*:\s*(\d+)',
    ]:
        match = re.search(pattern, text.lower()[:300])
        if match:
            n = int(match.group(1))
            if 1 <= n <= 50:
                return n
    return None

def extract_times(text):
    times = {}
    match = re.search(r'pr[eé]paration\s*[:\-]?\s*(\d+)\s*(?:min|mn)', text.lower())
    if match:
        times['prep_time_min'] = int(match.group(1))
    match = re.search(r'cuisson\s*[:\-]?\s*(\d+)\s*(?:min|mn)', text.lower())
    if match:
        times['cook_time_min'] = int(match.group(1))
    return times

def extract_difficulty(text):
    if 'facile' in text.lower():
        return 'Easy'
    elif 'moyen' in text.lower() or 'modéré' in text.lower():
        return 'Medium'
    elif 'difficile' in text.lower():
        return 'Hard'
    return None

def parse_recipe(item):
    text = clean_text(item['text'])
    
    if len(text) < 50:
        return None
    
    name = extract_name(text, item['file'])
    ingredients = extract_ingredients(text)
    instructions = extract_instructions(text)
    suggestions = extract_suggestions(text)
    servings = extract_servings(text)
    times = extract_times(text)
    difficulty = extract_difficulty(text)
    
    metadata = {}
    if times:
        metadata.update(times)
    if difficulty:
        metadata['difficulty'] = difficulty
    
    return {
        'name': name,
        'category': item.get('category', 'Unknown'),
        'file': item['file'],
        'servings': servings,
        'ingredients': ingredients,
        'instructions': instructions,
        'suggestions': suggestions,
        'metadata': metadata if metadata else None,
        'raw_text': text
    }

def is_binary_garbage(text):
    if '\x00' in text[:1000]:
        return True
    printable = sum(1 for c in text[:500] if c.isprintable() or c in '\n\r\t')
    if len(text[:500]) > 0 and printable / len(text[:500]) < 0.7:
        return True
    return False

def parse_menu(item):
    text = clean_text(item['text'])
    
    if len(text) < 50:
        return None
    
    # Handle binary .doc files
    if is_binary_garbage(text):
        readable_parts = []
        for line in text.split('\n'):
            line = line.strip()
            if len(line) > 10 and all(ord(c) >= 32 or c in '\n\r\t' for c in line):
                readable_parts.append(line)
        if readable_parts:
            text = '\n'.join(readable_parts)
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    # Get name from first readable line or filename
    name = None
    for line in lines[:15]:
        if len(line) > 3 and all(ord(c) >= 32 or c in '\n\r\t' for c in line):
            if not any(ord(c) > 127 for c in line[:20]):
                name = line[:80]
                break
    
    if not name or len(name) < 3 or any(ord(c) > 127 for c in name[:10]):
        name = item['file'].replace('.docx', '').replace('.doc', '').replace('_', ' ')
    
    name = re.sub(r'^(menus?|réveillon|repas)\s+', '', name, flags=re.IGNORECASE).strip()
    
    menu_items = []
    for line in lines[1:]:
        line = line.strip()
        if re.match(r'^\d+[,.]\d+', line):
            continue
        if 'total' in line.lower():
            continue
        if len(line) < 3:
            continue
        if any(ord(c) < 32 and c not in '\n\r\t' for c in line):
            continue
        menu_items.append(line)
    
    event_type = None
    text_lower = text.lower()
    if 'mariage' in text_lower:
        event_type = 'Wedding'
    elif 'noël' in text_lower or 'reveillon' in text_lower or 'sylvestre' in text_lower:
        event_type = 'Christmas/New Year'
    elif 'anniversaire' in text_lower:
        event_type = 'Birthday'
    elif 'repas' in text_lower:
        event_type = 'Dinner'
    elif 'deuil' in text_lower:
        event_type = 'Funeral'
    
    guests = None
    match = re.search(r'(\d+)\s*(?:personnes?|pers?)', text.lower())
    if match:
        n = int(match.group(1))
        if 1 <= n <= 500:
            guests = n
    
    return {
        'name': name,
        'file': item['file'],
        'event_type': event_type,
        'guests': guests,
        'menu_items': menu_items,
        'raw_text': text
    }

# Parse all
parsed_recipes = [parse_recipe(r) for r in recipes_raw if parse_recipe(r)]
parsed_menus = [parse_menu(m) for m in menus_raw if parse_menu(m)]

# Count by category
from collections import Counter
cats = Counter([r['category'] for r in parsed_recipes])

# Show final results
print("=== BATCH 4 FINAL RESULTS ===")
print(f"Recipes: {len(parsed_recipes)}")
print(f"Menus: {len(parsed_menus)}")

print(f"\nCategories:")
for cat, count in cats.most_common():
    print(f"  {cat}: {count}")

print(f"\n=== ALL RECIPES ===")
for r in parsed_recipes:
    servings = f" ({r['servings']} pers)" if r['servings'] else ""
    print(f"  - {r['name'][:70]}{servings} [{r['category']}]")

print(f"\n=== ALL MENUS ===")
for m in parsed_menus:
    guests = f" ({m['guests']} guests)" if m['guests'] else ""
    event = f" [{m['event_type']}]" if m['event_type'] else ""
    print(f"  - {m['name'][:70]}{guests}{event}")

# Build output
output = {
    'batch_info': {
        'batch': 'batch_4',
        'title': 'Recipes and Home Documents',
        'description': 'French cuisine recipes and event menus from family collection',
        'total_recipes': len(parsed_recipes),
        'total_menus': len(parsed_menus),
        'categories': dict(cats),
        'extraction_date': '2026-07-16',
        'language': 'French'
    },
    'recipes': parsed_recipes,
    'menus': parsed_menus
}

with open('ingestion_batch_4.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

size = len(json.dumps(output, ensure_ascii=False))
print(f"\n✅ Saved to ingestion_batch_4.json ({size:,} chars)")
print(f"   Recipes: {len(parsed_recipes)}")
print(f"   Menus: {len(parsed_menus)}")
