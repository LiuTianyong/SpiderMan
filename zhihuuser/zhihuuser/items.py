# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class UserItem(Item):
    avatar_url_template = Field()   # https://pic3.zhimg.com/v2-7626555b98634ddfc6e6147588463541_{size}.jpg
    name = Field()                  # Boyka
    headline = Field()              # \u5fae\u535a\uff1aBoyka\u540c\u5b66",
    type = Field()                  # people
    user_type = Field()             # people
    url_token = Field()             # Boyka2016
    is_advertiser = Field()         # false
    avatar_url = Field()            # https://pic3.zhimg.com/v2-7626555b98634ddfc6e6147588463541_is.jpg
    is_org = Field()                # false
    gender = Field()                # 1
    url = Field()                   # http://www.zhihu.com/api/v4/people/35b519a1c8b12c8ce7358afe6294aeb7",
    badge = Field()                 # [],
    id = Field()                    # 35b519a1c8b12c8ce7358afe6294aeb7