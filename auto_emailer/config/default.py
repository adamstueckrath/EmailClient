import os

from auto_emailer.config import environment_vars
from auto_emailer.config.credentials import Credentials


def _get_explicit_environ_credential_file():
    """Gets file path from
    `auto_emailer.config.environment_vars.emailer_credentials` environment
    variable. If file is found, it will load the json file variables and
    return class.

    Creates and returns a :class:`auto_emailer.config.credentials.Credentials`
    instance from the environment variable json file attributes.

    Returns:
        auto_emailer.config.credentials.Credentials: The constructed
        credentials created from the environment variable's
        :func:`auto_emailer.config.environment_vars.EMAILER_CREDS`
        file attributes or `None`.
    """
    explicit_file = os.environ.get(environment_vars.EMAILER_CREDS)
    if explicit_file is not None:
        credentials = Credentials.from_authorized_user_file(explicit_file)
        return credentials
    else:
        return None


def _get_explicit_environ_credentials():
    """Checks for any environment variables defined in
    `auto_emailer.config.environment_vars`. If variables found, then
    they are loaded and returned.

    Creates and returns a :class:`auto_emailer.config.credentials.Credentials`
    instance from the environment variables.

    Returns:
        auto_emailer.config.credentials.Credentials: The constructed
        credentials created from the environment variables defined in
        :func:`auto_emailer.config.environment_vars`

    Raises:
        EnvironmentError: If environment variable credentials are defined and
            set to None. Specifically checks, `EMAILER_SENDER` and
            `EMAILER_PASSWORD`.
    """
    #  check if there are ANY environment variables set
    if not any(env_vars.startswith('EMAILER') for env_vars
               in os.environ.keys()):
        return None

    # build environment variables into dict
    info = dict()
    info[environment_vars.EMAILER_SENDER] = os.environ.get(
                                            environment_vars.EMAILER_SENDER)
    info[environment_vars.EMAILER_PASSWORD] = os.environ.get(
                                            environment_vars.EMAILER_PASSWORD)
    info[environment_vars.EMAILER_HOST] = os.environ.get(
                                            environment_vars.EMAILER_HOST)
    info[environment_vars.EMAILER_PORT] = os.environ.get(
                                            environment_vars.EMAILER_PORT)

    # if no values are found for emailer_sender or
    # emailer_password, raise error
    if (info[environment_vars.EMAILER_SENDER] is None or
            info[environment_vars.EMAILER_PASSWORD] is None):
        raise EnvironmentError('The environment credentials do not contain the '
                               'necessary fields need to authenticate. You '
                               'must specify EMAILER_SENDER and '
                               'EMAILER_PASSWORD.')

    credentials = Credentials.from_authorized_user_info(info)
    return credentials


def default_credentials():
    """Gets the default credentials for the current environment.
    Default credentials provides an easy way to obtain credentials to call
    `auto_emailer.Emailer`.

    This function acquires credentials from the environment in the following
    order:

    1. If the environment variable
       `auto_emailer.config.environment_vars.EMAILER_SENDER` is set to the
       path of a valid JSON file, then it is loaded and returned.
    2. If explicit environment variables are set `EMAILER_`, then the
       credentials are loaded and returned.

    Returns:
        auto_emailer.config.credentials.Credentials: The constructed
        credentials.

    Raises:
        EnvironmentError: If no credentials were found, or if the credentials
            found were invalid.
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

    raise EnvironmentError('Could not automatically determine credentials. '
                           'Please set {env} file path or explicitly set '
                           'environment credentials variables and re-run the '
                           'application. For more information, please see '
                           'auto_emailer.config.environment_vars.'
                           .format(env=environment_vars.EMAILER_CREDS)
                           )
