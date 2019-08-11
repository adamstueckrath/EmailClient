Quickstart
==========

Setting up an Email
-------------------
Example will use Google account.
Need to reference imgs in _static

Gmail Bandwidth limits for accounts
https://support.google.com/a/answer/1071518?hl=en

Installation
------------

Install the latest auto-emailer release via pip::

    pip install auto-emailer


You may also install a specific version::

    pip install auto-emailer==1.0.0


.. note:: The latest development version can always be found on GitHub_.
.. _GitHub: https://github.com/adamstueckrath/auto-emailer/

Credentials
-----------

To get started either explicitly pass arguments to
`:class:``~auto_emailer.config.crendentials.Credentials`` to authenticate your
SMTP client or you can set the environment variables ``EMAILER_SENDER``
*AND* ``EMAIL_PASSWORD`` for auto configuration. In most cases, these two
environment variables will be enough, but if authentication is failing then you
may need to further specify the environment variables ``EMAILER_HOST`` and
``EMAILER_PORT``.

This library provides no support for obtaining user credentials, but does
provide support for using user credentials. This way you don’t have to worry
about accidentally pushing sensitive credentials to a place such as GitHub and
you can easily and securely authenticate the SMTP client within your code. The
auto-emailer environment variables all start with ``EMAILER_``.

Using auto-emailer
------------------

To use Boto 3, you must first import it and tell it what service you are going to use:



Now that you have an s3 resource, you can make requests and process responses
from the service. The following uses the buckets collection to print out all bucket names:

Resources and Collections will be covered in more detail in the following
sections, so don't worry if you do not completely understand the examples.


Tips and Tricks
---------------

- Reference the email provider (host) for more information on bandwidth limits
  for accounts.
- Reference the email provider (host) for more information on sending limits.
- Do not send too fast.
- Do not send more than 50 emails at once or use ``time.sleep()`` in between
  each email.
- Do not try stupid things or your email provider will punish you.
