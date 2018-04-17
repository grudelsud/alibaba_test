import argparse

from blah.runner import (
    create_queue,
    upload_notify,
    queue_notify,
    receive_download,
    upload_download,
    longpoll)


def get_parser():
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        '--notify',
        action='store_true',
        help='send simple messages to the queue')
    group.add_argument(
        '--longpoll',
        action='store_true',
        help='message queue long polling, just log received messages')
    group.add_argument(
        '--produce',
        action='store_true',
        help='create files, upload them to storage and notify the queue')
    group.add_argument(
        '--consume',
        action='store_true',
        help='read messages from queue, download files specified in msg body by --produce')
    group.add_argument(
        '--updown',
        action='store_true',
        help='simple oss upload & download')
    return parser


def run_up_down():
    upload_download()


def run_notify():
    queue_notify()


def run_produce():
    create_queue()
    upload_notify()


def run_consume():
    receive_download()

def run_longpoll():
    longpoll()


if __name__ == '__main__':
    parser = get_parser()
    args = parser.parse_args()
    if args.produce:
        run_produce()
    elif args.consume:
        run_consume()
    elif args.updown:
        run_up_down()
    elif args.longpoll:
        run_longpoll()
    elif args.notify:
        run_notify()
    else:
        parser.print_help()
