import os
from pathlib import Path
import json
import unittest
from unittest import mock
from auto_emailer.config import default, credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_USER_JSON_FILE = str(DATA_DIR / 'mock_credentials.json')
MOCK_USER_CSV_FILE = str(DATA_DIR / 'mock_credentials.csv')


def _get_mock_credentials():
    with open(MOCK_USER_JSON_FILE, 'r') as creds:
        return json.load(creds)


def _make_credentials():
    return mock.Mock(spec=credentials.Credentials)


class TestDefault(unittest.TestCase):
    @mock.patch('os.environ', {'emailer_credentials': None})
    def test_explicit_environ_credential_no_file(self):
        """
        Test default._get_explicit_environ_credential_file
        returns None if 'emailer_credentials' set to None.
        """
        test = default._get_explicit_environ_credential_file()
        self.assertEqual(test, None)

    @mock.patch('os.environ', {'emailer_credentials': MOCK_USER_JSON_FILE})
    def test_explicit_environ_credential_file(self):
        """
        Test default._get_explicit_environ_credential_file
        returns class credentials.Credentials class
        if json file found in os.environ.get('emailer_credentials').
        """
        with mock.patch("auto_emailer.config.default.Credentials.from_authorized_user_file",
                        return_value=credentials.Credentials) as my_test:
            self.assertIs(default._get_explicit_environ_credential_file(),
                          credentials.Credentials)
            self.assertEqual(my_test.call_count, 1)

    @mock.patch('os.environ', {'emailer_credentials': MOCK_USER_CSV_FILE})
    def test_explicit_environ_credential_bad_file(self):
        """
        Test default._get_explicit_environ_credential_file
        raises ValueError if file is not JSON and
        found in os.environ.get('emailer_credentials').
        """
        with mock.patch("auto_emailer.config.default.Credentials.from_authorized_user_file",
                        side_effect=ValueError) as my_test:
            with self.assertRaises(ValueError):
                default._get_explicit_environ_credential_file()

    @mock.patch('os.environ', {'Hello_test': 'Testing', 'My_test': None})
    def test_get_explicit_environ_credentials_no_creds(self):
        """
        Test default._get_explicit_environ_credentials
        returns None if no environ variables are set.
        """
        self.assertEqual(default._get_explicit_environ_credentials(), None)

    @mock.patch('os.environ', {'emailer_sender': 'test@gmail.com', 'emailer_test': None})
    def test_get_explicit_environ_credentials_some_creds(self):
        """
        Test default._get_explicit_environ_credentials
        raises EnvironmentError if some variables are set but
        not all to initialize credentials.Credentials class.
        """
        with self.assertRaises(EnvironmentError):
            default._get_explicit_environ_credentials()

    @mock.patch('os.environ', _get_mock_credentials())
    def test_get_explicit_environ_credentials_creds(self):
        """
        Test default._get_explicit_environ_credentials
        initializes credentials.Credentials class if environment
        variables are set.
        """
        with mock.patch("auto_emailer.config.default.Credentials.from_authorized_user_info",
                        return_value=credentials.Credentials) as my_test:
            creds = default._get_explicit_environ_credentials()
            self.assertIs(creds,
                          credentials.Credentials)
            self.assertEqual(my_test.call_count, 1)

    @mock.patch("auto_emailer.config.default._get_explicit_environ_credential_file",
                return_value=None)
    @mock.patch("auto_emailer.config.default._get_explicit_environ_credentials",
                return_value=None)
    def test_default_credentials_none(self, mock_explicit, mock_environ):
        """
        Test default.default_credentials raises EnvironmentError
        if environment variables or file are not set..
        """ 
        with self.assertRaises(EnvironmentError):
            default.default_credentials()
            self.assertEqual(mock_explicit.call_count, 1)
            self.assertEqual(mock_environ.call_count, 1)

    # # @mock.patch('os.environ', {'emailer_credentials': MOCK_USER_JSON_FILE})
    # # @mock.patch("auto_emailer.config.default._get_explicit_environ_credential_file")
    # # @mock.patch("auto_emailer.config.default._get_explicit_environ_credentials")
    # def test_default_credentials(self):
    #     with mock.patch("auto_emailer.config.default._get_explicit_environ_credential_file") as my_test:
    #         t = default.default_credentials()
    #         print(t)
    #         print(t.return_value)
    #         print(my_test)
    #         print(my_test.return_value)
    #     # self.assertEqual(mock_explicit.call_count, 1)
    #     # self.assertEqual(mock_environ.call_count, 0)


if __name__ == '__main__':
    unittest.main()
