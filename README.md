# - Report spams and purge e-mails -

This small tool is designed to connect to an e-mail account using IMAP.
Then it iterates over all emails in a specified folder, and report them to a spam service and finally delete them.
So you have been warned : every mail in 'EMAIL_FOLDER' will be sent to another service then deleted.

# Requirements:
  - python3
  - requests_html==0.10.0
  - beautifulsoup4==4.11.1


# Usage:
 - install dependencies : pip3 install -r requirements.txt
 - add environement variables (see, edit and run setenv.sh)
 - run : python main.py

# Dev mode:
 - apt install python3-venv : if needed
 - python3 -m venv .
 - source ./bin/activate
 - pip3 install -r requirements.txt
 - python3 main.py
