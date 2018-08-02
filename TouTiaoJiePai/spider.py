import json
import os
import re
from _md5 import md5
from multiprocessing import Pool
from urllib.parse import urlencode

import pymongo
from bs4 import BeautifulSoup
from requests.exceptions import RequestException
import requests
from TouTiaoJiePai.config import *

client = pymongo.MongoClient(MONGO_URL, connect=False)
db = client[MONGO_DB]

headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/68.0.3440.75 '
                  'Chrome/68.0.3440.75 Safari/537.36'
}

requests_ = requests.session()
requests_.headers = headers


def get_page_index(offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = "https://www.toutiao.com/search_content/?" + urlencode(data)
    try:
        response = requests_.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求索引页出错")
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            if 'article_url' in item.keys():
                yield item.get('article_url')


def get_page_detail(url):
    try:

        response = requests_.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print("请求详情页出错", url)
        return None


def parse_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    # print(title)
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(images_pattern, html)
    if result:
        data = json.loads(result.group(1).replace('\\', ''))
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                download_image(image)
            return {
                'title': title,
                'images': images,
                'url': url
            }


def save_to_mongo(result):
    if result is not None and db[MONGO_TABLE].insert(result):
        print('存储到mongoDB成功', result)
        return True
    print(result)
    return False


def download_image(url):
    print("downloading...", url)
    try:
        response = requests_.get(url)
        if response.status_code == 200:
            save_image(response.content)
        return None
    except RequestException:
        print('请求图片出错', url)
        return None


def save_image(content):
    file_path = '{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()


def main(offset):
    html = get_page_index(offset, KEYWORD)
    # print(html)
    for url in parse_page_index(html):
        html = get_page_detail(url)
        if html:
            result = parse_page_detail(html, url)
            if result:
                save_to_mongo(result)


if __name__ == '__main__':
    groups = [x * 20 for x in range(GROUP_START, GROUP_END)]
    pool = Pool()
    pool.map(main, groups)