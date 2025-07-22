import os
from dotenv import load_dotenv

# User-defined imports
from data.webmail_details import WebmailDetails
from utils.fetch_mails import get_new_emails
from event_creator.clean_email import clean_mail
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
    # Clean emails to redact sensitive information
    cleaned_emails = []
    for mail in new_emails:
        cleaned_mail, secrets = clean_mail(mail)
        cleaned_emails.append(cleaned_mail)
    print(f"Extracted {len(cleaned_emails)} events from the new emails.")
    for event in cleaned_emails:
        print(f"Subject: {event.subject}")
        print(f"From: {event.date}")
        print(f"Body: {event.body}")
        print(f"Secrets: {secrets}")
        print("-" * 120)

    # Get events from the new emails
    new_events = []
    for mail in cleaned_emails:
        events = get_events(mail)
        print(f"Extracted {len(events)} events from the email.")
        new_events.extend(events)

if __name__ == "__main__":
    main()
