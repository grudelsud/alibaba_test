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

ALI_ACCESSKEYID = os.getenv('ALI_ACCESSKEYID')
ALI_ACCESSKEYSECRET = os.getenv('ALI_ACCESSKEYSECRET')
ALI_ACCOUNTID = os.getenv('ALI_ACCOUNTID')

BUCKET_NAME = 'droparea'
OSS_ENDPOINT = 'https://oss-cn-beijing.aliyuncs.com'

MNS_ENDPOINT = f'https://{ALI_ACCOUNTID}.mns.cn-beijing.aliyuncs.com/'

PATH_TEST01 = 'test01/messages'
QUEUE_TEST01 = os.getenv('QUEUE_TEST01', 'test01')
