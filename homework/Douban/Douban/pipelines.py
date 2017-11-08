# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
class DoubanPipeline(object):
    def __init__(self):
        self.f = open('movie.json', 'w')
        self.list = []

    def process_item(self, item, spider):
        # content = json.dumps(dict(item), ensure_ascii = False) + ",\n"
        # self.f.write(content)
        item = dict(item)
        self.list.append(item)
        return item

    def close_spider(self, spider):
        content = json.dumps(self.list, ensure_ascii = False, indent = 1)
        self.f.write(content)
        self.f.close()
