Auto Emailer
---
A wrapper around python's SMTP (Simple Mail Transfer Protocol) library for making email automation easier.

The main utility of this program is to automate sending emails from a python script, spreadsheets, or  
for when you’re away from your computer and you want to send an alert on a certain condition. 

Here's an example, let's say you’re automating a task that takes a couple of hours to do, you don’t want to go back to 
your computer every few minutes to check on the program’s status. Instead, you can use Auto Emailer to send a friendly 
email when it’s done—freeing you to focus on more important things while you’re away from your computer.

## Setup
If you want to use the emailing features of this package, then you can either pass in the parameters to sign into an 
email account inside the code, or you can set the environment variables "EMAIL_ADDRESS" AND "EMAIL_PASSWORD". In most 
cases, these two environment variables will be enough, but if authentication is failing then you may need to further 
create. 

For more advance configurations, set up "EMAIL_PORT" and "EMAIL_HOST". Once again, though, you can avoid environment 
variables and pass the appropriate values in inside the code.

docs:
how to use:
https://www.tutorialspoint.com/python/python_sending_email
https://www.afternerd.com/blog/how-to-send-an-email-using-python-and-smtplib/

how to setup configurations:
https://googleapis.dev/python/google-api-core/latest/auth.html

### Email Providers Automatically Configured
Provider | SMTP Server
------------ | -------------
Gmail | smtp.gmail.com
Outlook.com/Hotmail.com | smtp.office365.com
Yahoo Mail | smtp.mail.yahoo.com

## Auto Emailer Example
You can programmatically send an email with a dynamic body to each one of them. So instead of manually writing 
thousands of emails, you just write a few lines of code and you’re good to go.
The main use of this package is to integrate into your environment. 

