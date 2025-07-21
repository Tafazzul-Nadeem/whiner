import os
from dotenv import load_dotenv

# User-defined imports
from data.webmail_details import WebmailDetails
from utils.fetch_mails import get_new_emails
from event_creator.get_events import get_events

# load environment variables from .env file
load_dotenv()

def main():
    webmail1 = WebmailDetails(imap_server=os.getenv("IMAP_SERVER1"),
                                port=int(os.getenv("IMAP_PORT1")),
                                security=os.getenv("SECURITY1"),
                                username=os.getenv("EMAIL_ACCOUNT1"),
                                password=os.getenv("EMAIL_PASSWORD1")
                            )
    new_emails = get_new_emails(webmail1)
    # Connect to the webmail server
    print(f"Found {len(new_emails)} new emails.")
    # print(new_emails[-1])

    # Get events from the new emails
    new_events = get_events(new_emails)
    print(f"Extracted {len(new_events)} events from the new emails.")
    for event in new_events:
        print(f"Subject: {event['subject']}")
        print(f"Body: {event['body']}")
        print(f"Secrets: {event['secrets']}")
        print("-" * 120)


if __name__ == "__main__":
    main()
