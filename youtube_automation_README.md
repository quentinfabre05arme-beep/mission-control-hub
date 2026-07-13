# YouTube Automation System

## Status: OPERATIONAL

### Overview
Monitors 25 YouTube channels daily at 9:00 AM, downloads transcripts, generates summaries, and creates daily digest.

### Current Status
- **Channels Monitored:** 25
- **Last Run:** 2026-07-10 14:50:19
- **Videos Processed:** 8 (in first run)
- **Status:** Working

### Commands

```bash
# Run daily check manually
python youtube_automation.py run

# List all channels
python youtube_automation.py list

# Show system status
python youtube_automation.py status

# Add a channel
python youtube_automation.py add "Channel Name" "CHANNEL_ID" "category"

# Remove a channel
python youtube_automation.py remove "Channel Name"
```

### Channel Categories

| Category | Count | Channels |
|----------|-------|----------|
| Finance | 14 | Graham Stephan, Meet Kevin, Mark Tilbury, Andrei Jikh, Patrick Boyle, Two Cents, The Plain Bagel, Humphrey Yang, Caleb Hammer, Our Rich Journey, Stock Moe, New Money, Nate OBrien, The Financial Diet |
| Tech | 6 | Linus Tech Tips, MKBHD, Mrwhosetheboss, Fireship, Traversy Media, Tech With Tim |
| Business | 3 | Jake Paul, Logan Paul, MrBeast |
| Productivity | 2 | Ali Abdaal, Thomas Frank |

### Files

| File | Description |
|------|-------------|
| `youtube_automation.py` | Main automation script |
| `youtube_content/channels.json` | Channel list with IDs and categories |
| `youtube_content/progress.json` | Run statistics and progress |
| `youtube_content/transcripts/` | Downloaded video transcripts |
| `youtube_content/summaries/` | Video summaries with metadata |
| `youtube_content/digest_YYYY-MM-DD.txt` | Daily digest files |

### Telegram Integration

To enable Telegram notifications:

1. Create a bot with @BotFather on Telegram
2. Get your chat ID
3. Edit `youtube_automation.py` and update:
   ```python
   TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
   TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
   ```

### Windows Task Scheduler Setup

To run daily at 9:00 AM:

1. Open Task Scheduler
2. Create Basic Task:
   - Name: YouTube Daily Check
   - Trigger: Daily at 9:00 AM
   - Action: Start a program
   - Program: `python`
   - Arguments: `C:\Users\quent\.openclaw\workspace\youtube_automation.py run`

### Daily Digest Format

```
[TV] YouTube Daily Digest
📅 Friday, July 10, 2026

Found 8 new video(s) from 25 channels:

1. [MONEY] Video Title
   by Channel Name
   
   Summary of key points...
   Link: https://youtube.com/...
```

### Notes

- RSS feeds are used to check for new videos (no API key required)
- Transcripts are downloaded using youtube-transcript-api
- Summaries use extractive summarization (first 5 + last 3 sentences)
- Only videos from the last 24 hours are processed
- Telegram integration is optional (configure token to enable)