from utils.connect import connect_webmail
from utils.timestamp import get_last_timestamp, update_last_timestamp
from utils.email_utils import (
    fetch_all_emails,
    new_email_exists,
    store_email,
    fetch_single_email
)


def get_new_emails(webmail_details):
    mail = connect_webmail(webmail_details)
    all_emails = fetch_all_emails(mail, folder="INBOX")
    last_timestamp = get_last_timestamp()

    new_mails = []
    # Start from the last email and iterate backwards
    for eid in reversed(all_emails):
        msg = fetch_single_email(mail, eid)
        if not msg:
            continue
        email_date = msg.get("Date")
        if last_timestamp is None or new_email_exists(email_date, last_timestamp):
            # CREATE EMAIL CONTENT OBJECT
            email_content = store_email(msg)
            new_mails.insert(0, email_content)  # Insert at the beginning to keep order
        else:  
            break
    if new_mails:
        latest_email_date = new_mails[-1].date
        update_last_timestamp(latest_email_date)
    else:
        pass
    
    mail.logout()
    return new_mails

