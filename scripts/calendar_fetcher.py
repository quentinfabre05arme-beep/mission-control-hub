"""
Fetch Google Calendar events and save as JSON for dashboard
"""
import os
import json
import sys
from datetime import datetime, timedelta

# Add config path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def get_calendar_events():
    """Fetch events from Google Calendar"""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from googleapiclient.discovery import build
        
        SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
        creds = None
        token_path = 'config/token.json'
        creds_path = 'config/google_credentials.json'
        
        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not creds or not creds.valid:
            return {'error': 'Not authenticated', 'needs_auth': True}
        
        service = build('calendar', 'v3', credentials=creds, static_discovery=False)
        
        # Get events for next 30 days
        now = datetime.utcnow().isoformat() + 'Z'
        end = (datetime.utcnow() + timedelta(days=30)).isoformat() + 'Z'
        
        events_result = service.events().list(
            calendarId='primary',
            timeMin=now,
            timeMax=end,
            maxResults=50,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        
        events = events_result.get('items', [])
        
        # Format for dashboard
        formatted = []
        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end_time = event['end'].get('dateTime', event['end'].get('date'))
            
            # Parse datetime
            if 'T' in start:
                event_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
            else:
                event_date = datetime.fromisoformat(start)
            
            formatted.append({
                'id': event['id'],
                'title': event['summary'],
                'start': start,
                'end': end_time,
                'date': event_date.strftime('%Y-%m-%d'),
                'time': event_date.strftime('%H:%M') if 'T' in start else 'All day',
                'description': event.get('description', ''),
                'location': event.get('location', ''),
                'link': event.get('htmlLink', '')
            })
        
        return {
            'status': 'success',
            'count': len(formatted),
            'events': formatted,
            'updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        return {'error': str(e), 'status': 'error'}

if __name__ == '__main__':
    result = get_calendar_events()
    print(json.dumps(result, indent=2))
