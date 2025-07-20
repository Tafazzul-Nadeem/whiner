class EmailContent:
    def __init__(self, subject: str, date: str, body: str, attachment: list = None):
        self.subject = subject
        self.date = date
        self.body = body
        self.attachment = attachment

    def __repr__(self):
        return (f"Email(subject={self.subject!r},\n"
                f"date={self.date!r},\n"
                f"body={self.body!r},\n"
                f"attachment={self.attachment!r}")