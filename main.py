import os
from dotenv import load_dotenv
import pprint
import json

# User-defined imports
from data.webmail_details import WebmailDetails
from utils.get_new_emails import get_new_emails
from event_creator.clean_email import clean_mail
from event_creator.get_events import get_events
from utils.add_reminder import add_event

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
    secrets = []
    for mail in new_emails:
        cleaned_mail, mail_secrets = clean_mail(mail)
        cleaned_emails.append(cleaned_mail)
        secrets.append(mail_secrets)
    print(f"Extracted {len(cleaned_emails)} events from the new emails.")

    email_in_dict = [s.to_dict() for s in cleaned_emails]
    # Create dictionary
    data = {
        "mail": email_in_dict,
        "secrets": secrets
    }

    # Save to JSON
    with open("data/cleaned_mails.json", "w") as f:
        json.dump(data, f)

    # Get events from the new emails
    new_events = []
    for mail, secret in zip(cleaned_emails, secrets):
        event = get_events(mail, secret)
        new_events.append(event)
        # pprint.pprint(events)
        for key, value in event.items():
            if key != "user_input":
                pprint.pprint(f"{key}: {value}")
        event_description = f"""Email Date: {event['email_reception_date']}
Main Entity: {event['main_entity']}
Email Summary: {event['email_summary']}"""
        
        add_event(event["event_title"], event_description, 
                  event["start_date_time"], event["end_date_time"])

if __name__ == "__main__":
    main()
