import imaplib
import email
from email.header import decode_header
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Your credentials and server settings
IMAP_SERVER = os.getenv("IMAP_SERVER")
EMAIL_ACCOUNT = os.getenv("EMAIL_ACCOUNT") # without domain
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")

# Connect to the server
mail = imaplib.IMAP4_SSL(IMAP_SERVER)
mail.login(EMAIL_ACCOUNT, EMAIL_PASSWORD)

# status, mailboxes = mail.list()
# for box in mailboxes:
#     print(box.decode())

# Select the mailbox you want to use
mail.select("INBOX")  # or "INBOX" or any other mailbox

# Search for all emails
status, messages = mail.search(None, "ALL")
email_ids = messages[0].split()
# print(email_ids)

print(f"Total emails: {len(email_ids)}")
# Fetch the most recent email
latest_email_id = email_ids[-21]

# status, data = mail.fetch(latest_email_id, "(RFC822)") # this marks the mail read
status, data = mail.fetch(latest_email_id, "(BODY.PEEK[])") # this does not mark the mail read

# Parse the email
msg = email.message_from_bytes(data[0][1])

# Decode subject
subject, encoding = decode_header(msg["Subject"])[0]
if isinstance(subject, bytes):
    subject = subject.decode(encoding or "utf-8")

# From
from_ = msg.get("CC")
date_time = msg.get("Date")
print("Date:", date_time)

# Print email info
print("From:", from_)
print("Subject:", subject)

# Extract body
if msg.is_multipart():
    for part in msg.walk():
        content_type = part.get_content_type()
        content_disposition = str(part.get("Content-Disposition"))
        if content_type == "text/plain" and "attachment" not in content_disposition:
            body = part.get_payload(decode=True).decode()
            print("Body:", body)
            break
else:
    body = msg.get_payload(decode=True).decode()
    print("Body:", body)

# Logout
mail.logout()
