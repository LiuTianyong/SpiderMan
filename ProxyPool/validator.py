import re
import time

import requests
from ProxyPool.db import db_client
from threading import Thread


class Validator(Thread):
    """
    检测右边最久的proxy
    proxy有用入队
    proxy无用抛弃
    """

    def __init__(self, seconds, numbers=10):
        Thread.__init__(self)
        self._db = db_client
        self._num = numbers
        self._s = seconds

    def run(self):
        while True:
            for i in range(self._num):
                proxy = self._db.lpop()
                print('validate proxy...', proxy)
                if proxy_useful_valid(proxy):
                    self._db.rpush(proxy)
            time.sleep(self._s)


def proxy_useful_valid(proxy):
    """
    测试代理是否可用
    :param proxy:
    :return:
    """
    proxies = {"http": "http://{0}".format(proxy)}
    try:
        r = requests.get('http://httpbin.org/ip', proxies=proxies, timeout=10, verify=False)
        if r.status_code == '200':
            return True
    except Exception:
        return False
