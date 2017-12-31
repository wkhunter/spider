# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class UserItem(Item):
    
    name = Field()
    avatar_url = Field()
    url_token = Field()
    headline = Field()
    description = Field()
    url = Field()
    gender = Field()
    type = Field()
    id = Field()
    badge = Field()
    follower_count = Field()
    user_type = Field()
    employments = Field()
    answer_count = Field()
    articles_count = Field()

