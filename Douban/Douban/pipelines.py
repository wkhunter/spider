# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
import json
from scrapy.conf import settings

class DoubanPipeline(object):

    def __init__(self):
        host = settings['MANGODB_HOST']
        port = settings['MANGODB_PORT']
        dbname = settings['MANGODB_DBNAME']
        sheetname = settings['MANGODB_SHEETNAME']

        # 创建mangodb的数据库连接
        client = pymongo.MongoClient(host = host, port = port)
        # 指定数据库
        mydb = client[dbname]
        # 指定存放数据的数据库表名称
        self.post = mydb[sheetname]

    def process_item(self, item, spider):
        
        data = dict(item)
        self.post.insert(data)
        return item









