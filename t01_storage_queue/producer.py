import json
from datetime import datetime

from .utils import StorageUtils
from .settings import BUCKET_NAME, PATH_TEST01


def produce():
    su = StorageUtils(BUCKET_NAME)
    for i in range(1, 10):
        path = f'{PATH_TEST01}/f{i:03d}.json'
        data = {
            'message': f'file {path}',
            'created': datetime.now().isoformat(),
        }
        su.upload(path, json.dumps(data, indent=2))
