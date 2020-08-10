import email
import smtplib
from email.mime.text import MIMEText
from config.config import cfg
from spamcop import spamcop_http


def process_mailbox(M):
    """
    Find all mail in the specified mailbox, send them
    to spamcop, then delete the email.
    """

    # find all msgs in this folder
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print("No messages found!")
        return

    # connect smtp
    smtp_server = None
    try:
        print("  > connecting to SMTP!")
        smtp_server = smtplib.SMTP_SSL(cfg['EMAIL_SVC_SMTP'])
        smtp_server.ehlo()  # optional
    except Exception as e:
        print('Could not connect to', smtphost, e.__class__, e)
        exit(2)

    smtp_server.login(cfg['EMAIL_ACCOUNT'], cfg['EMAIL_PASSWD'])

    # for every mail found
    for mail_id in data[0].split():
        # get this mail
        rv, data = M.fetch(mail_id, '(RFC822)')
        if rv != 'OK':
            print("ERROR getting message", mail_id)
            return

        # get mail content & send to spamcop!
        mail_content = data[0][1].decode("utf-8")

        # display some infos to stdout
        msg = email.message_from_string(mail_content)
        subject = email.header.decode_header(msg['Subject'])[0][0]
        num = int(mail_id)
        print('    [*] msg %02d: %s' % (num, subject))

        # send to spamcop
        spamcop_http.send_to_spamcop(smtp_server, mail_content, subject)

        # remove mail
        M.store(mail_id, '+FLAGS', '\\Deleted')
    smtp_server.quit();
