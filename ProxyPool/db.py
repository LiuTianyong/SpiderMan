import redis
from ProxyPool.conf import *


class Redis(object):
    """
    操作 redis 数据库
    """

    def __init__(self, name, host, port):
        self._name = name
        self._conn = redis.Redis(host=host, port=port, db=0)

    def lpop(self):
        """
        左边弹出proxy
        :return:
        """
        proxy = self._conn.lpop(self._name)
        if proxy:
            return proxy.decode("utf8")

    def rpush(self, proxy):
        """
        右边入队proxy
        :return:
        """
        return self._conn.rpush(self._name, proxy)

    def rpush_many(self, proxies):
        """
        右边入队多个
        :param proxies:
        :return:
        """
        return self._conn.rpush(self._name, *proxies)

    def get(self):
        """
        从数据库右边返回一个最新的proxy
        :return:
        """
        proxy = self._conn.rpop(self._name)
        if proxy:
            return proxy.decode("utf8")


db_client = Redis(NAME, HOST, PORT)

if __name__ == '__main__':
    print(db_client.rpush_many(['11', '22']))
    print(db_client.lpop().decode("utf8"))
