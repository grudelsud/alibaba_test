import logging
import json
import sys
from datetime import datetime

from .utils import StorageUtils, MessageQueueUtils
from .settings import BUCKET_NAME, PATH_TEST01, QUEUE_TEST01

logger = logging.getLogger('alibaba')


def create_queue():
    mqu = MessageQueueUtils()
    mqu.create_queue(QUEUE_TEST01)


def upload_notify():
    su = StorageUtils(BUCKET_NAME)
    mqu = MessageQueueUtils()

    for i in range(1, 10):
        path = f'{PATH_TEST01}/f{i:03d}.json'
        data = {
            'message': f'up/notify file {path}',
            'created': datetime.now().isoformat(),
        }
        su.upload(path, json.dumps(data, indent=2))
        mqu.send_msg(QUEUE_TEST01, path)


def receive_download():
    su = StorageUtils(BUCKET_NAME)
    mqu = MessageQueueUtils()

    while True:
        msg = mqu.recv_msg(QUEUE_TEST01)
        if msg is None:
            print('Nothing else to do, bye.')
            sys.exit(1)
        else:
            print(f"Receive Message Succeed! \
                      \nMessageId: {msg.message_id}\nMessageBodyMD5: {msg.message_body_md5} \
                      \nMessageBody: {msg.message_body}\nDequeueCount: {msg.dequeue_count} \
                      \nEnqueueTime: {msg.enqueue_time}\nFirstDequeueTime: {msg.first_dequeue_time} \
                      \nPriority: {msg.priority}\nNextVisibleTime: {msg.next_visible_time} \
                      \nReceiptHandle: {msg.receipt_handle}\n\n")
            out = json.loads(su.download(msg.message_body))
            print(f'received: {out}')


def upload_download():
    su = StorageUtils(BUCKET_NAME)

    for i in range(1, 10):
        path = f'{PATH_TEST01}/f{i:03d}.json'
        data = {
            'message': f'up/down file {path}',
            'created': datetime.now().isoformat(),
        }
        su.upload(path, json.dumps(data, indent=2))
        out = json.loads(su.download(path))
        print(f'received: {out}')


def longpoll():
    mqu = MessageQueueUtils()
    wait_seconds = 10

    while True:
        msg = mqu.recv_msg(QUEUE_TEST01, wait_seconds=wait_seconds)
        if msg is not None:
            logger.info(f"Receive Message Succeed! \
                \nMessageId: {msg.message_id}\nMessageBodyMD5: {msg.message_body_md5} \
                \nMessageBody: {msg.message_body}\nDequeueCount: {msg.dequeue_count} \
                \nEnqueueTime: {msg.enqueue_time}\nFirstDequeueTime: {msg.first_dequeue_time} \
                \nPriority: {msg.priority}\nNextVisibleTime: {msg.next_visible_time} \
                \nReceiptHandle: {msg.receipt_handle}\n\n")
        else:
            logger.info(f'waiting another {wait_seconds}s')

    logger.info('::: how did we get here? :::')
