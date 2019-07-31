import json
import unittest
from pathlib import Path
from auto_emailer.config.credentials import Credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_USER_JSON_FILE = str(DATA_DIR / 'mock_envir_credentials.json')
USER_CREDS_JSON_FILE = str(DATA_DIR / 'user_credentials.json')
MOCK_USER_CSV_FILE = str(DATA_DIR / 'mock_credentials.csv')


def _get_mock_credentials(file):
    with open(file, 'r') as creds:
        return json.load(creds)


class TestCredentials(unittest.TestCase):

    def test_credentials_warning(self):
        with self.assertWarns(Warning):
            Credentials()

    def test_credentials_properties(self):
        creds = Credentials(**_get_mock_credentials(USER_CREDS_JSON_FILE))
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_fill_missing_user_error(self):
        """
        """
        data = {"emailer_sender": "test@gmailsssssssss.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        with self.assertRaises(ValueError):
            Credentials.fill_missing_user_info(data)

    def test_credentials_fill_missing_user_info_empty(self):
        """
        """
        self.assertEqual(Credentials.fill_missing_user_info({}), {})

    def test_credentials_fill_missing_user_info(self):
        """
        """
        data = {"emailer_sender": "test@gmail.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        creds = Credentials.fill_missing_user_info(data)
        self.assertEqual(creds['emailer_port'], 587)
        self.assertEqual(creds['emailer_host'], 'smtp.gmail.com')

    def test_credentials_from_authorized_user_info_error(self):
        """
        """
        with self.assertRaises(ValueError):
            Credentials.from_authorized_user_info({})

    def test_credentials_from_authorized_user_info_filled_info(self):
        """
        """
        data = {"emailer_sender": "test@gmail.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        creds = Credentials.from_authorized_user_info(data)
        self.assertIsInstance(creds, Credentials)
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_from_authorized_user_info(self):
        """
        """
        data = _get_mock_credentials(MOCK_USER_JSON_FILE)
        creds = Credentials.from_authorized_user_info(data)
        self.assertIsInstance(creds, Credentials)
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_from_authorized_user_file_error(self):
        """
        """
        with self.assertRaises(ValueError):
            Credentials.from_authorized_user_file(MOCK_USER_CSV_FILE)

    def test_credentials_from_authorized_user_file(self):
        """
        """
        creds = Credentials.from_authorized_user_file(MOCK_USER_JSON_FILE)
        self.assertIsInstance(creds, Credentials)
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)


if __name__ == '__main__':
    unittest.main()
