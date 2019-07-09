import os
import json
from collections import defaultdict


class EmailerConfig:
    """
    Order for the following information is
    config -> environment variable
    """

    def __init__(self, file_path=None, required=None):
        """
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
        """
        self._config_dict = defaultdict()  # added defaultdict for guess logic
        self._config_file = file_path or os.getenv('EMAILER_CREDENTIALS', None)
        self._required = required or ['sender_email', 'password']
        if self._config_file is not None:
            self._config_dict = self.from_file_name(self.config_file)
        else:
            self._config_dict = self.build_config()

    @property
    def config(self):
        return self._config_dict

    @property
    def config_file(self):
        return self._config_file

    @property
    def required(self):
        return self._required

    def get_config_property(self, property_name):
        # If key doesn't exist, it return None by default.
        return self._config_dict.get(property_name)

    @staticmethod
    def from_file_name(file_path):
        """
        Reads a JSON file
        and returns its parsed info.

        :param file_path: string
            Path to the service account .json file.
        :return: dictionary
            Credential data.
        """
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            assert isinstance(data, dict), "The data must be a dictionary instance."
            return data

    def validate_dict(self, creds_dict):
        """
        Validates a dictionary containing Google service account data.
        :raises ValueError:
            If data was in the wrong format, or if one of the
            required keys is missing.
        :return: None
        """
        keys_needed = set(self._required if self._required is not None else [])
        print(keys_needed)
        missing = keys_needed.difference(creds_dict.keys())
        print('missing {}'.format(missing))
        if missing:
            raise ValueError('Credentials info was not in the '
                             'expected format, missing fields: {}.'.format(', '.join(missing))
                             )

    def build_config(self):
        config = dict()
        config['sender_email'] = self._config_dict.get('EMAILER_ADDRESS', os.environ.get('EMAILER_ADDRESS'))
        config['password'] = self._config_dict.get('EMAILER_PASSWORD', os.environ.get('EMAILER_PASSWORD'))
        config['port'] = self._config_dict.get('EMAILER_PORT', os.getenv('EMAILER_PORT'))
        if config['port'] is None:
            config['port'] = 587

        config['host'] = self._config_dict.get('EMAILER_HOST', os.getenv('EMAILER_HOST'))
        self.validate_dict(config)

        # if config['host'] is None:
        #     if ('@outlook.com' in config['sender_email']) or ('@hotmail.com' in config['sender_email']):
        #         config['host'] = 'smtp.office365.com'
        #     elif '@gmail.com' in config['sender_email']:
        #         config['host'] = 'smtp.gmail.com'
        #     elif '@yahoo.com' in config['sender_email']:
        #         config['host'] = 'smtp.mail.yahoo.com'
        #     else:
        #         raise ValueError('Cannot guess host given email.')

        return config


if __name__ == '__main__':
    test_config = EmailerConfig()
    print(test_config.config_file)
    print(test_config.required)
    print(test_config.config)
