from credentials import Credentials
import environment_vars
import os


def _get_explicit_environ_credentials_path():
    """Gets credentials from the GOOGLE_APPLICATION_CREDENTIALS environment
    variable."""
    explicit_file = os.environ.get(environment_vars.CREDENTIALS_ENVIR_PATH)

    if explicit_file is not None:
        credentials = Credentials.from_authorized_user_file(os.environ[environment_vars.CREDENTIALS_ENVIR_PATH])
        return credentials
    else:
        return None


def _get_explicit_environ_credentials():
    info = dict()
    info[environment_vars.ENVIR_SENDER] = os.environ.get(environment_vars.ENVIR_SENDER)
    info[environment_vars.ENVIR_PASSWORD] = os.environ.get(environment_vars.ENVIR_PASSWORD)
    info[environment_vars.ENVIR_HOST] = os.environ.get(environment_vars.ENVIR_HOST)
    info[environment_vars.ENVIR_PORT] = os.environ.get(environment_vars.ENVIR_PORT)

    if (info[environment_vars.ENVIR_SENDER] is None or
            info[environment_vars.ENVIR_PASSWORD] is None):
            raise EnvironmentError(
                'The credentials do not contain the necessary fields need to '
                'refresh the access token. You must specify refresh_token, '
                'token_uri, client_id, and client_secret.')

    credentials = Credentials.from_authorized_user_info(info)
    return credentials


def default():
    checkers = (
        _get_explicit_environ_credentials_path,
        _get_explicit_environ_credentials)

    for checker in checkers:
        credentials = checker()
        if credentials is not None:
            credentials = credentials.Credentials(credentials)
            return credentials

if __name__ == '__main__':
    test = _get_explicit_environ_credentials()
    print(test)
