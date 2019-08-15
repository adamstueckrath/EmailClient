User Guide
==========

Python comes with the built-in smtplib module for sending emails using the
Simple Mail Transfer Protocol (SMTP). smtplib uses the RFC 2821 protocol for
SMTP. The email package is a library for managing email messages. It is
specifically not designed to do any sending of email messages to SMTP
(RFC 2821), NNTP, or other servers; those are functions of modules such as
smtplib.

The auto-emailer library provides a nice, easy to use, wrapper around the
two libraries.


Credentials
-----------

:class:`~auto_emailer.config.credentials.Credentials` are the means of
identifying a user to a authenticate a SMTP client and host. Auto credentials
can be obtained in two different ways with the class ``emailer.Emailer``:
*environment credentials* and *environment credentials file*. Another way to
authenticate is to manually pass configurations to the ``Credentials`` class and
then initiate emailer with those credentials.

With the Credentials class, you do not need to set the port or host, though it
is HIGHLY recommended that you do. The Credentials class will set the port to a
default value of 587 if is not set and will attempt to guess the host from the
sender email address if host is not set.

SMTP clients in which ``EMAILER_HOST`` and ``EMAILER_PORT`` will
be auto configured. This means you only need to specify ``EMAILER_SENDER`` and
``EMAILER_PASSWORD``.

==================   ====================
Provider             SMTP Server
==================   ====================
Gmail                smtp.gmail.com
Outlook/Hotmail	     smtp.office365.com
Yahoo Mail           smtp.mail.yahoo.com
==================   ====================

Auto Credentials
----------------

If you instantiate the emailer class with default configuration settings, it
will perform the following credential configuration checks:

1. If the environment variable ``EMAILER_CREDS`` is set to the path of a valid
JSON file, then the credentials are loaded and returned.

2. If explicit environment variables are set (they start with ``EMAILER_``), then
the environment variables are loaded and returned.

Initiating the ``emailer.Emailer`` will automatically determine the
credentials from the environment if config argument is None.::

    from auto_emailer import Emailer

    # auto-configuration of credentials
    my_emailer = Emailer(config=None, delay_login=False)
    print(my_emailer.connected)

Environment Credentials File
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The auto-emailer library will first look for the environment variable
``EMAILER_CREDS`` to create a Credentials instance from an authorized user json
file. Set the ``EMAILER_CREDS`` environment variable to the full path to your
credential file::

    EMAILER_CREDS='/path/to/creds.json'

The json file needs to be in the specified format (order does not matter)::

    {
      "EMAILER_SENDER": "test@gmail.com",
      "EMAILER_PASSWORD": "mypassword",
      "EMAILER_HOST": "smtp.gmail.com",
      "EMAILER_PORT": 587
    }

Environment Credentials Variables
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The auto-emailer library will then look for these environment variables:

``EMAILER_SENDER``
    Environment variable providing the value of auto-emailer's config
    attribute `EMAILER_SENDER`.

``EMAILER_PASSWORD``
    Environment variable providing the value of auto-emailer's config
    attribute `EMAILER_PASSWORD`.

``EMAILER_HOST``
    Environment variable providing the value of auto-emailer's config
    attribute `EMAILER_HOST`.

``EMAILER_PORT``
    Environment variable providing the value of auto-emailer's config
    attribute `EMAILER_PORT`.

If it cannot find any credentials from environment file or explicit environment
variables, then an error message will display asking you to either create your
own configuration, or if you use auto configuration, then specify either
credential file or explicit environment variables.

.. warning:: Credential files must be kept secret. If you expose your secret file
    it is recommended that you change your credentials from the email host you
    are using.

Manual Credentials
------------------
You manually configure your credentials but why would you do that since the
hard work is already done for you with environment variables :) However, if
you would like to it is recommended that you initiate ``Credentials`` from the
class methods. Here is how you can with a file or python dictionary.

Use :meth:`~auto_emailer.config.credentials.Credentials.from_authorized_user_file`::

    from auto_emailer import Emailer
    from auto_emailer.config import Credentials

    # path to creds file
    creds_path = '/path/to/creds.json'

    # explicitly initiate credentials
    email_creds = Credentials.from_authorized_user_file(creds_path)

    # pass credential instance to Emailer
    my_emailer = Emailer(config=email_creds, delay_login=False)
    print(my_emailer.connected)

Use :meth:`~auto_emailer.config.credentials.Credentials.from_authorized_user_info`::

    import pickle
    from auto_emailer import Emailer
    from auto_emailer.config import Credentials

    # load creds from pickle file
    # must be type: dict
    with open('creds_file.pickle', 'rb') as creds:
        creds_dict = pickle.load(creds)

    # explicitly initiate credentials
    email_creds = Credentials.from_authorized_user_info(creds_dict)

    # pass credential instance to Emailer
    my_emailer = Emailer(config=email_creds, delay_login=False)
    print(my_emailer.connected)

