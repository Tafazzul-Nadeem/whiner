class WebmailDetails:
    def __init__(self, 
                 imap_server: str, 
                 port: int, 
                 security: str, 
                 username: str, 
                 password: str):
        """ Initialize webmail details."""
        self.imap_server = imap_server
        self.port = port
        self.security = security
        self.username = username
        self.password = password

    def __repr__(self):
        return (f"WebmailDetails(imap_server='{self.imap_server}', port={self.port}, "
                f"security='{self.security}', username='{self.username}')")