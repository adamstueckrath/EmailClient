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
            sender_email (Optional[str]): The user name to authenticate SMTP
                client. Can be None if environment variables are configured.
                Equivalent environment variable: `EMAILER_SENDER`.
            password (Optional[str]): The password to authenticate SMTP client.
                Can be None if environment variables are configured.
                Equivalent environment variable: `EMAILER_PASSWORD`.
            port (Optional[str]): The port number of SMTP server.
                Equivalent environment variable: `EMAILER_HOST`.
                If neither config nor environment variable are set, then it
                will default to 587.
            host (Optional[str]): Host name of SMTP server.
                Equivalent environment variable: `EMAILER_PORT`.
                If neither config nor environment variable are set, then it
                will attempt to guess the host from the `emailer_address`.

        Warnings:
            Raises warning if port or host are none.
        """
        self._sender_email = sender_email
        self._password = password
        self._port = port
        self._host = host
        if (self._port is None) or (self._host is None):
            warnings.simplefilter("always")
            warnings.warn('If explicitly passing args to initialize '
                          'Credentials, please pass in `port` and `host` or '
                          'use environment variables for configuration '
                          '{} and {}'.format(environment_vars.EMAILER_PORT,
                                             environment_vars.EMAILER_HOST)
                          )

    @property
    def sender_email(self):
        """User name for SMTP client."""
        return self._sender_email

    @property
    def password(self):
        """Password for SMTP client."""
        return self._password

    @property
    def port(self):
        """Port where SMTP server is listening."""
        return self._port

    @property
    def host(self):
        """SMTP server host name."""
        return self._host

    @staticmethod
    def fill_missing_user_info(info):
        """Fills in automatically assigns `EMAILER_PORT` or `EMAILER_HOST` if
        they not set. Sets the default port to 587 and attempts to guess the
        host from the `EMAILER_SENDER`.

        Args:
            info (dict): Config dictionary object in auto_emailer format for
                initializing :func:`auto_emailer.config.credentials.Credentials`
                class instance.

        Returns:
            dict: Dictionary object with missing information filled.

        Raises:
            ValueError: If it cannot guess `EMAILER_HOST` from `EMAILER_SENDER`.
        """
        if not info or not isinstance(info, dict):
            return info

        if (info['EMAILER_PORT'] is None) or (info['EMAILER_PORT'] is ""):
            info['EMAILER_PORT'] = 587

        if (info['EMAILER_HOST'] is None) or (info['EMAILER_HOST'] is ""):
            if ('@outlook.com' in info['EMAILER_SENDER']) or \
                    ('@hotmail.com' in info['EMAILER_SENDER']):
                info['EMAILER_HOST'] = 'smtp.office365.com'
            elif '@gmail.com' in info['EMAILER_SENDER']:
                info['EMAILER_HOST'] = 'smtp.gmail.com'
            elif '@yahoo.com' in info['EMAILER_SENDER']:
                info['EMAILER_HOST'] = 'smtp.mail.yahoo.com'
            else:
                raise ValueError('Cannot guess host given email. '
                                 'Please explicitly set `EMAILER_HOST`.')

        return info

    @classmethod
    def from_authorized_user_info(cls, info):
        """Creates a Credentials instance from parsed authorized user info.

        Args:
            info (dict): Config dictionary object in auto_emailer format for
                initializing :func:`auto_emailer.config.credentials.Credentials`
                class instance.

        Returns:
            auto_emailer.config.credentials.Credentials: The
            constructed credentials created from user configuration object.

        Raises:
            ValueError: If the authorized user info is not in the expected
                format (missing keys).
        """
        keys_needed = {'EMAILER_SENDER', 'EMAILER_PASSWORD',
                       'EMAILER_HOST', 'EMAILER_PORT'}
        missing = keys_needed.difference(six.iterkeys(info))

        if missing:
            raise ValueError('Authorized user info was not in the expected '
                             'format, missing fields {}.'
                             .format(', '.join(missing))
                             )

        cls.fill_missing_user_info(info)

        return Credentials(
            sender_email=info['EMAILER_SENDER'],
            password=info['EMAILER_PASSWORD'],
            host=info['EMAILER_HOST'],
            port=info['EMAILER_PORT'])

    @classmethod
    def from_authorized_user_file(cls, file_name):
        """Creates a Credentials instance from an authorized user json file.

        Args:
            file_name (str): The string path to the authorized user json file

        Returns:
            auto_emailer.config.credentials.Credentials: The
            constructed credentials created from user file attributes.

        Raises:
            ValueError: If the authorized user file is not in the expected
                format (json).
        """
        with io.open(file_name, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except ValueError:
                raise ValueError('File {} is not a valid json file.'
                                 .format(file_name)
                                 )
            return cls.from_authorized_user_info(data)
