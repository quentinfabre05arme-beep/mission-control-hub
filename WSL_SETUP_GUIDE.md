# WSL + Docker + Nitter Setup Guide

## Overview

Complete setup guide for running Nitter (X/Twitter proxy) on Windows via WSL + Docker.

## Current Status

**Started:** 2026-07-12 14:19  
**Status:** WSL installing (--no-launch mode)  
**Reminder Set:** 14:30 (15 minutes)

## Setup Steps

### Step 1: Install WSL (✅ In Progress)

Command used:
```powershell
wsl --install --distribution Ubuntu --no-launch
```

This installs WSL without requiring immediate restart.

### Step 2: Restart PC (Pending)

After WSL install completes:
1. Save your work
2. Restart Windows
3. WSL will be available

### Step 3: Ubuntu First Setup (After Restart)

On first launch:
```bash
# Ubuntu will prompt for:
Username: [create one]
Password: [create one]

# Then update system
sudo apt update && sudo apt upgrade -y
```

### Step 4: Install Docker in WSL

```bash
# Install Docker
sudo apt install docker.io -y

# Start Docker service
sudo service docker start

# Add user to docker group
sudo usermod -aG docker $USER

# Verify
sudo docker --version
```

### Step 5: Run Nitter Container

```bash
# Run Nitter on port 8788
docker run -d -p 8788:8080 --name nitter zedeus/nitter:latest

# Verify it's running
docker ps

# Test locally
curl http://localhost:8788
```

### Step 6: Configure X-Tweet-Fetcher

In Windows (PowerShell):
```powershell
# Set environment variable
[Environment]::SetEnvironmentVariable("XTF_NITTER", "http://127.0.0.1:8788", "User")

# Test search
xtf --search "ETH treasury" --limit 3
```

## Verification

Test the full pipeline:
```bash
# From Windows
python enhanced_research_pipeline.py
```

X search should now return actual tweets instead of errors.

## Troubleshooting

### WSL Install Fails
- Enable Virtualization in BIOS
- Enable Windows features: "Virtual Machine Platform" and "Windows Subsystem for Linux"

### Docker Won't Start
```bash
sudo service docker start
# OR
sudo systemctl start docker
```

### Nitter Connection Refused
- Check if container is running: `docker ps`
- Check logs: `docker logs nitter`
- Restart: `docker restart nitter`

### XTF Can't Connect
- Verify XTF_NITTER env var: `echo $env:XTF_NITTER`
- Test connection: `curl http://127.0.0.1:8788`

## Automation Notes

Once complete:
- ✅ Daily pipeline runs automatically at 8 AM
- ✅ X search provides real-time data
- ✅ Nitter runs persistently in Docker
- ✅ No manual intervention needed

---
Created: 2026-07-12
Status: In Progress
