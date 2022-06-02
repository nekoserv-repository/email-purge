import signal
from imaplib import IMAP4_SSL
from time import sleep

from config.configservice import ConfigService
from processors.mailbox import process_mailbox


class Runner:
    mailbox = None

    def __init__(self):
        signal.signal(signal.SIGINT, lambda signal, frame: self._signal_handler())
        signal.signal(signal.SIGTERM, lambda signal, frame: self._signal_handler())

    def _signal_handler(self):
        if self.mailbox is not None and self.mailbox.socket().fileno() != -1:
            self.mailbox.close()
            self.mailbox.logout()
        print('! caught exit signal - farewell')
        exit(0)

    def mail_loop(self):
        while True:
            self._call_imap_server()

    def _call_imap_server(self):
        try:
            # connect to IMAP with SSL
            self.mailbox = IMAP4_SSL(ConfigService.get('EMAIL_SVC_IMAP'))
            self.mailbox.login(ConfigService.get('EMAIL_ACCOUNT'), ConfigService.get('EMAIL_PASSWD'))
        except Exception as e:
            print("FATAL : login to mailbox failed", e)
            exit(1)

        # change folder
        rv, data = self.mailbox.select(ConfigService.get('EMAIL_FOLDER'))
        if rv == 'OK':
            print("> Opening mailbox...")
            # do some stuff
            process_mailbox(self.mailbox)
            print("> Done.")
        else:
            print("ERROR: Unable to open mailbox", rv)
            self.mailbox.close()
            self.mailbox.logout()
            exit(1)

        # exit mailbox
        self.mailbox.close()
        self.mailbox.logout()

        # sleep for 10 minutes
        print("~ waiting 10 min")
        sleep(600)
