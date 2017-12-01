# -*- coding: utf-8 -*-
import scrapy


class TiebaSpider(scrapy.Spider):
    name = 'bdtb'
    allowed_domains = ['https://tieba.baidu.com/']
    start_urls = ['https://tieba.baidu.com/f?kw=巴塞罗那&fr=index']

    def parse(self, response):
        with open('response.html', 'w') as f:
        	f.write(response.body)
