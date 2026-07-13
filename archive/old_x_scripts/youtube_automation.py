#!/usr/bin/env python3
"""
YouTube Automation System
Monitors 25 subscribed channels, extracts transcripts, generates summaries
Daily check at 9:00 AM - Sends digest to Telegram
"""

import json
import re
import urllib.request
from datetime import datetime, timedelta
from pathlib import Path
from xml.etree import ElementTree as ET

# Telegram configuration
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"

try:
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter
except ImportError:
    import subprocess
    subprocess.run(["pip", "install", "youtube-transcript-api", "-q"], check=True)
    from youtube_transcript_api import YouTubeTranscriptApi
    from youtube_transcript_api.formatters import TextFormatter


class YouTubeAutomation:
    """YouTube channel monitoring and transcript automation"""
    
    VERSION = "2.0"
    TARGET_CHANNELS = 25
    
    def __init__(self):
        self.workspace = Path("C:/Users/quent/.openclaw/workspace")
        self.youtube_dir = self.workspace / "youtube_content"
        self.channels_file = self.youtube_dir / "channels.json"
        self.summaries_dir = self.youtube_dir / "summaries"
        self.transcripts_dir = self.youtube_dir / "transcripts"
        self.progress_file = self.youtube_dir / "progress.json"
        
        # Ensure directories exist
        for d in [self.youtube_dir, self.summaries_dir, self.transcripts_dir]:
            d.mkdir(exist_ok=True, parents=True)
        
        self.load_channels()
        self.load_progress()
    
    def load_channels(self):
        """Load channels from file"""
        if self.channels_file.exists():
            with open(self.channels_file, 'r', encoding='utf-8') as f:
                self.channels = json.load(f)
        else:
            self.channels = {}
    
    def save_channels(self):
        """Save channels to file"""
        with open(self.channels_file, 'w', encoding='utf-8') as f:
            json.dump(self.channels, f, indent=2)
    
    def load_progress(self):
        """Load progress tracking"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                self.progress = json.load(f)
        else:
            self.progress = {
                "total_runs": 0,
                "last_run": None,
                "videos_processed": 0,
                "channels_checked": 0,
                "errors": []
            }
    
    def save_progress(self):
        """Save progress tracking"""
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(self.progress, f, indent=2)
    
    def update_progress(self, videos_count=0, channels_count=0, error=None):
        """Update progress after run"""
        self.progress["total_runs"] += 1
        self.progress["last_run"] = datetime.now().isoformat()
        self.progress["videos_processed"] += videos_count
        self.progress["channels_checked"] += channels_count
        if error:
            self.progress["errors"].append({
                "time": datetime.now().isoformat(),
                "message": str(error)
            })
            # Keep only last 10 errors
            self.progress["errors"] = self.progress["errors"][-10:]
        self.save_progress()
    
    def get_channel_feed(self, channel_id):
        """Get RSS feed for channel"""
        rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
        
        try:
            req = urllib.request.Request(
                rss_url,
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
            )
            with urllib.request.urlopen(req, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            print(f"[ERROR] Cannot fetch RSS for {channel_id}: {e}")
            return None
    
    def parse_feed(self, feed_xml):
        """Parse RSS feed and extract video info"""
        if not feed_xml:
            return []
        
        try:
            root = ET.fromstring(feed_xml)
            ns = {'atom': 'http://www.w3.org/2005/Atom'}
            
            videos = []
            for entry in root.findall('atom:entry', ns):
                video = {}
                
                # Title
                title = entry.find('atom:title', ns)
                video['title'] = title.text if title is not None else "Unknown"
                
                # Video ID
                video_id = entry.find('atom:id', ns)
                if video_id is not None:
                    match = re.search(r'video:([a-zA-Z0-9_-]+)', video_id.text)
                    if match:
                        video['id'] = match.group(1)
                    else:
                        continue
                else:
                    continue
                
                # Published date
                published = entry.find('atom:published', ns)
                if published is not None:
                    video['published'] = published.text
                
                # Link
                link = entry.find('atom:link', ns)
                if link is not None:
                    video['url'] = link.get('href')
                
                videos.append(video)
            
            return videos
        except Exception as e:
            print(f"[ERROR] Cannot parse RSS: {e}")
            return []
    
    def get_video_transcript(self, video_id):
        """Get transcript for video"""
        try:
            transcript_list = YouTubeTranscriptApi().fetch(video_id)
            formatter = TextFormatter()
            transcript_text = formatter.format_transcript(transcript_list)
            return transcript_text
        except Exception as e:
            print(f"[ERROR] Cannot get transcript for {video_id}: {e}")
            return None
    
    def summarize_transcript(self, transcript, title):
        """Generate summary of transcript using extractive summarization"""
        if not transcript:
            return None
        
        sentences = transcript.split('.')
        key_sentences = sentences[:5] + sentences[-3:]
        summary = '. '.join([s.strip() for s in key_sentences if len(s.strip()) > 20])
        
        if len(summary) > 800:
            summary = summary[:800] + "..."
        
        return {
            "title": title,
            "key_points": summary,
            "word_count": len(transcript.split()),
            "summary_length": len(summary)
        }
    
    def check_for_new_videos(self):
        """Check all channels for new videos from last 24 hours"""
        new_videos = []
        channels_checked = 0
        
        yesterday = datetime.now() - timedelta(days=1)
        
        for channel_name, channel_info in self.channels.items():
            print(f"[CHECK] {channel_name}...")
            channels_checked += 1
            
            feed = self.get_channel_feed(channel_info['id'])
            if feed is None:
                continue
            
            videos = self.parse_feed(feed)
            
            for video in videos:
                if 'published' in video:
                    try:
                        pub_date = datetime.fromisoformat(video['published'].replace('Z', '+00:00').replace('+00:00', ''))
                        if pub_date > yesterday:
                            new_videos.append({
                                **video,
                                'channel': channel_name,
                                'category': channel_info.get('category', 'general')
                            })
                    except Exception as e:
                        print(f"[WARN] Could not parse date for {video.get('title', 'unknown')}: {e}")
        
        return new_videos, channels_checked
    
    def process_videos(self, videos):
        """Process videos: get transcripts and summaries"""
        processed = []
        
        for video in videos:
            print(f"[PROCESS] {video['title'][:60]}...")
            
            transcript = self.get_video_transcript(video['id'])
            
            if transcript:
                # Save transcript
                transcript_file = self.transcripts_dir / f"{video['id']}.txt"
                with open(transcript_file, 'w', encoding='utf-8') as f:
                    f.write(transcript)
                
                # Generate summary
                summary = self.summarize_transcript(transcript, video['title'])
                
                if summary:
                    summary_data = {
                        **summary,
                        'video_id': video['id'],
                        'url': video.get('url', f"https://youtube.com/watch?v={video['id']}"),
                        'channel': video['channel'],
                        'category': video['category'],
                        'published': video.get('published', ''),
                        'processed_at': datetime.now().isoformat()
                    }
                    
                    # Save summary
                    summary_file = self.summaries_dir / f"{video['id']}.json"
                    with open(summary_file, 'w', encoding='utf-8') as f:
                        json.dump(summary_data, f, indent=2)
                    
                    processed.append(summary_data)
            else:
                # Save video info even without transcript
                processed.append({
                    'title': video['title'],
                    'video_id': video['id'],
                    'url': video.get('url', f"https://youtube.com/watch?v={video['id']}"),
                    'channel': video['channel'],
                    'category': video['category'],
                    'key_points': 'Transcript not available',
                    'word_count': 0
                })
        
        return processed
    
    def generate_daily_digest(self, summaries):
        """Generate daily digest from summaries"""
        if not summaries:
            return "[TV] YouTube Daily Digest\n\n_No new videos today_"
        
        today_str = datetime.now().strftime('%A, %B %d, %Y')
        
        digest = f"""[TV] YouTube Daily Digest
