# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # 电影名称
    title = scrapy.Field()
    # 信息
    bd = scrapy.Field()
    # 评分
    star = scrapy.Field()
    # 引用
    quote = scrapy.Field()
    # 链接
    url = scrapy.Field()
    # 简介
    info = scrapy.Field()
    