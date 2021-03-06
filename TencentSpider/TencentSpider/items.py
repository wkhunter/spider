# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TencentspiderItem(scrapy.Item):
    # 职位名称
    positionName = scrapy.Field()
    # 职位详情
    positionLink = scrapy.Field()
    # 只为类别
    positionType = scrapy.Field()
    # 人数
    peopleNum = scrapy.Field()
    # 工作地点
    workLocation = scrapy.Field()
    # 发布时间
    publishTime = scrapy.Field()
