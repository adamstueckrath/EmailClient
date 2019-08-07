"""Environment variables used by :mod:`auto_emailer.config`"""

CREDENTIALS_ENVIR_PATH = 'emailer_credentials'
"""Environment variable defining location of Auto Emailer 
file path of credentials.

This used by :func:`auto_emailer.config.default_credentials` to 
explicitly set a file path of credentials json file.
"""

ENVIR_SENDER = 'emailer_sender'
"""Environment variable providing the value of Auto Emailer's config 
attribute `emailer_sender`.
"""

ENVIR_PASSWORD = 'emailer_password'
"""Environment variable providing the value of Auto Emailer's config 
attribute `emailer_password`.
"""

ENVIR_HOST = 'emailer_host'
"""Environment variable providing the value of Auto Emailer's config 
attribute `emailer_host`.
"""

ENVIR_PORT = 'emailer_port'
"""Environment variable providing the value of Auto Emailer's config 
attribute `emailer_port`.
"""
