import json
from datetime import datetime

from .utils import StorageUtils, MessageQueueUtils
from .settings import BUCKET_NAME, PATH_TEST01, QUEUE_TEST01


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
