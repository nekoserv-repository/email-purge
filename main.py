#!/usr/bin/env python3
#
# This app is designed to connect to an e-mail account using IMAP4.
# Then it iterates over all emails in a specified folder,
# send them to SpamCop and finally delete them.
#


from processors.runner import Runner

# run!
app = Runner()
app.mail_loop()
