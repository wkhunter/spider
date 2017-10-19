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
    # 电影链接
    movie_link = scrapy.Field()
    # 电影评论
    movie_comment = scrapy.Field()

class DoubanmovieComment(scrapy.Item):
	# 评论内容
	comment_content = scrapy.Field()
	# 评论作者
	comment_author = scrapy.Field()
