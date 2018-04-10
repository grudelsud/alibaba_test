import os
import logging.config

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'alibaba': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },
}

logging.config.dictConfig(LOGGING)

CLOUD_ENDPOINT = 'https://oss-cn-beijing.aliyuncs.com'

BUCKET_NAME = 'droparea'

ALIBABA_ACCESSKEYID = os.getenv('ALIBABA_ACCESSKEYID')
ALIBABA_ACCESSKEYSECRET = os.getenv('ALIBABA_ACCESSKEYSECRET')

PATH_TEST01 = 'test01/messages'
