from pathlib import Path
import json
import unittest
from unittest import mock
from auto_emailer.config import default, credentials

DATA_DIR = Path(__file__).resolve().parents[1] / 'data'
MOCK_USER_JSON_FILE = str(DATA_DIR / 'mock_credentials.json')
MOCK_USER_CSV_FILE = str(DATA_DIR / 'mock_credentials.csv')




def _make_credentials():
    import auto_emailer.config.credentials
    return mock.Mock(spec=auto_emailer.config.credentials.Credentials)


class TestCredentials(unittest.TestCase):

    def test_constructor_defaults(self):
        credentials = _make_credentials()
        patch1 = mock.patch("auto_emailer.config.default", return_value=(credentials, None))

        project = "prahj-ekt"
        patch2 = mock.patch(
            "google.cloud.client._determine_default_project", return_value=project
        )

        with patch1 as default:
            with patch2 as _determine_default_project:
                client_obj = self._make_one()

        self.assertEqual(client_obj.project, project)
        self.assertIs(client_obj._credentials, credentials)
        self.assertIsNone(client_obj._http_internal)
        default.assert_called_once_with()
        _determine_default_project.assert_called_once_with(None)
