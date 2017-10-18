# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Doubanmovie250Item(scrapy.Item):
	# 电影名称
    movie_title = scrapy.Field()
    # 电影评分
    movie_star = scrapy.Field()
    # 电影描述
    movie_quote = scrapy.Field()
