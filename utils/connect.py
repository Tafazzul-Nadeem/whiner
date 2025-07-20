import imaplib
import email
from email.header import decode_header
import os

def connect_webmail(webmail_details):
    """
    Connect to the webmail server using the provided details.
    
    Args:
        webmail_details (WebmailDetails): An instance containing webmail connection details.
    
    Returns:
        imaplib.IMAP4_SSL: An authenticated IMAP connection object.
    """
    # Connect to the server
    mail = imaplib.IMAP4_SSL(webmail_details.imap_server, webmail_details.port)
    mail.login(webmail_details.username, webmail_details.password)
    
    return mail
