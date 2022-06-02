# - Report spams and purge e-mails -

This small tool is designed to connect to an e-mail account using IMAP.
Then it iterates over all emails in a specified folder, and report them to a spam service and finally delete them.
So you have been warned : every mail in 'EMAIL_FOLDER' will be sent to another service then deleted.

# Requirements:
  - python3
  - -to be defined -


# Usage:
 - install dependencies : pip3 install -r requirements.txt
 - add environement variables (see, edit and run setenv.sh)
 - run : python email_purge.py