📅 {today_str}

Found {len(summaries)} new video(s) from {len(self.channels)} channels:

"""
        
        for i, summary in enumerate(summaries, 1):
            emoji_cat = {
                'finance': '[MONEY]', 'crypto': '[BTC]', 'business': '[BAG]',
                'philosophy': '[BRAIN]', 'productivity': '[BOLT]', 'tech': '[PC]',
                'podcast': '[MIC]', 'lifestyle': '[STAR]'
            }.get(summary.get('category', 'general'), '[VIDEO]')
            
            title = summary.get('title', 'Unknown')[:80]
            channel = summary.get('channel', 'Unknown')
            url = summary.get('url', '')
            
            key_points = summary.get('key_points', 'No summary available')
            if len(key_points) > 250:
                key_points = key_points[:250] + "..."
            
            digest += f"""{i}. {emoji_cat} {title}
   by {channel}
   
   {key_points}
   Link: {url}

"""
        
        digest += "---\nGenerated by Claw YouTube Automation"
        
        return digest
    
    def send_telegram_message(self, message):
        """Send message to Telegram"""
        if TELEGRAM_BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            print("[WARN] Telegram not configured. Message saved to file.")
            return False
        
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            data = json.dumps({
                "chat_id": TELEGRAM_CHAT_ID,
                "text": message,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }).encode('utf-8')
            
            req = urllib.request.Request(
                url,
                data=data,
                headers={'Content-Type': 'application/json'}
            )
            
            with urllib.request.urlopen(req, timeout=30) as response:
                result = json.loads(response.read().decode('utf-8'))
                return result.get('ok', False)
        except Exception as e:
            print(f"[ERROR] Failed to send Telegram message: {e}")
            return False
    
    def run_daily_check(self):
        """Run full daily check"""
        print("="*60)
        print("YouTube Automation System v2.0")
        print(f"Monitoring {len(self.channels)} channels")
        print("="*60)
        
        try:
            # Check for new videos
            new_videos, channels_checked = self.check_for_new_videos()
            print(f"\n[FOUND] {len(new_videos)} new video(s)")
            
            # Process videos
            summaries = self.process_videos(new_videos)
            
            # Generate digest
            digest = self.generate_daily_digest(summaries)
            
            # Save digest
            today = datetime.now().strftime("%Y-%m-%d")
            digest_file = self.youtube_dir / f"digest_{today}.txt"
            with open(digest_file, 'w', encoding='utf-8') as f:
                f.write(digest)
            
            print(f"\n[DIGEST] Saved to {digest_file}")
            
            # Send to Telegram
            telegram_sent = self.send_telegram_message(digest)
            if telegram_sent:
                print("[TELEGRAM] Digest sent successfully")
            else:
                print("[TELEGRAM] Digest saved locally (configure token to send)")
            
            # Update progress
            self.update_progress(videos_count=len(summaries), channels_count=channels_checked)
            
            return {
                "status": "success",
                "videos_found": len(new_videos),
                "videos_processed": len(summaries),
                "channels_checked": channels_checked,
                "telegram_sent": telegram_sent,
                "digest_file": str(digest_file),
                "digest_preview": digest[:500] + "..." if len(digest) > 500 else digest
            }
            
        except Exception as e:
            self.update_progress(error=e)
            return {
                "status": "error",
                "error": str(e)
            }
    
    def add_channel(self, name, channel_id, category="general"):
        """Add new channel to monitor"""
        self.channels[name] = {
            "id": channel_id,
            "category": category
        }
        self.save_channels()
        print(f"[ADDED] Channel '{name}' ({category}) added successfully")
        print(f"        Total channels: {len(self.channels)}")
    
    def remove_channel(self, name):
        """Remove channel from monitoring"""
        if name in self.channels:
            del self.channels[name]
            self.save_channels()
            print(f"[REMOVED] Channel '{name}' removed")
            return True
        print(f"[ERROR] Channel '{name}' not found")
        return False
    
    def list_channels(self):
        """List all monitored channels"""
        print(f"\n{'='*60}")
        print(f"[TV] MONITORED CHANNELS ({len(self.channels)} total)")
        print(f"{'='*60}")
        
        categories = {}
        for name, info in self.channels.items():
            cat = info.get('category', 'general')
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(name)
        
        for cat, names in sorted(categories.items()):
            emoji = {
                'finance': '[MONEY]', 'crypto': '[BTC]', 'business': '[BAG]',
                'philosophy': '[BRAIN]', 'productivity': '[BOLT]', 'tech': '[PC]',
                'podcast': '[MIC]', 'lifestyle': '[STAR]'
            }.get(cat, '[VIDEO]')
            print(f"\n{emoji} {cat.upper()} ({len(names)})")
            for name in sorted(names):
                print(f"   - {name}")
        
        print(f"\n{'='*60}")
        print(f"Target: {self.TARGET_CHANNELS} channels | Current: {len(self.channels)}")
        print(f"Progress: {len(self.channels)}/{self.TARGET_CHANNELS} ({100*len(self.channels)//self.TARGET_CHANNELS}%)")
    
    def show_status(self):
        """Show system status"""
        print(f"\n{'='*60}")
        print("[STATS] SYSTEM STATUS")
        print(f"{'='*60}")
        print(f"Version: {self.VERSION}")
        print(f"Channels configured: {len(self.channels)}")
        print(f"Target channels: {self.TARGET_CHANNELS}")
        print(f"\n[CHART] PROGRESS TRACKING")
        print(f"Total runs: {self.progress.get('total_runs', 0)}")
        print(f"Last run: {self.progress.get('last_run', 'Never')}")
        print(f"Videos processed: {self.progress.get('videos_processed', 0)}")
        print(f"Channels checked: {self.progress.get('channels_checked', 0)}")
        print(f"Recent errors: {len(self.progress.get('errors', []))}")
        print(f"\n[FOLDER] DIRECTORIES")
        print(f"Data: {self.youtube_dir}")
        print(f"Transcripts: {self.transcripts_dir}")
        print(f"Summaries: {self.summaries_dir}")
        
        if self.progress.get('errors'):
            print(f"\n[!] RECENT ERRORS")
            for err in self.progress['errors'][-3:]:
                print(f"   [{err.get('time', 'unknown')}] {err.get('message', 'unknown')[:60]}")


def main():
    import sys
    
    yt = YouTubeAutomation()
    
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "run":
            result = yt.run_daily_check()
            print("\n" + "="*60)
            print("RESULT:")
            print(json.dumps(result, indent=2))
        
        elif command == "list":
            yt.list_channels()
        
        elif command == "status":
            yt.show_status()
        
        elif command == "add" and len(sys.argv) >= 5:
            yt.add_channel(sys.argv[2], sys.argv[3], sys.argv[4])
        
        elif command == "remove" and len(sys.argv) >= 3:
            yt.remove_channel(sys.argv[2])
        
        else:
            print("""YouTube Automation System v2.0

Commands:
  python youtube_automation.py run           - Run daily check
  python youtube_automation.py list          - List monitored channels
  python youtube_automation.py status        - Show system status
  python youtube_automation.py add "Name" "ID" "category"
  python youtube_automation.py remove "Name" - Remove channel

Categories: finance, crypto, business, philosophy, productivity, tech, podcast, lifestyle
""")
    else:
        # Run daily check by default
        result = yt.run_daily_check()
        print("\n" + "="*60)
        print("RESULT:")
        print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()