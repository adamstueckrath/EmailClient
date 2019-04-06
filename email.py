import os
import getpass
import datetime
import smtplib
from email.MIMEBase import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart

class Email():
    def __init__(self, config=None, delay_login=True):
        """
        The resolution order for the following information is
        config -> environment variable -> guess

        Parameters
        ----------
        config : dict
            dict with a subset of the following keys.
                - sender_email : str
                    - sender email.
                    - equivalent environment variable: EMAIL_ADDRESS
                - password : str
                    - password of that email account.
                    - equivalent environment variable: EMAIL_PASSWORD
                - port : int
                    - port number.
                    - equivalent environment variable: EMAIL_PORT
                    - If neither config nor environment variable is set,
                      then we attempt to guess the port number from the
                      sender_email.
                - host : str
                    - domain name of host.
                    - equivalent environment variable: EMAIL_HOST
                    - If neither config nor environment variable is set,
                      then we attempt to guess the host from the
                      sender_email.
        delay_login : bool
            if True, no login attempt will be made until send_mail
            is called and block_sending is False. Otherwise, a login
            attempt will be made at construction time.
        """
        if config is None:
            config = {}

        self._sender_email = config.get('sender_email', os.getenv('EMAIL_ADDRESS'))
        if not self._sender_email:
            raise ValueError('Either config must contain "sender_email" or the '
                             'EMAIL_ADDRESS environment variable must '
                             'be set.')

        self._password = config.get('password', os.getenv('EMAIL_PASSWORD'))
        if not self._password:
            raise ValueError('Either config must contain "password" or the '
                             'EMAIL_PASSWORD environment variable must '
                             'be set.')

        self._port = config.get('port', os.getenv('EMAIL_PORT'))
        if self._port is None:
            self._port = 587

        self._host = config.get('host', os.getenv('EMAIL_HOST'))
        if self._host is None:
            if '@outlook.com' in self._sender_email:
                self._host = 'smtp.office365.com'
            elif '@gmail.com' in self._sender_email:
                self._host = 'smtp.gmail.com'
            else:
                raise ValueError('Cannot guess host given email.')

        self._logged_in = False
        if not delay_login:
            self._login()

    def _login(self):
        self._smtp = smtplib.SMTP(host=self._host, port=self._port, timeout=10)
        self._smtp.starttls()
        self._smtp.login(self._sender_email, self._password)
        self._logged_in = True