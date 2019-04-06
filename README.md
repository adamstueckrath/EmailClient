Email Client
---
Checking and replying to email is a huge time sink. Of course, you can’t just write a program to handle all your email for you, since each message requires its own response. But you can still automate plenty of email-related tasks.

The main utility of this program is to send emails you’re away from your computer. If you’re automating a task that takes a couple of hours to do, you don’t want to go back to your computer every few minutes to check on the program’s status. Instead, the program can just send you a friendly email when it’s done—freeing you to focus on more important things while you’re away from your computer.

## Email Setup
If you want to use the emailing features of this script, then you can either pass in the parameters to sign into an email account inside the code, or you can set the environment variables "EMAIL_ADDRESS" AND "EMAIL_PASSWORD". In most cases, these two environment variables will be enough, but if authentication is failing then you may need to further create. 

For more advance configurations, set up "EMAIL_PORT" and "EMAIL_HOST". Once again, though, you can avoid environment variables and pass the appropriate values in inside the code.

### Email Service Providers Configured
* Outlook/Hotmail
* Gmail 
* Yahoo

## Email Example
```
# very handy email object that by default will sign into EMAIL_ADDRESS
email = Email()
email.send_mail(['test.destination@gmail.com'], 'Subject', 'Message')
```

