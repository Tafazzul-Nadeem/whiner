from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import datetime
import os
import pickle
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
client_secret_path = '/Users/tafazzulnadeem/Desktop/IITK Work/Placements/self_projects/whiner/client_secret.json' 
def get_credentials():
    creds = None

    # Load token if it exists
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)

    # If token is invalid/expired or doesn't exist, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh if possible
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new token
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    return creds

def add_event(summary, description, start_time, end_time, calendar_id='primary'):
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time.isoformat(),
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"✅ Event created: {event.get('htmlLink')}")

if __name__ == "__main__":
    start = datetime.datetime(2025, 7, 20, 18, 0)
    end = datetime.datetime(2025, 7, 20, 19, 0)
    add_event("Tafazzul's Meeting", "Discuss project", start, end)
