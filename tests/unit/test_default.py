import os
import json
import unittest
from unittest import mock
from auto_emailer.config import default, credentials

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')
MOCK_USER_JSON_FILE = os.path.join(DATA_DIR, 'mock_credentials.json')


def _get_mock_credentials():
    with open(MOCK_USER_JSON_FILE, 'r') as creds:
        return json.load(creds)


def _make_credentials():
    return mock.Mock(spec=credentials.Credentials)


class TestDefault(unittest.TestCase):
    @mock.patch('os.environ.get', {'emailer_credentials': None}.get)
    def test_explicit_environ_credential_no_file(self):
        test = default._get_explicit_environ_credential_file()
        self.assertEqual(test, None)

    @mock.patch('os.environ.get', {'emailer_credentials': MOCK_USER_JSON_FILE}.get)
    def test_explicit_environ_credential_file(self):
        mock_creds = _make_credentials()
        test = default._get_explicit_environ_credential_file()
        # self.assertEqual(test, mock_creds)


if __name__ == '__main__':
    unittest.main()
