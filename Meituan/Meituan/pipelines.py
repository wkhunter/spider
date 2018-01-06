# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json

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
