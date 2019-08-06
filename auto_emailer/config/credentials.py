import io
import json
import warnings

import six

from auto_emailer.config import environment_vars


class Credentials:
    """Base class for Auto Emailer credentials."""

    def __init__(self, sender_email=None, password=None,
                 port=None, host=None):
        """
        Args:
            sender_email (Optional(str)): The user name to authenticate SMTP client.
                Can be None if environment variables are configured. Equivalent environment
                variable: `emailer_address`.
            password (Optional(str)): The password to authenticate SMTP client.
                Can be None if environment variables are configured. Equivalent environment
                variable: `emailer_password`.
            port (Optional(int)): The port number of SMTP server. Equivalent environment
                variable: `emailer_port`. If neither config nor environment variable are set,
                then it will default to 587.
            host (Optional(str)): Host name of SMTP server. Equivalent environment
                variable: `emailer_host`. If neither config nor environment variable are set,
                then it will attempt to guess the host from the `emailer_address`.

        Warnings: Raises warning if port or host are none.
        """
        self._sender_email = sender_email
        self._password = password
        self._port = port
        self._host = host
        if (self._port is None) or (self._host is None):
            warnings.simplefilter("always")
            warnings.warn('If explicitly passing args to initialize Credentials, '
                          'please pass in `port` and `host` or use environment '
                          'variables for configuration {} and {}'
                          .format(environment_vars.ENVIR_PORT,
                                  environment_vars.ENVIR_HOST)
                          )

    @property
    def sender_email(self):
        """
        Returns:
            str: User name for SMTP client.
        """
        return self._sender_email

    @property
    def password(self):
        """
        Returns:
            str: Password for SMTP client.
        """
        return self._password

    @property
    def port(self):
        """
        Returns:
            str: Port where SMTP server is listening.
        """
        return self._port

    @property
    def host(self):
        """"
        Returns:
            str: SMTP server host name.
        """
        return self._host

    @staticmethod
    def fill_missing_user_info(info):
        """Fills in automatically assigns `emailer_port` or `emailer_host` if they not set.
        sets the default port to 587 and attempts to guess the host from the `emailer_sender`.

        Args:
            info (dict): Config dictionary object in auto_emailer format for initializing
                `auto_emailer.config.credentials.Credentials` class instance.

        Returns:
            dict: Dictionary object with missing information filled.

        Raises:
            ValueError: If it cannot guess `emailer_host` from `emailer_sender`.
        """
        if not info or not isinstance(info, dict):
            return info

        if (info['emailer_port'] is None) or (info['emailer_port'] is ""):
            info['emailer_port'] = 587

        if (info['emailer_host'] is None) or (info['emailer_host'] is ""):
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
        """Creates a Credentials instance from parsed authorized user info.

        Args:
            info (dict): Config dictionary object in auto_emailer format for initializing 
                `auto_emailer.config.credentials.Credentials` class instance. 

        Returns:
            auto_emailer.config.credentials.Credentials: The constructed credentials created from
            user configuration object.

        Raises:
            ValueError: If the authorized user info is not in the expected format (missing keys).
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
        """Creates a Credentials instance from an authorized user json file.

        Args:
            file_name (str): The string path to the authorized user json file

        Returns:
            auto_emailer.config.credentials.Credentials: The constructed credentials created from
            user file attributes.

        Raises:
            ValueError: If the authorized user file is not in the expected format (json).
        """
        with io.open(file_name, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except ValueError:
                raise ValueError('File {} is not a valid json file.'.format(file_name))
            return cls.from_authorized_user_info(data)
