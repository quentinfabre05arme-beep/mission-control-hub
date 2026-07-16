import json, re
from collections import Counter

# Load raw extraction
with open('ingestion_batch_4_raw.json', 'r', encoding='utf-8') as f:
    raw_data = json.load(f)

print(f"Root keys: {list(raw_data.keys())}")
print(f"Recipes count: {len(raw_data.get('recipes', []))}")
print(f"Menus count: {len(raw_data.get('menus', []))}")

recipes_raw = raw_data['recipes']
menus_raw = raw_data['menus']

def extract_name_from_first_lines(text):
    """Extract recipe name from first meaningful lines"""
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    for line in lines[:3]:
        # Skip generic headers
        if line.lower() in ['ingrédients', 'ingredients', 'préparation', 'preparation', 'pour', 'matériel']:
            continue
        # Skip metadata lines (times, ratings, etc.)
        if re.match(r'^(\d+\s*(min|mn|h|heures?)|\d+\.\d+.*étoiles?|quantité|coût|niveau|facile|moyen|difficile)', line.lower()):
            continue
        # Skip lines that look like ingredient quantities
        if re.match(r'^\d+\s*(g|cl|ml|cuillères?|c\.à)', line.lower()):
            continue
        return line
    
    return lines[0] if lines else 'Unknown Recipe'

def extract_ingredients(text):
    """Extract ingredients section from recipe text"""
    ingredients = []
    lines = text.split('\n')
    
    in_ingredients = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Detect ingredients section start
        if re.search(r'^ingr[eé]dients', stripped.lower()):
            in_ingredients = True
            continue
        
        # Detect preparation section end
        if re.search(r'^(pr[eé]paration|pr[eé]paration\s*:)', stripped.lower()):
            if in_ingredients:
                break
        
        if in_ingredients and stripped:
            # Skip section headers within ingredients
            if stripped.lower() in ['pour', 'matériel']:
                continue
            ingredients.append(stripped)
    
    return ingredients

def extract_instructions(text):
    """Extract numbered preparation steps"""
    instructions = []
    lines = text.split('\n')
    
    in_prep = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        # Detect preparation start
        if re.search(r'^(pr[eé]paration|pr[eé]paration\s*:)', stripped.lower()):
            in_prep = True
            continue
        
        # Detect end of preparation (suggestions, notes, etc.)
        if re.search(r'^(suggestions?|conseils?|note|remarques?|astuces?)', stripped.lower()):
            if in_prep:
                break
        
        if in_prep and stripped:
            instructions.append(stripped)
    
    return instructions

def extract_suggestions(text):
    """Extract suggestions and tips section"""
    suggestions = []
    lines = text.split('\n')
    
    in_suggestions = False
    for line in lines:
        stripped = line.strip()
        if not stripped:
            continue
        
        if re.search(r'^(suggestions?\s*(et|&)?\s*conseils?|conseils?|notes?|astuces?)', stripped.lower()):
            in_suggestions = True
            continue
        
        if in_suggestions and stripped:
            # Skip bullet markers
            clean = re.sub(r'^[\s•\-◦\*]+', '', stripped)
            if clean:
                suggestions.append(clean)
    
    return suggestions

def extract_metadata(text):
    """Extract cooking metadata (time, difficulty, cost)"""
    metadata = {}
    lines = text.split('\n')
    
    for line in lines[:10]:
        stripped = line.strip().lower()
        
        # Time
        if re.search(r'(pr[eé]paration\s*[:\-]?\s*\d+)', stripped):
            match = re.search(r'(\d+)\s*(min|mn)', stripped)
            if match:
                metadata['prep_time_min'] = int(match.group(1))
        
        if re.search(r'(cuisson\s*[:\-]?\s*\d+)', stripped):
            match = re.search(r'(\d+)\s*(min|mn)', stripped)
            if match:
                metadata['cook_time_min'] = int(match.group(1))
        
        # Difficulty
        if 'facile' in stripped:
            metadata['difficulty'] = 'Easy'
        elif 'moyen' in stripped or 'modéré' in stripped:
            metadata['difficulty'] = 'Medium'
        elif 'difficile' in stripped:
            metadata['difficulty'] = 'Hard'
        
        # Cost
        if 'pas cher' in stripped or 'économique' in stripped:
            metadata['cost_level'] = 'Low'
        elif 'moyen' in stripped and 'coût' in stripped:
            metadata['cost_level'] = 'Medium'
        elif 'cher' in stripped:
            metadata['cost_level'] = 'High'
    
    return metadata

def parse_recipe(item):
    text = item['text']
    name = extract_name_from_first_lines(text)
    ingredients = extract_ingredients(text)
    instructions = extract_instructions(text)
    suggestions = extract_suggestions(text)
    metadata = extract_metadata(text)
    
    # Detect servings from text
    servings = None
    match = re.search(r'(?:pour\s+)(\d+)\s*(personnes?|pers?)', text.lower())
    if match:
        servings = int(match.group(1))
    
    return {
        'name': name,
        'category': item['category'],
        'file': item['file'],
        'servings': servings,
        'ingredients': ingredients,
        'instructions': instructions,
        'suggestions': suggestions,
        'metadata': metadata,
        'raw_text': text
    }

def parse_menu(item):
    text = item['text']
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    
    name = lines[0] if lines else item['file'].replace('.docx', '')
    
    # Extract menu items (lines that look like meals)
    menu_items = []
    for line in lines[1:]:
        # Skip header lines
        if line.lower() in ['ingrédients', 'préparation', 'matériel']:
            continue
        # Skip quantity lines
        if re.match(r'^\d+\s*(g|cl|ml|cuillère)', line.lower()):
            continue
        menu_items.append(line)
    
    return {
        'name': name,
        'file': item['file'],
        'items': menu_items,
        'raw_text': text
    }

# Parse all
parsed_recipes = [parse_recipe(r) for r in recipes_raw]
parsed_menus = [parse_menu(m) for m in menus_raw]

# Show stats
print(f"\n=== RECIPES ({len(parsed_recipes)}) ===")
for r in parsed_recipes[:5]:
    print(f"\n{r['name']}")
    print(f"  Category: {r['category']}")
    print(f"  Servings: {r['servings']}")
    print(f"  Ingredients: {len(r['ingredients'])}")
    print(f"  Instructions: {len(r['instructions'])}")
    if r['suggestions']:
        print(f"  Suggestions: {len(r['suggestions'])}")
    if r['metadata']:
        print(f"  Metadata: {r['metadata']}")

print(f"\n=== MENUS ({len(parsed_menus)}) ===")
for m in parsed_menus[:3]:
    print(f"\n{m['name']}")
    print(f"  Items: {len(m['items'])}")
    print(f"  Sample: {m['items'][:3]}")

# Category breakdown
cats = Counter([r['category'] for r in parsed_recipes])
print(f"\n=== CATEGORIES ===")
for cat, count in cats.most_common():
    print(f"  {cat}: {count}")

# Save structured data
output = {
    'batch_info': raw_data['batch_info'],
    'recipes': parsed_recipes,
    'menus': parsed_menus
}

with open('ingestion_batch_4.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"\n✅ Saved to ingestion_batch_4.json ({len(json.dumps(output))} chars)")
