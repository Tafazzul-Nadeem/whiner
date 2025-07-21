from event_creator.clean_email import clean_mail

def get_events(new_mails):
    events = []
    for mail in new_mails:
        subject, body, secrets = clean_mail(mail)
        # Here you would implement the logic to extract events from the email
        # For now, we will just simulate event extraction
        events.append({
            "subject": subject,
            "body": body,
            "secrets": secrets
        })
    return events