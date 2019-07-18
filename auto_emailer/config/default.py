from .credentials import Credentials
from auto_emailer.config import environment_vars
import os


def _get_settings_from_environ():
    """
    NOT IN USE. FOR FUTURE VERSION.

    :return:
    """
    # for key in environment_vars:
    #     if key in os.environ:
    #         return os.environ[key]
    return


def _get_explicit_environ_credential_file():
    """
    Gets file path from emailer_credentials environment
    variable. If file is found, it will load the json file variables and returned.

    :return: class
        config.credentials.Credentials: The constructed credentials.
    """
    explicit_file = os.environ.get(environment_vars.CREDENTIALS_ENVIR_PATH)

    if explicit_file is not None:
        credentials = Credentials.from_authorized_user_file(os.environ[environment_vars.CREDENTIALS_ENVIR_PATH])
        return credentials
    else:
        return None


def _get_explicit_environ_credentials():
    """
    Checks for any environment variables. If variables found, then
    they are loaded and returned.

    :return: class
        config.credentials.Credentials: The constructed credentials.
    :raises: EnvironmentError
        If credentials were found and are invalid.
    """
    #  check if there are ANY environment variables set
    if not any(env_vars.startswith('emailer') for env_vars in os.environ.keys()):
        return None

    # build environment variables into dict
    info = dict()
    info[environment_vars.ENVIR_SENDER] = os.environ.get(environment_vars.ENVIR_SENDER)
    info[environment_vars.ENVIR_PASSWORD] = os.environ.get(environment_vars.ENVIR_PASSWORD)
    info[environment_vars.ENVIR_HOST] = os.environ.get(environment_vars.ENVIR_HOST)
    info[environment_vars.ENVIR_PORT] = os.environ.get(environment_vars.ENVIR_PORT)

    # if no values are found for emailer_sender or emailer_password, raise error
    if (info[environment_vars.ENVIR_SENDER] is None or
            info[environment_vars.ENVIR_PASSWORD] is None):
        raise EnvironmentError(
            'The environment credentials do not contain the necessary fields need to '
            'authenticate. You must specify emailer_sender and '
            'emailer_password'
        )

    credentials = Credentials.from_authorized_user_info(info)
    return credentials


def default():
    """
    Gets the default credentials for the current environment. Default credentials
    provides an easy way to obtain credentials to call auto_emailer.
    This function acquires credentials from the environment in the following
    order:
    1. If the environment variable `emailer_credentials` is set
       to the path of a valid JSON file, then it is loaded and returned.
    2. If explicit environment variables are set, then the credentials
       are loaded and returned.

    :return: class
        config.credentials.Credentials: The constructed credentials.

    :raises: EnvironmentError
        If no credentials were found, or if the credentials found were invalid.
    """
    # order of credential check
    checkers = (
        _get_explicit_environ_credential_file,
        _get_explicit_environ_credentials)

    # check if credentials exist, if so return credentials, else raise error
    for checker in checkers:
        credentials = checker()
        if credentials is not None:
            return credentials

    raise EnvironmentError(
        'Could not automatically determine credentials. '
        'Please set {env} or explicitly set environment '
        'credentials and re-run the application. For more '
        'information, please see config.environment_vars'.format(env=environment_vars.CREDENTIALS_ENVIR_PATH)
    )
