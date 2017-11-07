# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # 职位名称
    position = scrapy.Field()
    # 薪水
    money = scrapy.Field()
    # 经验
    exp = scrapy.Field()
    # 公司
    company = scrapy.Field()
    # 发布时间
    time = scrapy.Field()
    # 链接
    link = scrapy.Field()
    # 地址
    address = scrapy.Field()
