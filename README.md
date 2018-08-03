# python3爬虫教程



### 爬取猫眼top100电影

简述：

    利用requests和简单的正则表达式进行数据的爬取，并利用multiprocessing.Pool线程池加快速度


### 爬取头条街拍图片

简述：

    利用requests的session特性进行爬取，同时添加headers防止网站反爬，并把数据存储进mongoDB

问题1：

    爬取返回数据`<html><body></body></html>`, 并不是正确的数据

解决:

    利用requests.session(), 添加头信息headers的user-Agent, 替换之前的直接的requests请求

问题2:

    头条图片的js格式出现改变

解决:

    图片正则表达式:

    ```
    images_pattern = re.compile('gallery: JSON.parse\("(.*?)"\),', re.S)
    result = re.search(images_pattern, html)
    data = json.loads(result.group(1).replace('\\', ''))
    ```


### 爬取淘宝美食

简述：

    利用selenium+chrome自动爬取淘宝美食，并利用pyquery分析数据，存入mongodb

改进:

    利用chrome新特性headless进行后台爬取

    ```
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    browser = webdriver.Chrome(chrome_options=options)
    ```


### 代理池

简述：

    ip代理池，防止网站反爬设置代理池

文件：

    api.py:         flask api 对外接口，获取proxy ip

    conf.py:        代理设置文件

    db.py:          redis数据库操作

    getter.py:      获取代理IP

    spider.py:      代理handler设置

    schedule.py:    调度器，调度getter和validator

    utils.py:       工具函数

    validator.py:   验证代理是否可用

