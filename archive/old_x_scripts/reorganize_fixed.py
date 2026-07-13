#!/usr/bin/env python3
"""OneDrive file reorganization script - Fixed for file/directory conflicts"""

import os
import json
import shutil
import subprocess
from pathlib import Path
from datetime import datetime, timedelta

# Configuration
SOURCE_DIR = Path(r"C:\Users\quent\OneDrive\Documents")
DEST_ROOT = Path(r"C:\Users\quent\OneDrive")
PROGRESS_FILE = Path(r"C:\Users\quent\.openclaw\workspace\ONEDRIVE_REORG_PROGRESS.json")
BATCH_SIZE = 500
TOTAL_TARGET = 45000

# Destination mappings - Using alternate names to avoid file/directory conflicts
DESTINATIONS = {
    'PDF': DEST_ROOT / "08-REFERENCE" / "PDFs",
    'Image': DEST_ROOT / "06-MEDIA" / "Photos",
    'Video': DEST_ROOT / "06-MEDIA" / "Videos",
    'Audio': DEST_ROOT / "06-MEDIA" / "Audio",
    'Word': DEST_ROOT / "03-DOCUMENTS" / "WordDocs",
    'Code': DEST_ROOT / "07-DEVELOPMENT" / "CodeFiles",
    'Archive': DEST_ROOT / "04-ARCHIVES" / "Files",
    'Other': DEST_ROOT / "04-ARCHIVES" / "Misc",
}

# File extension mappings
TYPE_MAP = {
    '.pdf': 'PDF',
    '.jpg': 'Image', '.jpeg': 'Image', '.png': 'Image', '.gif': 'Image', '.bmp': 'Image',
    '.tiff': 'Image', '.tif': 'Image', '.webp': 'Image', '.svg': 'Image', '.ico': 'Image',
    '.raw': 'Image', '.cr2': 'Image', '.nef': 'Image', '.heic': 'Image', '.heif': 'Image',
    '.mp4': 'Video', '.mov': 'Video', '.avi': 'Video', '.mkv': 'Video', '.wmv': 'Video',
    '.flv': 'Video', '.webm': 'Video', '.m4v': 'Video', '.mpg': 'Video', '.mpeg': 'Video',
    '.3gp': 'Video', '.ts': 'Video', '.m2ts': 'Video',
    '.mp3': 'Audio', '.wav': 'Audio', '.flac': 'Audio', '.aac': 'Audio', '.ogg': 'Audio',
    '.wma': 'Audio', '.cda': 'Audio', '.m4a': 'Audio',
    '.doc': 'Word', '.docx': 'Word', '.odt': 'Word', '.rtf': 'Word', '.txt': 'Word',
    '.md': 'Word', '.xls': 'Word', '.xlsx': 'Word', '.xlsb': 'Word', '.ods': 'Word',
    '.ppt': 'Word', '.pptx': 'Word', '.odp': 'Word', '.csv': 'Word', '.epub': 'Word',
    '.zip': 'Archive', '.rar': 'Archive', '.7z': 'Archive', '.tar': 'Archive',
    '.gz': 'Archive', '.bz2': 'Archive',
}

CODE_EXTS = {
    '.py', '.js', '.ts', '.html', '.htm', '.css', '.scss', '.json', '.xml', '.yaml', '.yml',
    '.sql', '.sh', '.ps1', '.bat', '.cmd', '.java', '.c', '.cpp', '.h', '.hpp', '.cs', '.go',
    '.php', '.rb', '.pl', '.lua', '.r', '.scala', '.kt', '.dart', '.vue', '.jsx', '.tsx',
    '.ipynb', '.dockerfile', '.tf', '.gradle', '.pom', '.sln', '.csproj', '.config', '.ini',
    '.conf', '.env', '.lock', '.gitignore', '.as2', '.flipchart', '.profile', '.ocd', '.mod',
}

# Exclude folders
EXCLUDE_FOLDERS = {'08-REFERENCE', '06-MEDIA', '03-DOCUMENTS', '07-DEVELOPMENT',
                   '00-INBOX', '01-ACTIF', '02-RESSOURCES', '04-ARCHIVES',
                   '05-PERSONNEL', '99-LOGS', 'PDFs', 'WordDocs', 'CodeFiles',
                   'Photos', 'Videos', 'Audio', 'Files', 'Misc'}

def ensure_dirs():
    """Create destination directories, handling file/directory conflicts"""
    for dest in DESTINATIONS.values():
        try:
            if dest.exists() and not dest.is_dir():
                # If a file exists with the same name, rename it
                backup_name = dest.parent / f"{dest.name}.backup"
                counter = 1
                while backup_name.exists():
                    backup_name = dest.parent / f"{dest.name}.backup{counter}"
                    counter += 1
                os.rename(str(dest), str(backup_name))
                print(f"Renamed conflicting file: {dest} -> {backup_name}")
            os.makedirs(str(dest), exist_ok=True)
        except Exception as e:
            print(f"Warning: Could not create {dest}: {e}")

def get_file_type(ext):
    """Determine file type from extension"""
    ext_lower = ext.lower()
    if ext_lower in TYPE_MAP:
        return TYPE_MAP[ext_lower]
    if ext_lower in CODE_EXTS:
        return 'Code'
    return 'Other'

def sanitize_filename(name):
    """Clean filename for safe filesystem use"""
    invalid = '<>"/\\|?*'
    for char in invalid:
        name = name.replace(char, '_')
    return name

def get_files_to_process():
    """Get list of files to move"""
    files = []
    for root, dirs, filenames in os.walk(SOURCE_DIR):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if d not in EXCLUDE_FOLDERS]
        
        for filename in filenames:
            filepath = Path(root) / filename
            files.append(filepath)
    
    return files[:BATCH_SIZE]

