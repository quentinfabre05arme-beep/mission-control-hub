# YouTube Automation System
**Fully Autonomous Channel Monitoring & Summarization**

---

## What It Does (100% Autonomous)

### 1. Channel Monitoring
- Checks YouTube RSS feeds for new videos
- Monitors channels every 24 hours
- Detects videos uploaded in last 24 hours

### 2. Transcript Extraction
- Downloads video transcripts automatically
- Works with auto-generated captions
- Saves to `youtube_content/transcripts/`

### 3. AI Summarization
- Generates key points from transcripts
- Creates concise summaries
- Saves to `youtube_content/summaries/`

### 4. Daily Digest
- Compiles all new videos into daily report
- Sends to Telegram at scheduled time
- Includes: title, channel, key points

---

## Current Channels Monitored

| Channel | Category | Status |
|---------|----------|--------|
| Andrei Jikh | Finance | ✅ Active |
| Graham Stephan | Finance | ✅ Active |
| Meet Kevin | Finance | ✅ Active |

**Add more:** See commands below

---

## Cron Jobs (Auto-Scheduled)

### Daily Check
**Job:** youtube-daily-check
**Time:** 9:00 AM daily
**Action:**
- Check all channels for new videos
- Download transcripts
- Generate summaries
- Create digest
- Send to Telegram

---

## Commands You Can Use

### Run daily check manually:
```bash
python youtube_automation.py run
```

### List monitored channels:
```bash
python youtube_automation.py list
```

### Add new channel:
```bash
python youtube_automation.py add "Channel Name" "CHANNEL_ID" "category"
```

**How to find CHANNEL_ID:**
1. Go to YouTube channel
2. View page source (Ctrl+U)
3. Search for "channelId"
4. Copy the ID (starts with UC)

---

## Directory Structure

```
youtube_content/
├── channels.json              # Channel list
├── digest_YYYY-MM-DD.txt      # Daily digests
├── transcripts/
│   └── VIDEO_ID.txt          # Raw transcripts
└── summaries/
    └── VIDEO_ID.json         # Summaries with metadata
```

---

## Daily Digest Format

```
🎥 YouTube Daily Digest - Friday, July 11, 2026

Found 3 new video(s):

1. Video Title
   Channel: Andrei Jikh
   Category: finance
   
   Key Points:
   - Main point from video
   - Another key insight
   - Summary conclusion...
   
   ---

2. Video Title
   Channel: Graham Stephan
   ...
```

---

## Adding Your Favorite Channels

**Example channels to add:**

| Name | Category | Why |
|------|----------|-----|
| Coin Bureau | Crypto | Research |
| Financial Education | Finance | Stock analysis |
| Patrick Boyle | Finance | Markets |
| AI Explained | AI | Technology |
| Lex Fridman | Tech | Interviews |

**Command:**
```bash
python youtube_automation.py add "Coin Bureau" "UCqK_GSMbpiOVeZPrT41cQQw" "crypto"
```

---

## Limitations

- **Transcripts:** Only available if video has captions
- **Rate limits:** YouTube may block after many requests
- **Processing time:** Depends on video length
- **Language:** Works best with English videos

---

## Future Enhancements

- [ ] AI-generated summaries (instead of extractive)
- [ ] Topic filtering (only finance/tech videos)
- [ ] Sentiment analysis
- [ ] Auto-share best clips to X
- [ ] Weekly summary reports

---

## Status

**Installed:** ✅ youtube-transcript-api
**Channels:** 3 active
**Cron jobs:** 1 scheduled
**Next digest:** Tomorrow 9:00 AM

---

**Questions? Reply with commands:**
- `Add channel` - I'll guide you
- `Show channels` - List current
- `Run now` - Generate today's digest
- `Change time` - Adjust schedule
