"""Environment variables used by :mod:`auto_emailer.config`"""

EMAILER_CREDS = 'EMAILER_CREDS'
"""Environment variable defining location of auto-emailer 
file path of credentials.

This used by :func:`auto_emailer.config.default_credentials` to 
explicitly set a file path of credentials json file.
"""

EMAILER_SENDER = 'EMAILER_SENDER'
"""Environment variable providing the value of auto-emailer's config 
attribute `EMAILER_SENDER`.
"""

EMAILER_PASSWORD = 'EMAILER_PASSWORD'
"""Environment variable providing the value of auto-emailer's config 
attribute `EMAILER_PASSWORD`.
"""

EMAILER_HOST = 'EMAILER_HOST'
"""Environment variable providing the value of auto-emailer's config 
attribute `EMAILER_HOST`.
"""

EMAILER_PORT = 'EMAILER_PORT'
"""Environment variable providing the value of auto-emailer's config 
attribute `EMAILER_PORT`.
"""