def move_file(src, dest_dir, filename):
    """Move file using multiple strategies"""
    try:
        # Ensure destination directory exists
        if not os.path.exists(str(dest_dir)):
            os.makedirs(str(dest_dir), exist_ok=True)
        
        dest_path = dest_dir / filename
        
        # Handle duplicates by appending number
        counter = 1
        original_name = filename
        while os.path.exists(str(dest_path)):
            name, ext = os.path.splitext(original_name)
            filename = f"{name}_{counter}{ext}"
            dest_path = dest_dir / filename
            counter += 1
        
        # Try multiple move strategies
        # Strategy 1: Direct rename (atomic, fastest)
        try:
            os.rename(str(src), str(dest_path))
            return True
        except OSError:
            pass
        
        # Strategy 2: Copy then delete
        try:
            shutil.copy2(str(src), str(dest_path))
            os.remove(str(src))
            return True
        except Exception:
            pass
        
        # Strategy 3: Use robocopy for stubborn files
        try:
            cmd = ['robocopy', str(src.parent), str(dest_dir), src.name, '/MOV', '/R:3', '/W:1']
            result = subprocess.run(cmd, capture_output=True, text=True, shell=False)
            if not src.exists():
                return True
        except:
            pass
            
        return False
        
    except Exception as e:
        print(f"Error moving {src}: {e}")
        return False

def load_progress():
    """Load progress from JSON file"""
    if PROGRESS_FILE.exists():
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {
        'total_processed': 800,
        'current_batch': 0,
        'batches': [],
        'started': datetime.now().isoformat(),
        'total_target': TOTAL_TARGET,
        'status': 'running'
    }

def save_progress(progress):
    """Save progress to JSON file"""
    PROGRESS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=2)

def process_batch():
    """Process a batch of files"""
    ensure_dirs()
    progress = load_progress()
    
    files = get_files_to_process()
    if not files:
        print("No more files to process!")
        progress['status'] = 'completed'
        progress['estimated_completion'] = datetime.now().isoformat()
        save_progress(progress)
        return 0
    
    stats = {'PDF': 0, 'Image': 0, 'Video': 0, 'Audio': 0, 'Word': 0, 
             'Code': 0, 'Archive': 0, 'Other': 0, 'Errors': 0}
    moved = []
    
    print(f"Processing {len(files)} files...")
    start_time = datetime.now()
    
    for filepath in files:
        try:
            ext = filepath.suffix.lower()
            file_type = get_file_type(ext)
            
            dest_dir = DESTINATIONS[file_type]
            
            # Get parent folder name for organization
            try:
                rel_path = filepath.parent.relative_to(SOURCE_DIR)
                if rel_path == Path('.'):
                    subfolder = 'Root'
                else:
                    subfolder = rel_path.parts[0]
            except:
                subfolder = 'Root'
            
            target_dir = dest_dir / subfolder
            
            # Clean filename
            clean_filename = sanitize_filename(filepath.name)
            
            # Move file
            success = move_file(filepath, target_dir, clean_filename)
            
            if success:
                moved.append(str(filepath))
                stats[file_type] += 1
            else:
                stats['Errors'] += 1
                    
        except Exception as e:
            stats['Errors'] += 1
            print(f"Error processing {filepath}: {e}")
    
    duration = (datetime.now() - start_time).total_seconds()
    
    # Update progress
    progress['current_batch'] += 1
    progress['total_processed'] += len(moved)
    
    batch_entry = {
        'batch_number': progress['current_batch'],
        'timestamp': datetime.now().isoformat(),
        'files_moved': len(moved),
        'stats': stats
    }
    progress['batches'].append(batch_entry)
    
    # Calculate ETA
    remaining = TOTAL_TARGET - progress['total_processed']
    if len(moved) > 0 and duration > 0:
        rate = len(moved) / duration
        remaining_batches = remaining / BATCH_SIZE
        eta_seconds = remaining_batches * duration
        eta = datetime.now() + timedelta(seconds=eta_seconds)
        progress['estimated_completion'] = eta.isoformat()
    
    progress['last_update'] = datetime.now().isoformat()
    save_progress(progress)
    
    # Print summary
    print(f"\n=== BATCH {progress['current_batch']} COMPLETE ===")
    print(f"Moved: {len(moved)} files in {duration:.1f}s")
    for k, v in sorted(stats.items()):
        if v > 0:
            print(f"  {k}: {v}")
    print(f"Total: {progress['total_processed']} / {TOTAL_TARGET}")
    print(f"ETA: {progress.get('estimated_completion', 'N/A')}")
    
    return len(moved)

def process_all_batches():
    """Process multiple batches until complete"""
    total_batches = 0
    max_batches = 100  # Safety limit
    
    while total_batches < max_batches:
        count = process_batch()
        total_batches += 1
        
        if count == 0:
            print("\n=== ALL FILES PROCESSED ===")
            break
            
        # Check if we've reached target
        progress = load_progress()
        if progress['total_processed'] >= TOTAL_TARGET:
            print(f"\n=== TARGET REACHED: {progress['total_processed']} files ===")
            progress['status'] = 'completed'
            save_progress(progress)
            break
    
    return total_batches

if __name__ == '__main__':
    import sys
    
    # Check if we should run single batch or all
    if len(sys.argv) > 1 and sys.argv[1] == '--all':
        batches = process_all_batches()
        print(f"Completed {batches} batches")
    else:
        count = process_batch()
        print(f"Batch complete: {count} files moved")
