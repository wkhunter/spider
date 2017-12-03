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
    answer_count = Field()
    gender = Field()
    headline = Field()


    
