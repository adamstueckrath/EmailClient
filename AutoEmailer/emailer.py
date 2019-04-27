import os
import getpass
import datetime
import smtplib
from pathlib import Path
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart


class Emailer:
    def __init__(self, config=None, delay_login=True):
        """
        Welcome to the Emailer to send all of your emails!

        Order for the following information is
        config -> environment variable -> guess
        :param config: dict
            sender_email : str
              - sender email.
              - equivalent environment variable: EMAIL_ADDRESS
            password : str
              - password of that email account.
              - equivalent environment variable: EMAIL_PASSWORD
            port : int
              - port number.
              - equivalent environment variable: EMAIL_PORT
              - If neither config nor environment variable is set,
                then we attempt to guess the port number from the
                sender_email.
            host : str
              - domain name of host.
              - equivalent environment variable: EMAIL_HOST
              - If neither config nor environment variable is set,
                then we attempt to guess the host from the
                sender_email.
        :delay_login: bool
            if True, no login attempt will be made until send_mail
            is called. Otherwise, a login attempt will be made
            at construction time.
        """
        if config is None:
            config = {}

        self._sender_email = config.get('sender_email', os.environ.get('EMAIL_ADDRESS'))
        if not self._sender_email:
            raise ValueError('Either config must contain "sender_email" or the '
                             'EMAIL_ADDRESS environment variable must '
                             'be set.')

        self._password = config.get('password', os.environ.get('EMAIL_PASSWORD'))
        if not self._password:
            raise ValueError('Either config must contain "password" or the '
                             'EMAIL_PASSWORD environment variable must '
                             'be set.')

        self._port = config.get('port', os.getenv('EMAIL_PORT'))
        if self._port is None:
            self._port = 587

        self._host = config.get('host', os.getenv('EMAIL_HOST'))
        if self._host is None:
            if ('@outlook.com' in self._sender_email) or ('@hotmail.com' in self._sender_email):
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
        """
        Use the config from input or environment variables to login.
        :return:
        """
        self._smtp = smtplib.SMTP(host=self._host, port=self._port, timeout=10)
        self._smtp.starttls()
        self._smtp.login(self._sender_email, self._password)
        self._logged_in = True

    @staticmethod
    def email_template(template_path):
        """
        Opens, reads, and returns the given template file path as a string.
        :param template_path: str
            file path for the email template
        :return: string of template
        """
        # try and except logic here
        try:
            template_text = Path(template_path).read_text()
        except FileNotFoundError:
            raise
        return template_text

    @staticmethod
    def from_login(**kwargs):
        """
        Get prompted for login information at your command line.
        All keyword args are passed to initialize Emailer().
        :param kwargs: input from user
        :return: Initialized Emailer() from input values.
        """
        config = dict()
        config['sender_email'] = input('Email account to send from: ')

        if ('@outlook.com' in config['sender_email']) or ('@hotmail.com' in config['sender_email']):
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
        config['password'] = getpass.getpass('Email password (nothing will be shown as you type): ')

        return Emailer(config=config, **kwargs)

    def send_email(self, destinations, subject, text=None,
                   template_path=None, template_args=None, attach_files=None):
        """
        Send an email to the emails listed in destinations
        with the given message.

        The message will auto-fill in the FROM, TO,
        and DATE field, and the SUBJECT field will be filled
        in with your given subject.
        :param destinations: list
            list of strings of email addresses
        :param subject: str
            subject header of your email
        :param text: str
            the body text of your email
        :param template_path:
            path of email template text file
        :param template_args: dict
            keyword arguments to format email template
        :param attach_files: list
            list of file paths to attached to email
        :return:
        """
        # create multi-part message for text and attachments
        message = MIMEMultipart()
        message['From'] = self._sender_email
        message['To'] = '; '.join(destinations)
        message['Date'] = datetime.datetime.utcnow().isoformat()
        message['Subject'] = subject

        # check if email template is used
        if template_path:
            text = self.email_template(template_path)
            text.format(**template_args)

        # attach text part of message
        message.attach(MIMEText(text))

        # iterate through files to attach
        for path in attach_files or []:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())
            encode_base64(part)
            part.add_header('Content-Disposition',
                            'attachment', filename=os.path.basename(path))
            message.attach(part)

        if not self._logged_in:
            self._login()

        # handle disconnect and connection errors by quick login and attempt to send again
        try:
            self._smtp.sendmail(self._sender_email, destinations, message.as_string())

        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            self._login()
            self._smtp.sendmail(self._sender_email, destinations, message.as_string())

        return


if __name__ == '__main__':
    # create emailer object from input
    email = Emailer.from_login()

    # get email destination, subject, and text from input
    email_destination = input('Email account to send to: ')
    email_subject = input('Email subject: ')
    email_text = input('Email template path: ')

    # send email away!
    email.send_email([email_destination], email_subject, template_path=email_text)
