from event_creator.cleaning_tool import clean_component

def clean_mail(email):
    # Data Structure to store entities and their codes
    entity_map = {"person": {}, "company": {}, "secret":{}}
    code_counters = {"PERSON": 1, "ORG": 1, "SECRET": 1}

    # Clean the subject
    subject = email.subject
    # print("Raw Subject: ", subject)
    new_subject = subject
    # Redact entities like names and organizations
    new_subject, entity_map, code_counters = clean_component(new_subject, 
                                                             entity_map, 
                                                             code_counters)
    subject = new_subject

    # Clean the body
    body = email.body
    # print("Raw Subject: ", subject)
    new_body = body
    # Redact entities like names and organizations
    new_body, entity_map, code_counters = clean_component(new_body, 
                                                             entity_map, 
                                                             code_counters)
    body = new_body

    return subject, body, entity_map

if __name__ == "__main__":
    # Example email object
    class Email:
        def __init__(self, subject, body):
            self.subject = subject
            self.body = body
    text = """Meeting with John Doe at TechCorp. 
Their phone number is +91 (512) 234/754-2554. 
Contact me at username: johndoe, password : secret123
Address: 1234 Elm Street, Springfield,
Utah, 
USA.
"""
    email = Email(text, "Let's discuss the project details John.")
    cleaned_subject, cleaned_body, secrets = clean_mail(email)
    print(f"Cleaned Subject: {cleaned_subject}")
    print(f"Cleaned Body: {cleaned_body}")
    print(f"Secrets: {secrets}")