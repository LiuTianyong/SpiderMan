# 爬取网站的ip,制作ip代理池
# 获取器
import time

from ProxyPool.utils import get_page


class SpiderMan(type):
    spiders = []

    def __new__(cls, *args, **kwargs):
        """
        子类构造方法
        :param args: args[0]=name, args[1]=bases,args[2]=attrs
        :param kwargs: None
        :return: 子类
        """

        # 爬虫类必须拥有crawl函数
        if 'crawl' not in args[2]:
            raise Exception

        SpiderMan.spiders.append(type.__new__(cls, *args, **kwargs))
        return type.__new__(cls, *args, **kwargs)


class CrawlKuaiDaiLi(metaclass=SpiderMan):

    @staticmethod
    def crawl(page=3):
        crawl_url = 'https://www.kuaidaili.com/free/inha/{}/'
        proxies = list()
        for i in range(1, page):
            soup = get_page(crawl_url.format(i))
            if soup:
                trs = soup.find('table',
                                {'class': 'table table-bordered table-striped'}).find('tbody')
                for tr in trs.find_all('tr'):
                    tmp = tr.find_all('td')
                    proxy = ':'.join([tmp[0].get_text(), tmp[1].get_text()])
                    print('crawl proxy...', proxy)
                    proxies.append(proxy)
            time.sleep(1)
        return proxies

