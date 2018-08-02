import requests
import re
from ProxyPool.conf import *
from bs4 import BeautifulSoup

session = requests.session()
session.headers = HEADERS


def get_page(url):
    try:
        response = session.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            return soup
    except Exception as e:
        print('请求{}出错{}'.format(url, e))

    return None
