#!/usr/bin/env python3
#
# This small tool is designed to connect to an e-mail account using IMAP.
# Then it iterates over all emails in a specified folder,
# report them to a spam service and finally delete them.
#

import sys
import imaplib
import email
import datetime
from mailing import mailing
from config.config import cfg
from config.config import check_runtime_cfg
from spamcop import spamcop_http


## check runtime configuration
check_runtime_cfg()

## connect to IMAP with SSL
M = imaplib.IMAP4_SSL(cfg['EMAIL_SVC_IMAP'])

try:
    rv, data = M.login(cfg['EMAIL_ACCOUNT'], cfg['EMAIL_PASSWD'])
except imaplib.IMAP4.error:
    print("LOGIN FAILED!!! ", data)
    exit(1)

## change folder
rv, data = M.select(cfg['EMAIL_FOLDER'])
if rv == 'OK':
    print("> Opening mailbox...")
    ## do some stuff
    mailing.process_mailbox(M)
    print("> Done.")
    M.close()
else:
    print("ERROR: Unable to open mailbox ", rv)

## exit
M.logout()