Emailer
-------

:class:`~auto_emailer.emailer.Emailer` is the interface to the SMTP client. To
send an email using auto-emailer, all you need to do is call the ``send_email``
function. If you're send an email with the ``auto_emailer.emailer.Message``,
the to_addrs and from_addr arguments are optional. However, if you are sending
a string email message, then you need to pass the arguments. Otherwise an error
will raise if one or both are missing. At the moment, auto-emailer uses TLS
encryption but there will be support for SSL encryption in future versions.

Sending Emails
--------------

Sending emails with the auto-emailer library is very easy. Once you have your
email account setup and credentials configured, all you need to do is this::

    from auto_emailer import Emailer, Message

    # create emailer instance
    my_emailer = Emailer()

    # send email!
    my_emailer.send_email('Hello, how are you doing today?',
                          'my_email@gmail.com',
                          ['my_friend_email@gmail.com'])


Or you can send an email with a Message object, like this::

    # create a message object instance
    my_email = Message('my_email@gmail.com',
                       ['my_friend@gmail.com'],
                       'Hello Friend!')
    # draft a message
    my_email = my_email.draft_message(text="Hi! Let's hang out 😁")

    # send email message to friend!
    mailer.send_email(my_email)

Notice that you do not need to pass in the arguments ``to_addrs`` and
``from_addr`` because they are optional if you send a Message object.

Message
-------

:class:`~auto_emailer.emailer.Message` is the wrapper for building email
messages to send with ``Emailer``. A Message object has headers and payloads.
Headers and the body are the two main parts of an email. When you call the
Message class, a message object is created automatically. However, it does not
populate the message until you call the method ``draft_message``. The
method return the message object with headers and text.

The Message class handles the object representation of an email; it does not
actually have the functionality to send emails (that functionality is in the
Emailer module).

Message from Templates
^^^^^^^^^^^^^^^^^^^^^^

To use the Message template functionality, you'll need to create a text file.::

    '/path/to/email_template.txt'

An example text file could look like this::

    Hi,

    How are you doing today?

    Sincerely,
    Your friend

After creating a text file template, pass the file path as an argument to the
:meth:`~auto_emailer.emailer.Message.draft_message` function. The function will
open the template text file, read the text and add it as the body of the
Message::

    from auto_emailer import Emailer, Message

    # create emailer instance
    my_emailer = Emailer()

    # email template file path
    my_template = '/path/to/email_template.txt'

    # create a message
    my_email = Message('my_email@test.com',
                       ['my_friend@gmail.com'],
                       'My Subject!')

    # draft email message with template
    my_email.draft_message(template_path=my_template)

    # send email with template!
    my_emailer.send_email(my_email)



Message from Templates with Dynamic Arguments
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Using the example above, what if you wanted to have the template dynamically
change depending on the destination of the email? For example, you can create a
text file with ``{test_var}`` variables and change the variable values on some
event

Create a text file with variables::

    Hi {name},

    How are you doing today?

    Sincerely,
    Your friend

After creating a text file template with keyword variables, pass the file path as
an argument to the :meth:`~auto_emailer.emailer.Message.draft_message` function
as well as the variable keyword values. The `draft_message` function will open
the template text file, read the text, insert the variables values, and attach
the text as the body of the email::

    from auto_emailer import Emailer, Message

    # create emailer instance
    my_emailer = Emailer()

    # email template file path
    my_template = '/path/to/email_template.txt'

    # create a message
    my_email = Message('my_email@test.com',
                       ['my_friend@gmail.com'],
                       'My Subject!')

    # draft email message with template
    my_email.draft_message(template_path=my_template,
                           template_args=dict(name="joe")

    # send email with template arguments!
    my_emailer.send_email(my_email)

As you might have noticed, you don't need to pass in the ``text`` argument,
since the body of the email is populated by the template text.

Message with Attachments
^^^^^^^^^^^^^^^^^^^^^^^^

In order to send binary files to an email server that is designed to work with
textual data, they need to be encoded before transport. This is most commonly
done using base64, which encodes binary data into printable ASCII characters.
All of this is done in the ``attach`` method. At the moment text, json, csv,
and other file formats are supported as attachments. As well as .png and .jpeg
image formats. In future versions, the auto-emailer will have the ability to
attach audio files.::

   from auto_emailer import Emailer, Message

    # create emailer instance
    my_emailer = Emailer()

    # email template file path
    files = ['/path/to/attachment_1.csv',
             '/path/to/attachment_2.png']

    # create a message
    my_email = Message('my_email@test.com',
                       ['my_friend@gmail.com'],
                       'Hello Friend!')

    # draft email message
    my_email.draft_message(text="Please see attached.")

    # add attachments to message
    my_email.attach(attach_files=files)

    # send email with attachments!
    my_emailer.send_email(my_email)

Please note that each SMTP client has a limit on email size. If you are having
trouble sending attachments, check your specific client's allowed email size.













