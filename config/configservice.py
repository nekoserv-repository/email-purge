import os


class ConfigService:
    __cfg = None

    @staticmethod
    def get(value):
        """init configuration if needed, then return item from __cfg"""
        # reload
        ConfigService.__load_env()
        # get config
        return ConfigService.__cfg[value]

    @staticmethod
    def __load_env():
        """get all env. variables and check configuration"""
        ConfigService.__cfg = {'EMAIL_SVC_IMAP': os.getenv('EMAIL_SVC_IMAP'),
                               'EMAIL_SVC_SMTP': os.getenv('EMAIL_SVC_SMTP'),
                               'EMAIL_ACCOUNT': os.getenv('EMAIL_ACCOUNT'),
                               'EMAIL_PASSWD': os.getenv('EMAIL_PASSWD'),
                               'EMAIL_FOLDER': os.getenv('EMAIL_FOLDER'),
                               'SPAM_URL': os.getenv('SPAM_URL'),
                               'SPAM_LOGIN_PASSWD': os.getenv('SPAM_LOGIN_PASSWD')}

        return ConfigService.__check()

    @staticmethod
    def __check():
        is_valid = True
        # check all environment variables
        for k, v in ConfigService.__cfg.items():
            # display which environment variable is not set
            if v is None:
                print('runtime parameter "%s" is not set' % k)
                is_valid = False
        # exit if not valid
        if not is_valid:
            exit(1)
        return is_valid
