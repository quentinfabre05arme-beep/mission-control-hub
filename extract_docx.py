#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract text from .docx files using zip/XML extraction (no external deps)."""
import zipfile
import xml.etree.ElementTree as ET
import json
import os
import sys
import io

# Fix encoding for Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


def extract_docx_text(filepath):
    """Extract all text from a .docx file."""
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            xml_content = z.read('word/document.xml')
        tree = ET.fromstring(xml_content)
        paragraphs = []
        for p in tree.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p'):
            texts = []
            for t in p.iter('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t'):
                if t.text:
                    texts.append(t.text)
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"ERROR: {e}"


def extract_odt_text(filepath):
    """Extract text from .odt files."""
    try:
        with zipfile.ZipFile(filepath, 'r') as z:
            xml_content = z.read('content.xml')
        tree = ET.fromstring(xml_content)
        paragraphs = []
        for p in tree.iter('{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p'):
            texts = []
            for t in p.iter():
                if t.text and t.text.strip():
                    texts.append(t.text)
            if texts:
                paragraphs.append(''.join(texts))
        return '\n'.join(paragraphs)
    except Exception as e:
        return f"ERROR: {e}"


def extract_doc_text(filepath):
    """For .doc files, try basic extraction."""
    try:
        with open(filepath, 'rb') as f:
            raw = f.read()
        text = raw.decode('latin-1', errors='ignore')
        lines = [line.strip() for line in text.split('\n') if line.strip() and len(line.strip()) > 2]
        return '\n'.join(lines[:100])
    except Exception as e:
        return f"ERROR: {e}"


def extract_file_text(filepath):
    ext = os.path.splitext(filepath)[1].lower()
    if ext == '.docx':
        return extract_docx_text(filepath)
    elif ext == '.odt':
        return extract_odt_text(filepath)
    elif ext == '.doc':
        return extract_doc_text(filepath)
    else:
        return "UNSUPPORTED FORMAT"


def main():
    base = r"C:\Users\quent\OneDrive"
    
    # Find the Home-Life folder with emoji prefix
    all_dirs = os.listdir(base)
    home_life_folders = [d for d in all_dirs if 'Home-Life' in d]
    print("Found Home-Life folders:", repr(home_life_folders))
    
    if not home_life_folders:
        print("ERROR: No Home-Life folder found")
        return
    
    # Use the emoji-prefixed one (??-Home-Life)
    target = [d for d in home_life_folders if d.startswith('\U0001f3e0')]
    if not target:
        target = home_life_folders
    
    home_life = os.path.join(base, target[0], "Bureau-Autres", "ROGER")
    print("Using path:", repr(home_life))
    print("Exists:", os.path.exists(home_life))
    
    # 1. RECETTES CUISINE
    recipe_paths = []
    recipe_base = os.path.join(home_life, "RECETTES CUISINE")
    print("Recipe base:", repr(recipe_base))
    print("Recipe base exists:", os.path.exists(recipe_base))
    
    if os.path.exists(recipe_base):
        for root, dirs, files in os.walk(recipe_base):
            for f in files:
                if f.lower().endswith(('.docx', '.doc', '.odt')):
                    full_path = os.path.join(root, f)
                    recipe_paths.append(full_path)
                    print("  Found recipe:", repr(f))

    # 2. MENUS
    menu_paths = []
    menu_base = os.path.join(home_life, "VIE PROFESSIONNELLE", "VACANCES ET LOISIRS", "economat", "MENUS")
    print("Menu base:", repr(menu_base))
    print("Menu base exists:", os.path.exists(menu_base))
    
    if os.path.exists(menu_base):
        for root, dirs, files in os.walk(menu_base):
            for f in files:
                if f.lower().endswith(('.docx', '.doc', '.odt')):
                    full_path = os.path.join(root, f)
                    menu_paths.append(full_path)
                    print("  Found menu:", repr(f))

    results = {
        "batch_info": {
            "batch": "batch_4",
            "title": "Recipes and Home Documents",
            "paths_scanned": ["RECETTES CUISINE", "MENUS", "Home-Life"],
            "excluded": ["bills/admin", "CHARGES", "DEPENSES", "EDF", "MEDIATHEQUE", "POLE EMPLOI", "TABLATURES", "TOYOTA", "VIE PROFESSIONNELLE (non-menu)"],
            "total_files": 0
        },
        "recipes": [],
        "menus": [],
        "errors": []
    }

    # Process recipes
    for fp in recipe_paths:
        print("Processing recipe:", repr(os.path.basename(fp)))
        text = extract_file_text(fp)
        category = os.path.basename(os.path.dirname(fp))
        results["recipes"].append({
            "file": os.path.basename(fp),
            "path": fp,
            "category": category,
            "text": text[:8000] if len(text) > 8000 else text
        })

    # Process menus
    for fp in menu_paths:
        print("Processing menu:", repr(os.path.basename(fp)))
        text = extract_file_text(fp)
        results["menus"].append({
            "file": os.path.basename(fp),
            "path": fp,
            "text": text[:8000] if len(text) > 8000 else text
        })

    results["batch_info"]["total_files"] = len(recipe_paths) + len(menu_paths)
    results["batch_info"]["recipe_count"] = len(recipe_paths)
    results["batch_info"]["menu_count"] = len(menu_paths)

    out_path = r"C:\Users\quent\.openclaw\workspace\ingestion_batch_4_raw.json"
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\nExtracted", len(recipe_paths), "recipes and", len(menu_paths), "menus to", out_path)


if __name__ == '__main__':
    main()
