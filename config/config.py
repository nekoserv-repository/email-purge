import base64
import os

# init dict.
cfg = {}

## get env. variables for email server
cfg['EMAIL_SVC_IMAP'] = os.getenv('EMAIL_SVC_IMAP')
cfg['EMAIL_SVC_SMTP'] = os.getenv('EMAIL_SVC_SMTP')
cfg['EMAIL_ACCOUNT'] = os.getenv('EMAIL_ACCOUNT')
cfg['EMAIL_PASSWD'] = os.getenv('EMAIL_PASSWD')
cfg['EMAIL_FOLDER'] = os.getenv('EMAIL_FOLDER')

## get env. variables for spam service
cfg['SPAM_URL'] = os.getenv('SPAM_URL')
cfg['SPAM_LOGIN_PASSWD'] = os.getenv('SPAM_LOGIN_PASSWD')

## check if every parameter is set
def check_runtime_cfg():
    is_valid = True
    # check every config parameters
    for k, v in cfg.items():
        # display which parameter is not set
        if v == None:
            print ('runtime parameter "%s" is not set' % k)
            is_valid = False
    # if at least one parameter is not set, exit
    if is_valid == False:
        exit(1)
