import os
import datetime
import smtplib
from .config import credentials, default
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
        :param config: class
            config.credentials.Credentials: The constructed credentials.
        :param delay_login: bool
            if True, no login attempt will be made until send_mail
            is called. Otherwise, a login attempt will be made
            at construction time.
        """
        if (config is not None and
                not isinstance(config, credentials.Credentials)):
            raise ValueError('Emailer library only supports credentials from '
                             'auto_emailer.config See auto_emailer.config.credentials '
                             'and auto_emailer.config.environment_vars '
                             'for help on authentication with this library.')
        elif config is None:
            self._config = default()
        elif isinstance(config, credentials.Credentials):
            self._config = config
        else:
            raise ValueError('Unknown credential configuration. Please '
                             'consult the docs: ')

        self._logged_in = False
        if not delay_login:
            self._login()

    @property
    def logged_in(self):
        """
        :return: bool if user is logged in or not.
        """
        return self._logged_in

    def _logout(self):
        """
        Quits the connection to the smtp server.
        """
        self._smtp.quit()

    def _login(self):
        """
        Uses the class property config to login.
        """
        self._smtp = smtplib.SMTP(host=self._config.host, port=self._config.port, timeout=10)
        self._smtp.starttls()
        self._smtp.login(self._config.sender_email, self._config.password)
        self._logged_in = True

    @staticmethod
    def email_template(template_path):
        """
        Opens, reads, and returns the given template file path as a string.

        :param template_path: str
            File path for the email template.
        :raises: FileNotFoundError
            If it cannot find the file from given `template_path`.
        :return: str
            Text of template file.
        """
        try:
            template_text = Path(template_path).read_text()
        except FileNotFoundError:
            raise('File path not found: {}'.format(template_path))
        return template_text

    def send_email(self, destinations, subject, text=None,
                   template_path=None, template_args=None, attach_files=None):
        """
        Send an email to given destination list. The email will auto fill
        the FROM with config.sender_email.

        :param destinations: list
            List of strings of email addresses to send the email to.
        :param subject: str
            Subject of your email.
        :param text: str
            The body text of your email.
        :param template_path: str
            File path of an email template text to use for the email body.
        :param template_args: dict
            Keyword arguments to format the email template text.
        :param attach_files: list
            List of file paths to attached to email.
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

        # log in to email client if not already.
        if not self._logged_in:
            self._login()

        # handle disconnect and connection errors by quick login and attempt to send again
        try:
            self._smtp.sendmail(self._config.sender_email, destinations, message.as_string())
        except smtplib.SMTPConnectError:
            self._login()
            self._smtp.sendmail(self._config.sender_email, destinations, message.as_string())
        finally:
            self._logout()
