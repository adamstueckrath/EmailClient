Auto Emailer
---
[![Build Status](https://travis-ci.org/adamstueckrath/AutoEmailer.svg?branch=master)](https://travis-ci.org/adamstueckrath/AutoEmailer)

A wrapper library around python's SMTP (Simple Mail Transfer Protocol) library for making emails easier.

Python makes sending email relatively easy via the smtplib module, but this library makes it even _easier_ with  
auto-configuration and email templates.

This repository contains:
1. [Changelog](CHANGELOG.md) for all notable changes to this library.
2. [Docs](https://github.com/AutoEmailer/docs) for detailed information of modules.
5. [Examples](https://github.com/AutoEmailer/examples) of how to use the AutoEmailer library.
5. [Work In Progress](https://github.com/AutoEmailer/issues/new) link to open issues and new features.

## Table of Contents
- [Background](#background)
- [Install](#install)
- [Usage](#usage)
- [Docs](#docs)
- [Maintainers](#maintainers)
- [Contributing](#contributing)
- [License](#license)

## Background
Let's say you’re automating a task that takes a couple of hours to do, and you don’t want to go back to 
your computer every few minutes to check on the program’s status. Instead, you can use Auto Emailer to 
send a friendly email programmatically when it’s done—freeing you to focus on more important things while 
you’re away from your computer.

What if you have a spreadsheet of email addresses and you need to send out an email to each one? Instead of 
manually writing hundreds, or even thousands, of emails, you just write a few lines of code to auto-mate the 
process and you're done.

## Install
PLACEHOLDER

## Usage
If you want to use the emailing features of this library, then you can either explicitly pass arguments to `Credentials` 
to authenticate your SMTP client or you can set the environment variables `EMAILER_SENDER` _AND_ `EMAIL_PASSWORD`. 
In most cases, these two environment variables will be enough, but if authentication is failing then you may 
need to further specify the environment variables `EMAILER_HOST` and `EMAILER_PORT`. 

For more advance configurations, please see the configuration docs [PLACEHOLDER FOR LINK]. Once again, you can avoid 
environment variables and pass the appropriate credentials in inside your code.

## Docs:
PLACEHOLDER

### Email Providers Automatically Configured
Provider | SMTP Server
------------ | -------------
Gmail | smtp.gmail.com
Outlook.com/Hotmail.com | smtp.office365.com
Yahoo Mail | smtp.mail.yahoo.com
 
## Maintainers
[@adamstueckrath](https://github.com/adamstueckrath)

## Contributing
Feel free to dive in! [Open an issue](https://github.com/RichardLitt/AutoEmailer/issues/new) or submit PRs.

AutoEmailer follows the [Contributor Covenant](https://www.contributor-covenant.org/version/1/4/code-of-conduct.html) 
Code of Conduct.

## License
[MIT](LICENSE.txt) © Adam Stueckrath
