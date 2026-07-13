"""
Google Calendar Authentication Handler
Saves tokens for API access
"""
import os
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Calendar access
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar'
]

def authenticate():
    """Authenticate with Google Calendar and save token"""
    creds = None
    token_path = 'config/token.json'
    creds_path = 'config/google_credentials.json'
    
    # Load existing token
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
    
    # If no valid credentials, authenticate
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                creds_path, SCOPES)
            creds = flow.run_local_server(port=8090)
        
        # Save token
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
    
    return creds

def get_service():
    """Get Calendar API service"""
    creds = authenticate()
    return build('calendar', 'v3', credentials=creds, static_discovery=False)

def list_calendars():
    """List user's calendars"""
    service = get_service()
    calendars_result = service.calendarList().list().execute()
    calendars = calendars_result.get('items', [])
    
    for cal in calendars:
        print(f"{cal['summary']} ({cal['id']})")
    
    return calendars

def list_events(calendar_id='primary', days=7):
    """List events from calendar"""
    from datetime import datetime, timedelta
    
    service = get_service()
    
    now = datetime.utcnow().isoformat() + 'Z'
    end = (datetime.utcnow() + timedelta(days=days)).isoformat() + 'Z'
    
    events_result = service.events().list(
        calendarId=calendar_id,
        timeMin=now,
        timeMax=end,
        maxResults=50,
        singleEvents=True,
        orderBy='startTime'
    ).execute()
    
    events = events_result.get('items', [])
    
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(f"{start} | {event['summary']}")
    
    return events

if __name__ == '__main__':
    print("Google Calendar Authentication")
    print("=" * 40)
    print("\nAuthenticating...")
    
    try:
        service = get_service()
        print("✅ Authentication successful!")
        
        print("\nYour calendars:")
        list_calendars()
        
        print("\nUpcoming events (next 7 days):")
        list_events()
        
    except Exception as e:
        print(f"❌ Error: {e}")
