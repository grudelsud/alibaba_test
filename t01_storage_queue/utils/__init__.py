import logging
import oss2
from mns.account import Account
from mns.queue import QueueMeta, MNSExceptionBase, Message

from ..settings import (
    ALI_ACCESSKEYID,
    ALI_ACCESSKEYSECRET,
    MNS_ENDPOINT,
    OSS_ENDPOINT)

logger = logging.getLogger('alibaba')


class StorageUtils:
    def __init__(self, bucket):

        self._auth = oss2.Auth(ALI_ACCESSKEYID, ALI_ACCESSKEYSECRET)
        self._bucket = oss2.Bucket(self._auth, OSS_ENDPOINT, bucket)

    def upload(self, key, data):
        logger.info(f'UPLOADING {key}')
        return self._bucket.put_object(key, data)

    def download(self, key):
        logger.info(f'DOWNLOADING {key}')
        return self._bucket.get_object(key).read()


class MessageQueueUtils:
    def __init__(self):
        self._account = Account(MNS_ENDPOINT, ALI_ACCESSKEYID, ALI_ACCESSKEYSECRET)

    def create_queue(self, queue_name):
        self._q = self._account.get_queue(queue_name)
        try:
            self._q_url = self._q.create(QueueMeta())
            logger.info(f'q: {queue_name} created at url {self._q_url}')
        except MNSExceptionBase as e:
            if e.type == "QueueAlreadyExist":
                logger.error(f'q: {queue_name} already exists')
            logger.error(f'error creating queue: {e}')

    def send_msg(self, queue_name, msg_body):
        self._q = self._account.get_queue(queue_name)
        try:
            msg = self._q.send_message(Message(msg_body))
            logger.info(f'msg sent: {msg.message_id}, {msg_body}')
        except MNSExceptionBase as e:
            if e.type == "QueueNotExist":
                logger.error(f'q {queue_name} does not exist, you need to create it first')
            logger.error(f'error sending message: {e}')

    def recv_msg(self, queue_name, wait_seconds=3, delete=True):
        self._q = self._account.get_queue(queue_name)
        try:
            msg = self._q.receive_message(wait_seconds)
            logger.info(f'msg received: {msg.receipt_handle}, {msg.message_body}, {msg.message_id}')
        except MNSExceptionBase as e:
            if e.type == "QueueNotExist":
                logger.error(f'q {queue_name} does not exist, you need to create it first')
            elif e.type == "MessageNotExist":
                logger.info(f'q {queue_name} is empty')
            else:
                logger.error(f'cannot receive msg: {e}')
        else:
            if delete:
                try:
                    self._q.delete_message(msg.receipt_handle)
                    logger.info('msg deleted from queue')
                except MNSExceptionBase as e:
                    logger.error(f'could not delete msg: {e}')
            return msg
