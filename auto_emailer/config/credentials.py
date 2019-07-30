import six
import json
import io
import warnings
from auto_emailer.config import environment_vars


class Credentials:
    """
    Configure credentials to the Auto Emailer.
    """

    def __init__(self, sender_email=None, password=None,
                 port=None, host=None):
        """
        :param sender_email: str
            The user name to authenticate with.
            Equivalent environment variable: emailer_address.
        :param password: str
            The password for the authentication.
            Equivalent environment variable: emailer_password
        :param port: int
            Port number, equivalent environment variable: emailer_port.
            If neither config nor environment variable is set,
            then it will default to 587.
        :param host: str
            Domain name of host, equivalent environment variable: emailer_host.
            If neither config nor environment variable is set,
            then we attempt to guess the host from the emailer_address.
        """
        self._sender_email = sender_email
        self._password = password
        self._port = port
        self._host = host
        if (self._port is None) or (self._host is None):
            warnings.simplefilter("always")
            warnings.warn('If explicitly passing args to initialize Credentials, '
                          'please pass in `port` and `host` or use environment '
                          'variables for configuration {} and {}'.format(environment_vars.ENVIR_PORT,
                                                                         environment_vars.ENVIR_HOST),
                          )

    @property
    def sender_email(self):
        """
        :return: sender (username) email address.
        """
        return self._sender_email

    @property
    def password(self):
        """
        :return: sender (user) email password.
        """
        return self._password

    @property
    def port(self):
        """
        :return: port where SMTP server is listening.
        """
        return self._port

    @property
    def host(self):
        """"
        :return: SMTP server host name.
        """
        return self._host

    @staticmethod
    def fill_missing_user_info(info):
        """
        If `emailer_port` or `emailer_host` is not set,
        sets the default port to 587 and attempts to guess the host
        from the `emailer_sender`.

        :param info: dict
            The authorized user info in auto_emailer format.
        :return: dict
            Constructed user credentials.
        :raises: ValueError
            If it cannot guess host from `emailer_sender`.
        """
        if info['emailer_port'] is None:
            info['emailer_port'] = 587

        if info['emailer_host'] is None:
            if ('@outlook.com' in info['emailer_sender']) or ('@hotmail.com' in info['emailer_sender']):
                info['emailer_host'] = 'smtp.office365.com'
            elif '@gmail.com' in info['emailer_sender']:
                info['emailer_host'] = 'smtp.gmail.com'
            elif '@yahoo.com' in info['emailer_sender']:
                info['emailer_host'] = 'smtp.mail.yahoo.com'
            else:
                raise ValueError('Cannot guess host given email. Please explicitly set `emailer_host`.')
        return info

    @classmethod
    def from_authorized_user_info(cls, info):
        """
        Creates a Credentials instance from parsed authorized user info.

        :param info: dict
            The authorized user info in auto_emailer format.
        :return: class
            config.credentials.Credentials: The constructed credentials.
        :raises: ValueError
            If the info is not in the expected format.
        """
        keys_needed = {'emailer_sender', 'emailer_password', 'emailer_port', 'emailer_host'}
        missing = keys_needed.difference(six.iterkeys(info))

        if missing:
            raise ValueError(
                'Authorized user info was not in the expected format, missing '
                'fields {}.'.format(', '.join(missing)))

        cls.fill_missing_user_info(info)

        return Credentials(
            sender_email=info['emailer_sender'],
            password=info['emailer_password'],
            host=info['emailer_host'],
            port=info['emailer_port'])

    @classmethod
    def from_authorized_user_file(cls, file_name):
        """
        Creates a Credentials instance from an authorized user json file.

        :param file_name: str
            The path to the authorized user json file.
        :return: class
            config.credentials.Credentials: The constructed credentials.
        :raises: ValueError
            If the file is not in the expected format.
        """
        with io.open(file_name, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except ValueError as exc:
                raise 'File {} is not a valid json file. {}'.format(file_name, exc)
            return cls.from_authorized_user_info(data)
