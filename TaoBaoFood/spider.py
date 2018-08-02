import re

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from pyquery import PyQuery as pq
from TaoBaoFood.config import *
import pymongo

client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# options = webdriver.ChromeOptions()
# options.add_argument('headless')
# browser = webdriver.Chrome(chrome_options=options)
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 10)


def search():
    try:
        browser.get('https://www.taobao.com')
        input_search = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )
        input_search.send_keys('美食')
        submit.click()
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )
        get_products()
        return total.text
    except TimeoutException:
        return search()


def next_page(page_number):
    print('正在翻页...', page_number)
    try:
        input_page = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input'))
        )
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit'))
        )
        input_page.clear()
        input_page.send_keys(page_number)
        submit.click()

        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number))
        )
        get_products()
    except TimeoutException:
        next_page(page_number)


def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item')))
    html = browser.page_source
    doc = pq(html)
    items = doc('#mainsrp-itemlist .items .item').items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        save_to_mongo(product)


def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert(result):
            print('存储到MONGODB成功', result)
    except Exception:
        print("存储到MONGODB错误", result)


def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))
        print(total)
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print("浏览器关闭出错")
    finally:
        browser.close()


if __name__ == '__main__':
    main()
