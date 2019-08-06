import json
import unittest
from pathlib import Path

from auto_emailer.config import credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_ENVIR_JSON_FILE = DATA_DIR / 'mock_envir_credentials.json'
USER_USER_JSON_FILE = DATA_DIR / 'mock_user_credentials.json'
MOCK_USER_CSV_FILE = DATA_DIR / 'mock_credentials.csv'


def _get_mock_credentials(file):
    with file.open() as creds:
        return json.load(creds)


class TestCredentials(unittest.TestCase):

    def test_credentials_warning(self):
        """Test credentials.Credentials raise warning
        if explicitly passing args to initialize Credentials, '
        and `port` or `host` are not set.'
        """
        with self.assertWarns(Warning):
            credentials.Credentials()

    def test_credentials_properties(self):
        """Test initializing an instance of credentials.Credentials,
        and validates explicitly passing args class object.Also test
        each class property call.
        """
        data = _get_mock_credentials(USER_USER_JSON_FILE)
        creds = credentials.Credentials(**data)
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_fill_missing_user_error(self):
        """Test credentials.Credentials.fill_missing_user_info()
        raise ValueError if given missing data and unknown email address.
        """
        data = {"emailer_sender": "test@gmailsssssssss.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        with self.assertRaises(ValueError):
            credentials.Credentials.fill_missing_user_info(data)

    def test_credentials_fill_missing_user_info_empty(self):
        """Test credentials.Credentials.fill_missing_user_info()
        returns argument if data is not a data type: dictionary
        or is None.
        """
        self.assertEqual(credentials.Credentials.fill_missing_user_info({}), {})

    def test_credentials_fill_missing_user_info(self):
        """Test credentials.Credentials.fill_missing_user_info()
        returns expected values if passed missing `host` or `port`.
        """
        data = {"emailer_sender": "test@gmail.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        creds = credentials.Credentials.fill_missing_user_info(data)
        self.assertEqual(creds['emailer_port'], 587)
        self.assertEqual(creds['emailer_host'], 'smtp.gmail.com')

    def test_credentials_from_authorized_user_info_error(self):
        """Test class method: credentials.Credentials.from_authorized_user_info()
        raises ValueError if dict argument is None or missing expected keys.
        """
        with self.assertRaises(ValueError):
            credentials.Credentials.from_authorized_user_info({})

    def test_credentials_from_authorized_user_info_filled_info(self):
        """Test class method: credentials.Credentials.from_authorized_user_info()
        calls credentials.Credentials.fill_missing_user_info() to fill missing values
        and initializes credentials.Credentials instance with expected values.
        """
        data = {"emailer_sender": "test@gmail.com",
                "emailer_password": "mypassword",
                "emailer_host": "",
                "emailer_port": ""
                }
        creds = credentials.Credentials.from_authorized_user_info(data)
        self.assertIsInstance(creds, credentials.Credentials)
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_from_authorized_user_info(self):
        """Test class method: credentials.Credentials.from_authorized_user_info()
        initializes credentials.Credentials instance with expected values.
        """
        data = _get_mock_credentials(MOCK_ENVIR_JSON_FILE)
        creds = credentials.Credentials.from_authorized_user_info(data)
        self.assertIsInstance(creds, credentials.Credentials)
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)

    def test_credentials_from_authorized_user_file_error(self):
        """Test class object: credentials.Credentials.from_authorized_user_info()
        raises ValueError if file format is not json.
        """
        with self.assertRaises(ValueError):
            credentials.Credentials.from_authorized_user_file(MOCK_USER_CSV_FILE)

    def test_credentials_from_authorized_user_file(self):
        """Test class method: credentials.Credentials.from_authorized_user_file()
        opens json file into python data type dict and then calls
        credentials.Credentials.from_authorized_user_info() to
        initialize credentials.Credentials instance with expected values.
        """
        creds = credentials.Credentials.from_authorized_user_file(MOCK_ENVIR_JSON_FILE)
        self.assertIsInstance(creds, credentials.Credentials)
        self.assertEqual(creds.sender_email, 'test@gmail.com')
        self.assertEqual(creds.password, 'mypassword')
        self.assertEqual(creds.host, 'smtp.gmail.com')
        self.assertEqual(creds.port, 587)


if __name__ == '__main__':
    unittest.main()
