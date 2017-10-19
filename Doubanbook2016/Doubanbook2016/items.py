# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubanbook2016Item(scrapy.Item):
    book_link = scrapy.Field()
    book_title = scrapy.Field()
    book_order = scrapy.Field()
    book_rating = scrapy.Field()
