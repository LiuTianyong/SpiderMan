from urllib.parse import urlencode
from WeChatArticle.conf import *
import pymongo
from pyquery import PyQuery as pq
import requests

base_url = 'http://weixin.sogou.com/weixin?'
headers = {
    'Cookie': 'CXID=8C47AD7F463AA035B71F0A330FBCBAAB; SUID=02F3261B3865860A5B5692A80000BC03; wuid=AAF1ucuAIQAAAAqGGWyepQgAQAU=; SUV=1532407467173649; SMYUV=1532407467178768; UM_distinctid=164ca9a4db6556-0d44f1cd64b94f-24414032-1fa400-164ca9a4db76b7; ad=Jlllllllll2bqI3olllllVHQLe6lllllphb8lkllllclllllpVxlw@@@@@@@@@@@; IPLOC=CN4403; ABTEST=0|1533206185|v1; weixinIndexVisited=1; JSESSIONID=aaa1dB_trTaEQ8Yu0SHsw; PHPSESSID=vt9j6mfvf9k2ogfao8qqesrv52; SUIR=7F9FB412A5A0D7D7C4AC6F43A68381C5; ppinf=5|1533206422|1534416022|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNTpUb21teSU0MCVFOSVCQiU4NCVFNiVBMiU5MyVFNSU4MSVBNXxjcnQ6MTA6MTUzMzIwNjQyMnxyZWZuaWNrOjM1OlRvbW15JTQwJUU5JUJCJTg0JUU2JUEyJTkzJUU1JTgxJUE1fHVzZXJpZDo0NDpvOXQybHVGWC1FM1Z5ZjVGQk1YMUREUHNpakdNQHdlaXhpbi5zb2h1LmNvbXw; pprdig=fzjjcYRC1-gf4ehmJ7TEZV1MMlZTTv_bmoPF3fg23c_2SLobnOVKppKo21_QoyN-6MPhYkKo9zohgoNdNRBPz1ylBS_TnZaCvhMbQqGVm1hJgmNl050MClRulVuYmE4U6Y1EGT1rp14NSnaPu62huUaxTVqfCCGkqFtAz6zjafI; sgid=26-36377555-AVtia35Yk5GHegRQWaWQ4Ixk; sct=3; SNUID=E005D1EDF7F385880C2BF180F79FAB0D; ppmdig=1533270449000000173c66dad6564f0f0a9161828bd02821',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Ubuntu Chromium/68.0.3440.75 Chrome/68.0.3440.75 Safari/537.36',
    'Connection': 'close',
}
proxy = None

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DB]


def get_proxy():
    try:
        response = requests.get(PROXY_POOL_URL, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling...', url)
    print('Trying Count...', count)
    global proxy
    if count >= MAX_COUNT:
        print('Tried Too many Counts')
        return None
    try:
        if proxy:
            proxies = {'http': 'http://{}'.format(proxy)}
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            return response.text
        if response.status_code == 302:
            # Need Proxy
            proxy = get_proxy()
            if proxy:
                print('Using Proxy...', proxy)
                count += 1
                return get_html(url, count)
            else:
                print('Get Proxy Failed...', proxy)
                return None
    except Exception as e:
        print('Error Occurred', e.args)
        proxy = get_proxy()
        count += 1
        return get_html(url, count)


def get_index(kw, page):
    data = {
        'query': kw,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def parse_index(html):
    doc = pq(html)
    items = doc('.news-box .news-list .list-box h3 a').items()
    for item in items:
        yield item.attr('href')


def get_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def parse_detail(html):
    doc = pq(html)
    title = doc('.rich_media_title').text()
    content = doc('.rich_media_content').text()
    date = doc('#post-date').text()
    nickname = doc('.rich_media_meta_list .rich_media_meta_nickname').text()
    wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()
    return {
        'title': title,
        'content': content,
        'date': date,
        'nickname': nickname,
        'wechat': wechat
    }


def save_to_mongo(data):
    if db['articles'].update({'title': data.get('title')}, {'$set': data}, True):
        print('Saved to Mongo', data['title'])
    else:
        print('Saved to Mongo Failed', data['title'])


def main():
    for i in range(1, 101):
        html = get_index(KEYWORD, i)
        if html:
            article_urls = parse_index(html)
            for article_url in article_urls:
                article_html = get_detail(article_url)
                if article_html:
                    article_data = parse_detail(article_html)
                    if article_data:
                        save_to_mongo(article_data)


if __name__ == '__main__':
    main()
