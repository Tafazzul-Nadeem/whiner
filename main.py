import os
from dotenv import load_dotenv

# User-defined imports
from data.webmail_details import WebmailDetails
from utils.fetch_mails import get_new_emails

# load environment variables from .env file
load_dotenv()

webmail1 = WebmailDetails(
    imap_server=os.getenv("IMAP_SERVER1"),
    port=int(os.getenv("IMAP_PORT1")),
    security=os.getenv("SECURITY1"),
    username=os.getenv("EMAIL_ACCOUNT1"),
    password=os.getenv("EMAIL_PASSWORD1")
)

def main():
    new_emails = get_new_emails(webmail1)
    # Connect to the webmail server
    print(f"Found {len(new_emails)} new emails.")
    print(new_emails[-1])


if __name__ == "__main__":
    main()
