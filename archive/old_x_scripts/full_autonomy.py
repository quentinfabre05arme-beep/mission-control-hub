"""
FULL AUTONOMY SYSTEM
Coordinates: Email, Calendar, AI Services, PC Control, X, YouTube
"""

import asyncio
import io
import json
import sys
from datetime import datetime
from pathlib import Path

# Fix Windows encoding for emojis
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add paths
sys.path.append('.')
sys.path.append('./browser_automation')
sys.path.append('./ai_services')
sys.path.append('./pc_control')

from browser_automation.gmail_automation import GmailAutomation
from browser_automation.outlook_automation import OutlookAutomation
from browser_automation.calendar_automation import CalendarAutomation
from ai_services.gemini_automation import GeminiAutomation
from ai_services.grok_automation import GrokAutomation
from pc_control.system_automation import PCAutomation

class FullAutonomy:
    """Complete digital life automation"""
    
    def __init__(self):
        self.gmail = GmailAutomation()
        self.outlook = OutlookAutomation()
        self.calendar = CalendarAutomation()
        self.gemini = GeminiAutomation()
        self.grok = GrokAutomation()
        self.pc = PCAutomation()
        
        self.status_file = "autonomy_status.json"
        
    async def morning_routine(self):
        """7:00 AM - Complete morning briefing"""
        print(f"\n{'='*50}")
        print(f"🌅 MORNING ROUTINE - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        print(f"{'='*50}\n")
        
        # 1. System Health
        print("1️⃣ Checking system health...")
        health = self.pc.system_health_check()
        
        # 2. Email Check
        print("2️⃣ Checking emails...")
        gmail_data = await self.gmail.check_inbox()
        outlook_data = await self.outlook.check_inbox()
        
        # 3. Calendar Check
        print("3️⃣ Checking calendars...")
        cal_briefing = await self.calendar.generate_daily_briefing()
        
        # 4. Trend Research
        print("4️⃣ Researching trends...")
        trends = await self.grok.check_trends()
        
        # Generate comprehensive briefing
        briefing = self.generate_morning_briefing(
            health, gmail_data, outlook_data, trends
        )
        
        # Save briefing
        briefing_file = f"briefings/morning_{datetime.now().strftime('%Y%m%d')}.txt"
        Path("briefings").mkdir(exist_ok=True)
        with open(briefing_file, "w", encoding='utf-8') as f:
            f.write(briefing)
            
        print(f"\n✅ Morning routine complete. Briefing saved to: {briefing_file}")
        return briefing
        
    def generate_morning_briefing(self, health, gmail, outlook, trends):
        """Generate comprehensive morning briefing"""
        
        briefing = f"""
🌅 GOOD MORNING - {datetime.now().strftime('%A, %B %d, %Y')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💻 SYSTEM STATUS
• Disk: {health['disk_usage_percent']}%
• Memory: {health['memory_usage_percent']}%
• CPU: {health['cpu_usage_percent']}%
• Status: {health['status'].upper()}

📧 EMAIL SUMMARY
• Gmail: {gmail.get('unread', 'N/A')} unread
• Outlook: {outlook.get('unread', 'N/A')} unread

📅 CALENDAR
• Check Google Calendar for today's events
• Check Outlook Calendar for meetings

🔥 TRENDING NOW
• ETH treasury adoption
• GLP-1 healthcare infrastructure
• AI agentic commerce

🎯 TODAY'S PRIORITIES
1. Review X POST NOW briefing (8:00 AM)
2. Check YouTube digest (9:00 AM)
3. Monitor trends (9:00 AM, 1:00 PM, 7:00 PM)
4. Evening summary (6:00 PM)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Generated: {datetime.now().strftime('%H:%M')}
Autonomy System: Active
        """
        
        return briefing
        
    async def midday_check(self):
        """12:00 PM - Midday status check"""
        print(f"\n🕐 MIDDAY CHECK - {datetime.now().strftime('%H:%M')}")
        
        # Quick email check
        gmail_data = await self.gmail.check_inbox()
        
        # System health
        health = self.pc.system_health_check()
        
        print(f"✅ Midday check complete. System: {health['status']}")
        
    async def afternoon_routine(self):
        """3:00 PM - Afternoon research"""
        print(f"\n🕒 AFTERNOON ROUTINE - {datetime.now().strftime('%H:%M')}")
        
        # Research trending topics
        trends = await self.grok.check_trends()
        
        # Check for new emails
        await self.gmail.check_inbox()
        await self.outlook.check_inbox()
        
        print(f"✅ Afternoon routine complete")
        
    async def evening_summary(self):
        """6:00 PM - Evening summary"""
        print(f"\n🌆 EVENING SUMMARY - {datetime.now().strftime('%H:%M')}")
        
        # Final email check
        gmail_data = await self.gmail.check_inbox()
        outlook_data = await self.outlook.check_inbox()
        
        # System status
        health = self.pc.system_health_check()
        
        # Generate summary
        summary = f"""
🌆 EVENING SUMMARY - {datetime.now().strftime('%Y-%m-%d')}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📧 EMAILS
• Gmail: {gmail_data.get('unread', 'N/A')} unread
• Outlook: {outlook_data.get('unread', 'N/A')} unread

💻 SYSTEM
• Status: {health['status']}
• Disk: {health['disk_usage_percent']}%
• Memory: {health['memory_usage_percent']}%

📅 TOMORROW
• Morning briefing: 7:00 AM
• X POST NOW: 8:00 AM
• YouTube digest: 9:00 AM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Autonomy System: Signing off
        """
        
        # Save evening summary
        summary_file = f"briefings/evening_{datetime.now().strftime('%Y%m%d')}.txt"
        Path("briefings").mkdir(exist_ok=True)
        with open(summary_file, "w", encoding='utf-8') as f:
            f.write(summary)
            
        print(f"✅ Evening summary saved to: {summary_file}")
        return summary

async def main():
    """Main entry point"""
    autonomy = FullAutonomy()
    
    # Parse command line arguments
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "morning":
            await autonomy.morning_routine()
        elif command == "midday":
            await autonomy.midday_check()
        elif command == "afternoon":
            await autonomy.afternoon_routine()
        elif command == "evening":
            await autonomy.evening_summary()
        else:
            print(f"Unknown command: {command}")
            print("Available: morning, midday, afternoon, evening")
    else:
        # Default: morning routine
        await autonomy.morning_routine()

if __name__ == "__main__":
    asyncio.run(main())
