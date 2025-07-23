from googleapiclient.discovery import build
import datetime
from datetime import datetime
import pytz

from utils.auth_calendar import get_credentials


def add_event(summary, description, start_time, end_time, calendar_id='primary'):


    def to_google_datetime(dt_str):
        # Parse naive datetime string
        dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")
        # Set timezone
        tz = pytz.timezone("Asia/Kolkata")
        dt = tz.localize(dt)
        # Convert to RFC3339 string
        return dt.isoformat()

    # Then before calling add_event
    start_time = to_google_datetime(start_time)
    end_time = to_google_datetime(end_time)
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    event = {
        'summary': summary,
        'description': description,
        'start': {
            'dateTime': start_time,
            'timeZone': 'Asia/Kolkata',
        },
        'end': {
            'dateTime': end_time,
            'timeZone': 'Asia/Kolkata',
        },
    }

    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    print(f"Event created: {event.get('htmlLink')}")

# if __name__ == "__main__":
#     start = '2025-12-24 00:00:00'
#     end = '2025-12-24 01:00:00'
#     add_event("Meeting", "Discuss project", start, end)