# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import Request
from Douyu.items import DouyuItem
class DouyuSpider(scrapy.Spider):
    name = 'douyu'
    allowed_domains = ['http://capi.douyucdn.cn']

    offset = 0
    url = 'http://capi.douyucdn.cn/api/v1/getVerticalRoom?limit=20&offset='

    start_urls = [url + str(offset)]

    def parse(self, response):

        # json格式的数据装换成python格式
        data = json.loads(response.text)['data']
        for each in data:
            item = DouyuItem()

            item['nickname'] = each['nickname']
            item['imagelink'] = each['vertical_src']

            yield item

        self.offset += 20
        yield scrapy.Request(self.url + str(self.offset), callback = self.parse)

