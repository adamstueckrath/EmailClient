import os
import datetime

import smtplib
from pathlib import Path

from email import encoders
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from .config import credentials
from .config import default_credentials


class Emailer:
    """Welcome to the auto-emailer to send all of your emails!"""
    def __init__(self, config=None, delay_login=True):
        """
        Args:
            config (Optional(config.credentials.Credentials)): The constructed
                credentials. Can be None if environment variables are
                configured.
            delay_login (bool): If True, no login attempt will be made until
                send_mail is called. Otherwise, a login attempt will be made at
                class initialization.
        """
        if (config is not None and
                not isinstance(config, credentials.Credentials)):
            raise ValueError('Emailer class only supports credentials from '
                             'auto_emailer.config. See '
                             'auto_emailer.config.credentials and '
                             'auto_emailer.config.environment_vars for help on '
                             'authentication with auto-emailer library.')
        elif config is None:
            try:
                self._config = default_credentials()
            except EnvironmentError:
                raise ValueError('Emailer class only supports credentials from '
                                 'auto_emailer.config. Either define and pass '
                                 'explicitly to Emailer() or set '
                                 'environment_vars.')
        else:
            self._config = config

        self._connected = False
        if not delay_login:
            self._login()

    @property
    def connected(self):
        """Returns:
            bool: If SMTP client is logged in or not.
        """
        return self._connected

    def _logout(self):
        """Quits the connection to the smtp client."""
        if self.connected:
            try:
                self._smtp.quit()
            except smtplib.SMTPServerDisconnected:
                pass
        self._connected = False

    def _login(self):
        """Uses the class attribute Emailer._config to connect
        to SMTP client.
        """
        self._smtp = smtplib.SMTP(host=self._config.host,
                                  port=self._config.port)
        # send 'hello' to SMTP server
        self._smtp.ehlo()
        # start TLS encryption
        self._smtp.starttls()
        self._smtp.login(self._config.sender_email, self._config.password)
        self._connected = True

    @staticmethod
    def email_template(template_path):
        """Opens, reads, and returns the given template file path as a string.

        Args:
            template_path (str): File path for the email template.

        Returns:
            str: Text of file.

        Raises:
            FileNotFoundError: If cannot find the file from given
                `template_path`.
        """
        try:
            template_text = Path(template_path).read_text()
        except FileNotFoundError:
            raise FileNotFoundError('File path not found: {}'
                                    .format(template_path))
        return template_text

    def send_email(self, destinations, subject, text=None,
                   template_path=None, template_args=None, attach_files=None):
        """Send an email to given destination list. The email will auto fill
        the FROM with `Email._config.EMAILER_SENDER` and quit after email
        is sent.

        Args:
            destinations (Sequence[str]): List of strings of email
                addresses to send the email to.
            subject (str): Subject of your email.
            text (Optional[str]): The body text of your email.
            template_path (Optional[str]): File path of an email template
                text to use for the email body.
            template_args (Optional[dict]): Keyword arguments to format
                the email template text.
            attach_files (Sequence[str]): List of string file paths
                to attached to email.
        """
        # create multi-part message for text and attachments
        message = MIMEMultipart()
        message['From'] = self._config.sender_email
        message['To'] = '; '.join(destinations)
        message['Date'] = datetime.datetime.utcnow().isoformat()
        message['Subject'] = subject

        # check if email template is used
        if template_path:
            text = self.email_template(template_path)
            text = text.format(**template_args)

        # attach text part of message
        message.attach(MIMEText(text))

        # iterate through files to attach
        for path in attach_files or []:
            part = MIMEBase('application', "octet-stream")
            with open(path, 'rb') as file:
                part.set_payload(file.read())

            # encode file in ASCII characters to send by email
            encoders.encode_base64(part)
            # add header as to attachment part
            part.add_header('Content-Disposition',
                            'attachment',
                            filename=os.path.basename(path))
            message.attach(part)

        # log in to email client if not already.
        if not self._connected:
            self._login()

        # handle disconnect and connection errors by
        # quick login and attempt to send again
        try:
            self._smtp.sendmail(self._config.sender_email,
                                destinations,
                                message.as_string())
        except (smtplib.SMTPConnectError, smtplib.SMTPServerDisconnected):
            self._login()
            self._smtp.sendmail(self._config.sender_email,
                                destinations,
                                message.as_string())
        finally:
            self._logout()


class Message:
    def __init__(self, ):
        """
        Args:
            config (Optional(config.credentials.Credentials)): The constructed
                credentials. Can be None if environment variables are
                configured.
            delay_login (bool): If True, no login attempt will be made until
                send_mail is called. Otherwise, a login attempt will be made at
                class initialization.
        """
        self.subject = subject or ''
        self.sender = sender
        self.receivers = receivers
        self.authors = authors
        self.cc = cc
        self.bcc = bcc

        self._connected = False
        if not delay_login:
            self._login()
