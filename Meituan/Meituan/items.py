# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    city = scrapy.Field()
    cate = scrapy.Field()
    title = scrapy.Field()
    avgScore = scrapy.Field()
    address = scrapy.Field()
    avgPrice = scrapy.Field()
    frontImg = scrapy.Field()
    
