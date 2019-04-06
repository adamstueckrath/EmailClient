import os
import getpass
import datetime
import smtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart

class Emailer():
    def __init__(self, config=None, delay_login=True, from_input=False):
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

        if from_input:
            self.from_login()
        else:
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
                if '@outlook.com' or '@hotmail.com' in self._sender_email:
                    self._host = 'smtp.office365.com'
                elif '@gmail.com' in self._sender_email:
                    self._host = 'smtp.gmail.com'
                elif '@yahoo.com' in self._sender_email:
                    self._host = 'smtp.mail.yahoo.com'
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

    @staticmethod
    def from_login(**kwargs):
        """
        Get prompted for login information at your command line.
        All keyword args are passed to the initializer Emailer().
        """
        config = {}
        config['sender_email'] = input('Email account to send from: ')
        if '@outlook.com' or '@hotmail.com' in config['sender_email']:
            port_message = 'Port # (likely 587): '
            host_message = 'Host URL (likely smtp.office365.com): '
        elif '@gmail.com' in config['sender_email']:
            port_message = 'Port # (likely 587): '
            host_message = 'Host URL (likely smtp.gmail.com): '
        elif '@yahoo.com' in config['sender_email']:
            port_message = 'Port # (likely 587): '
            host_message = 'Host URL (likely smtp.mail.yahoo.com): '
        else:
            port_message = 'Port #: '
            host_message = 'Host URL: '
        config['port'] = int(input(port_message))
        config['host'] = input(host_message)
        config['password'] = getpass.getpass(
            'Email password (nothing will be shown as you type):'
        )
        return Emailer(config=config, **kwargs)

    def send_email(self, destinations, subject, text, files=None):
        """
        Send an email to the emails listed in destinations
        with the given message.

        The message will auto-fill in the FROM, TO,
        and DATE field, and the SUBJECT field will be filled
        in with your given subject.

        Parameters
        ----------
        destinations : list
            list of strings of email addresses
        subject : str
            subject header of your email
        text : str
            the body text of your email
        files : list
            list of file paths to attached to email

        Returns
        -------
        failed : dict
            dict of addresses that it failed to send to.
        """
        # create multi-part message for text and attachments
        message = MIMEMultipart()
        message['From'] = self._sender_email
        message['To'] = '; '.join(destinations)
        message['Date'] = datetime.datetime.utcnow().isoformat()
        message['Subject'] = subject

        # attach text part of message
        message.attach(MIMEText(text))

        # iterterate through files to attach
        for path in files or []:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=os.path.basename(path))
            message.attach(part)

        else:
            if not self._logged_in:
                self._login()
            try:
                self._smtp.sendmail(self._sender_email, destinations, message.as_string())
            except smtplib.SMTPServerDisconnected:
                self._login()
                self._smtp.sendmail(self._sender_email, destinations, message.as_string())

        return


if __name__ == '__main__':
    try:
        Emailer() or Emailer().from_login()
    except:
        raise
