from google.oauth2 import service_account
"""
This module provides functionality to add events to a Google Calendar using the Google Calendar API and a service account.

Functions:
    add_event(summary, description, start_time, end_time, calendar_id='primary'):
        Adds an event to the specified Google Calendar.

        Args:
            summary (str): The title or summary of the event.
            description (str): The description of the event.
            start_time (datetime.datetime): The start time of the event as a datetime object.
            end_time (datetime.datetime): The end time of the event as a datetime object.
            calendar_id (str, optional): The ID of the calendar to add the event to. Defaults to 'primary'.

        Returns:
            None. Prints the link to the created event.

Usage:
    Run the module directly to add a sample event to the calendar.
"""
from googleapiclient.discovery import build
import datetime

# Path to your service account key file
SERVICE_ACCOUNT_FILE = '/Users/tafazzulnadeem/Desktop/IITK Work/Placements/self_projects/whiner/whiner-b9f838c8af18.json'
SCOPES = ['https://www.googleapis.com/auth/calendar']

def add_event(summary, description, start_time, end_time, calendar_id='Tafazzul Nadeem'):
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('calendar', 'v3', credentials=credentials)

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
    summary = "Test Event"
    description = "This is a detailed description of the test event."
    start_time = datetime.datetime(2025, 7, 20, 16, 30)
    end_time = datetime.datetime(2025, 7, 20, 16, 45)
    add_event(summary, description, start_time, end_time)