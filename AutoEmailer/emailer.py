import os
import getpass
import datetime
import smtplib
from AutoEmailer import EmailerConfig
from pathlib import Path
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.encoders import encode_base64
from email.mime.multipart import MIMEMultipart


class Emailer:
    """
    Welcome to the Auto Emailer to send all of your emails!
    """
    def __init__(self, config=None, delay_login=True):
        """
        """
        self._config = EmailerConfig(**config) if config else EmailerConfig()
        self._logged_in = False
        if not delay_login:
            self._login()

    def _login(self):
        """
        Use the config from input or environment variables to login.
        """
        self._smtp = smtplib.SMTP(host=self._config, port=self._port, timeout=10)
        self._smtp.starttls()
        self._smtp.login(self._sender_email, self._password)
        self._logged_in = True

    @staticmethod
    def from_login(**kwargs):
        """
        Get prompted for login information at your command line.
        All keyword args are passed to initialize Emailer().

        :param kwargs: input from user
        :return: Emailer() object
            initialized emailer object from input values
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

    @staticmethod
    def email_template(template_path):
        """
        Opens, reads, and returns the given template file path as a string.

        :param template_path: str
            file path for the email template
        :return: str
            text of template file
        """
        # try and except logic here
        try:
            template_text = Path(template_path).read_text()
        except FileNotFoundError:
            raise
        return template_text

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
        :return: nothing
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
        # add finally to the try/except block
        return


if __name__ == '__main__':
    # create emailer object from input
    email = Emailer.from_login()

    # get email destination, subject, and text from input
    email_destination = input('Email destination: ')
    email_subject = input('Email subject: ')
    email_text = input('Email text: ')

    # send email away!
    email.send_email([email_destination], email_subject, text=email_text)
    print('Email Sent!')
