from email import message_from_string
from email.header import decode_header

from spamcop import spamcop_http
from tools.convertors import to_utf8


def process_mailbox(mailbox):
    """
    Find all mails in the specified mailbox, send them
    to SpamCop, then delete the email.
    """

    # find all mails in this folder
    rv, data = mailbox.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    if data[0] == b'':
        print('  > Nothing to do for now')
        return

    # for every mail found
    for mail_id in data[0].split():
        # get this mail
        rv, data = mailbox.fetch(mail_id, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", mail_id)
            return

        # get mail content & send to SpamCop!
        mail_content = to_utf8(data[0][1])

        # display details to stdout
        msg = message_from_string(mail_content)
        subject = decode_header(msg['Subject'])[0][0]
        num = int(mail_id)
        print('    [*] msg %02d: %s' % (num, subject))

        # send to SpamCop
        spamcop_http.send_to_spamcop(mail_content)

        # remove mail
        mailbox.store(mail_id, '+FLAGS', '\\Deleted')
