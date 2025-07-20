from googleapiclient.discovery import build
import datetime

from utils.auth_calendar import get_credentials


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
    print(f"Event created: {event.get('htmlLink')}")

if __name__ == "__main__":
    start = datetime.datetime(2025, 7, 20, 23, 0)
    end = datetime.datetime(2025, 7, 20, 23, 30)
    add_event("Meeting", "Discuss project", start, end)