#!/usr/bin/env python3
#
# This app is designed to connect to an e-mail account using IMAP.
# Then it iterates over all emails in a specified folder,
# send them to spamcop.net and finally delete them.
#

import imaplib
from time import sleep
import signal
from mailing import mailing
from config.config import cfg
from config.config import check_runtime_cfg
from spamcop import spamcop_http


class Email_Purge:
    mailbox = None

    def __init__(self):
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())
        signal.signal(signal.SIGTERM, lambda signal, frame: self._signal_handler())
        self.terminated = False

    def _signal_handler(self):
        if self.mailbox != None and self.mailbox.socket().fileno() != -1:
            self.mailbox.close()
            self.mailbox.logout()
        print('! caugth exit signal - farewell')
        exit(0)

    def mail_loop(self):
        while True:
            try:
                ## connect to IMAP with SSL
                self.mailbox = imaplib.IMAP4_SSL(cfg['EMAIL_SVC_IMAP'])
                rv, data = self.mailbox.login(cfg['EMAIL_ACCOUNT'], cfg['EMAIL_PASSWD'])
            except imaplib.IMAP4.error:
                print("LOGIN FAILED!!! ", data)
                exit(1)

            ## change folder
            rv, data = self.mailbox.select(cfg['EMAIL_FOLDER'])
            if rv == 'OK':
                print("> Opening mailbox...")
                ## do some stuff
                mailing.process_mailbox(self.mailbox)
                print("> Done.")
            else:
                print("ERROR: Unable to open mailbox ", rv)

            ## exit mailbox
            self.mailbox.close()
            self.mailbox.logout()

            ## sleep for 10 mins
            print("~ waiting 10 mins")
            sleep(600)


## check runtime configuration
check_runtime_cfg()

# run!
app = Email_Purge()
app.mail_loop()
