@echo off
echo Starting X Automation System...
cd /d "C:\Users\quent\.openclaw\workspace"
pythonw.exe x_automation_scheduler.py > automation_data\scheduler.log 2>&1
