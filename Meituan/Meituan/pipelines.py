# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import pymysql
import chardet

class MeituanPipeline(object):

    def __init__(self):
        self.file = open('items.txt', 'wb')

    def process_item(self, item, spider):
        with open('items.txt', 'a') as f:
            f.write(str(item) + ',\n')
            f.close()
        return item

    def close_spider(self, spider):
        self.file.close()

class MysqlPipelene(object):
	def __init__(self):
		self.conn = pymysql.connect(host = 'localhost', port = 3306, user = 'root',
						passwd = 'admin123', db = 'Meituan', charset = 'utf8')
		self.cur = self.conn.cursor()

	def process_item(self, item, spider):
		self.cur.execute('INSERT INTO meishi (city, frontImg, title, avgScore, address, avgPrice) VALUES (%s, %s, %s, %s, %s, %s)', (item['city'].encode('utf-8'), item['frontImg'], item['title'].encode('utf-8'), item['avgScore'], item['address'].encode('utf-8'), item['avgPrice']))
		self.conn.commit()
		return item

	def close_spider(self, spider):
		self.cur.close()
		self.conn.close()

















