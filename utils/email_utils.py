import email
from email.header import decode_header
from email.utils import parsedate_to_datetime
import json
import os

from data.email_content import EmailContent

def get_last_timestamp():
    json_path = "./last_timestamp.json"
    if not os.path.exists(json_path):
        # Create the file with default content
        with open(json_path, "w") as f:
            json.dump({"last_timestamp": None}, f)
        return None
    with open(json_path, "r") as f:
        data = json.load(f)
        return data.get("last_timestamp")


def fetch_all_emails(mail, folder="INBOX"):
    # Select the mailbox
    mail.select(folder)
    
    # Search for all emails
    status, messages = mail.search(None, "ALL")
    if status != "OK":
        print("No messages found!")
        return []
    
    return messages[0].split()

def new_email_exists(latest_timestamp, last_timestamp):
    t1 = parsedate_to_datetime(latest_timestamp)
    t2 = parsedate_to_datetime(last_timestamp)
    return t1 > t2 # True if new email exists

def store_email(msg):
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition"))

            if (content_type == "text/plain"
                    and "attachment" not in content_disposition):
                body = part.get_payload(decode=True).decode(errors="ignore")
                break
        else:
            body = ""  # Fallback if no text/plain found
    else:
        body = msg.get_payload(decode=True).decode(errors="ignore")
    # Decode the subject
    subject, encoding = decode_header(msg["Subject"])[0]
    if isinstance(subject, bytes):
        subject = subject.decode(encoding or "utf-8")
        
    email_content = EmailContent(
            subject=subject,
            date=msg.get("Date"),
            body=body,
            attachment=None  # Handle attachments if needed
            )
    return email_content

def fetch_single_email(mail, eid):
    # Fetch the email
    status, data = mail.fetch(eid, "(BODY.PEEK[])")
    if status != "OK":
        print("Failed to fetch email.")
        return None
    
    # Parse the email
    return email.message_from_bytes(data[0][1])