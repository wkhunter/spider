# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

#!/usr/bin/python3
import json
from BDTB import settings
# import pymysql

class BdtbPipeline(object):

	def __init__(self):
		self.f = open("each.json", "w")

	def process_item(self, item, spider):
		content = json.dumps(dict(item), ensure_ascii = False, indent = 1) + ",\n"
		self.f.write(content)
		return item

	def close_spider(self, spider):
		self.f.close()

# class BdtbMySqlPipeline(object):
	
# 	def __init__(self):
# 		host = get_project_settings().get('MYSQL_HOST')
# 		user = get_project_settings().get('MYSQL_USER')
# 		dbname = get_project_settings().get('MYSQL_DBNAME')
# 		password = get_project_settings().get('MYSQL_PASSWORD')

# 		db = pymysql.connect(host, user, password, dbname)

# 		if db:
# 			print('MYSQL')


