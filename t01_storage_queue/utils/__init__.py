import oss2
import logging

from ..settings import ALIBABA_ACCESSKEYID, ALIBABA_ACCESSKEYSECRET, CLOUD_ENDPOINT

logger = logging.getLogger('alibaba')


class StorageUtils:
    def __init__(self, bucket):

        self._auth = oss2.Auth(ALIBABA_ACCESSKEYID, ALIBABA_ACCESSKEYSECRET)
        self._bucket = oss2.Bucket(self._auth, CLOUD_ENDPOINT, bucket)

    def upload(self, key, data):
        logger.info(f'UPLOADING {key}')
        return self._bucket.put_object(key, data)

    def download(self, key):
        logger.info(f'DOWNLOADING {key}')
        return self._bucket.get_object(key).read()
