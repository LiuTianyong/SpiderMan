import time
from threading import Thread
from ProxyPool.spider import SpiderMan
from ProxyPool.db import db_client


class Getter(Thread):
    def __init__(self, seconds):
        Thread.__init__(self)
        self._s = seconds
        self._db = db_client

    def run(self):
        while True:
            for spider in SpiderMan.spiders:
                proxies = spider.crawl()
                db_client.rpush_many(proxies)

            time.sleep(self._s)
