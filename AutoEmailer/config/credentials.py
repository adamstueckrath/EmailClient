import six
import json
import io


class Credentials:
    """

    """

    def __init__(self, sender_email=None, password=None,
                 port=None, host=None):
        self._sender_email = sender_email
        self._password = password
        self._port = port
        self._host = host

    @property
    def sender_email(self):
        return self._sender_email

    @property
    def password(self):
        return self._password

    @property
    def port(self):
        return self._port

    @property
    def host(self):
        return self._host

    @staticmethod
    def fill_missing_user_info(info):
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
                raise ValueError('Cannot guess host given email.')
        return info

    @classmethod
    def from_authorized_user_info(cls, info):
        """Creates a Credentials instance from parsed authorized user info.
        Args:
            info (Mapping[str, str]): The authorized user info in Google
                format.
            scopes (Sequence[str]): Optional list of scopes to include in the
                credentials.
        Returns:
            google.oauth2.credentials.Credentials: The constructed
                credentials.
        Raises:
            ValueError: If the info is not in the expected format.
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
            file_name (str): The path to the authorized user json file.
            scopes (Sequence[str]): Optional list of scopes to include in the
                credentials.
        Returns:
            google.oauth2.credentials.Credentials: The constructed
                credentials.
        Raises:
            ValueError: If the file is not in the expected format.
        """
        with io.open(file_name, 'r', encoding='utf-8') as json_file:
            try:
                data = json.load(json_file)
            except ValueError as exc:
                raise 'File {} is not a valid json file. {}'.format(file_name, exc)
            return cls.from_authorized_user_info(data)
