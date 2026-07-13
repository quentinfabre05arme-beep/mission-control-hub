"""
Buffer API Integration for X/Twitter posting
"""
import os
import json
import requests
from datetime import datetime, timezone

BUFFER_API_BASE = "https://api.bufferapp.com/1"
API_TOKEN = "NWlmHWsSm_sRCe_sDVRhCn28mO-ydBTBN-r8txORcUU"

def get_profiles():
    """Get connected social profiles"""
    url = f"{BUFFER_API_BASE}/profiles.json?access_token={API_TOKEN}"
    response = requests.get(url)
    
    if response.status_code == 200:
        profiles = response.json()
        return profiles
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def create_post(text, profile_ids, scheduled_at=None):
    """Create a new post"""
    url = f"{BUFFER_API_BASE}/updates/create.json"
    
    data = {
        'access_token': API_TOKEN,
        'text': text,
        'profile_ids[]': profile_ids if isinstance(profile_ids, list) else [profile_ids]
    }
    
    if scheduled_at:
        data['scheduled_at'] = scheduled_at.isoformat()
    
    response = requests.post(url, data=data)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        print(response.text)
        return None

def get_pending_posts(profile_id=None):
    """Get pending/scheduled posts"""
    if profile_id:
        url = f"{BUFFER_API_BASE}/profiles/{profile_id}/updates/pending.json?access_token={API_TOKEN}"
    else:
        url = f"{BUFFER_API_BASE}/updates/pending.json?access_token={API_TOKEN}"
    
    response = requests.get(url)
    
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error: {response.status_code}")
        return None

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python buffer_poster.py [command] [args]")
        print("Commands: profiles, post, pending")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'profiles':
        print("Fetching profiles...")
        profiles = get_profiles()
        if profiles:
            print(f"\nFound {len(profiles)} profile(s):\n")
            for p in profiles:
                print(f"  - {p['formatted_username']} (ID: {p['id']})")
                print(f"    Service: {p['service']}")
                print(f"    Connected: {p.get('counts', {}).get('followers', 'N/A')} followers")
                print()
    
    elif command == 'post':
        if len(sys.argv) < 4:
            print("Usage: python buffer_poster.py post 'Your post text' profile_id")
            sys.exit(1)
        
        text = sys.argv[2]
        profile_id = sys.argv[3]
        
        print(f"Creating post: {text[:50]}...")
        result = create_post(text, profile_id)
        
        if result and 'id' in result:
            print(f"✅ Post created successfully!")
            print(f"   Post ID: {result['id']}")
            print(f"   Status: {result.get('status', 'unknown')}")
        else:
            print("❌ Failed to create post")
    
    elif command == 'pending':
        print("Fetching pending posts...")
        posts = get_pending_posts()
        if posts:
            print(f"\n{len(posts)} pending post(s):\n")
            for post in posts:
                print(f"  - {post['text'][:50]}...")
                print(f"    Status: {post.get('status', 'unknown')}")
                print()
