import os
import sys
import argparse
from datetime import datetime

from mns.account import Account
from mns.queue import QueueMeta, Message, MNSExceptionBase

ALI_ACCESSKEYID = os.getenv('ALI_ACCESSKEYID')
ALI_ACCESSKEYSECRET = os.getenv('ALI_ACCESSKEYSECRET')
ALI_ACCOUNTID = os.getenv('ALI_ACCOUNTID')

MNS_ENDPOINT = 'https://{}.mns.cn-beijing.aliyuncs.com/'.format(ALI_ACCOUNTID)
QUEUE_NAME = 'test01p2'


def get_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--produce',
        action='store_true',
        help='create files, upload them to storage and notify the queue')
    group.add_argument(
        '--consume',
        action='store_true',
        help='read messages from queues, download files specified in msg body')
    return parser


def run_produce():
    account = Account(MNS_ENDPOINT, ALI_ACCESSKEYID, ALI_ACCESSKEYSECRET)
    q = account.get_queue(QUEUE_NAME)

    queue_meta = QueueMeta()
    queue_meta.set_visibilitytimeout(100)
    queue_meta.set_maximum_message_size(10240)
    queue_meta.set_message_retention_period(3600)
    queue_meta.set_delay_seconds(10)
    queue_meta.set_polling_wait_seconds(20)
    queue_meta.set_logging_enabled(True)

    try:
        q_url = q.create(queue_meta)
        sys.stdout.write("Create Queue Succeed!\nQueueURL:%s\n\n" % q_url)
    except MNSExceptionBase as e:
        sys.stderr.write("Create Queue Fail!\nException:%s\n\n" % e)
        sys.exit(1)

    for i in range(1, 10):
        msg_body = "Test Message n. {} at {}".format(i, datetime.now().isoformat())
        message = Message(msg_body)
        message.set_delayseconds(0)
        message.set_priority(10)
        try:
            send_msg = q.send_message(message)
            sys.stdout.write("Send Message Succeed.\nMessageBody:%s\nMessageId:%s\nMessageBodyMd5:%s\n\n" % (msg_body, send_msg.message_id, send_msg.message_body_md5))
        except MNSExceptionBase as e:
            sys.stderr.write("Send Message Fail!\nException:%s\n\n" % e)
            sys.exit(1)


def run_consume():
    account = Account(MNS_ENDPOINT, ALI_ACCESSKEYID, ALI_ACCESSKEYSECRET)
    q = account.get_queue(QUEUE_NAME)

    while True:
        try:
            wait_seconds = 10
            recv_msg = q.receive_message(wait_seconds)
            sys.stdout.write("Receive Message Succeed! \
                            \nMessageId: %s\nMessageBodyMD5: %s \
                            \nMessageBody: %s\nDequeueCount: %s \
                            \nEnqueueTime: %s\nFirstDequeueTime: %s \
                            \nPriority: %s\nNextVisibleTime: %s \
                            \nReceiptHandle: %s\n\n" %
                            (recv_msg.message_id, recv_msg.message_body_md5,
                            recv_msg.message_body, recv_msg.dequeue_count,
                            recv_msg.enqueue_time, recv_msg.first_dequeue_time,
                            recv_msg.priority, recv_msg.next_visible_time,
                            recv_msg.receipt_handle))

            q.delete_message(recv_msg.receipt_handle)
            sys.stdout.write("Delete Message Succeed.\n\n")

        except MNSExceptionBase as e:
            sys.stderr.write("Receive Message Fail!\nException:%s\n\n" % e)
            break

    try:
        q.delete()
        sys.stdout.write("Delete Queue Succeed!\n\n")
    except MNSExceptionBase as e:
        sys.stderr.write("Delete Queue Fail!\nException:%s\n\n" % e)
        sys.exit(1)


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.produce:
        run_produce()
    elif args.consume:
        run_consume()
    else:
        parser.print_help()
