from google_auth_oauthlib.flow import InstalledAppFlow
import os
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request

SCOPES = ['https://www.googleapis.com/auth/calendar.events']
client_secret_path = '/Users/tafazzulnadeem/Desktop/IITK Work/Placements/self_projects/whiner/client_secret.json' 
def get_credentials():
    creds = None

    # Load token if it exists
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # If token is invalid/expired or doesn't exist, do OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())  # Refresh if possible
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new token
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds




