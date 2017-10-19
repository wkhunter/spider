# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

class Doubanmovie250Pipeline(object):

	def __init__(self):
		self.f = open('movie.json', 'w')
		self.movies = []

	def process_item(self, item, spider):
		self.movies.append((dict(item)))
		# content = json.dumps(dict(item), ensure_ascii = False) + ',\n'
		# self.f.write(content)
		return item

	def close_spider(self, spider):
		content = json.dumps(self.movies, ensure_ascii = False, indent = 1)
		self.f.write(content)
		self.f.close()

