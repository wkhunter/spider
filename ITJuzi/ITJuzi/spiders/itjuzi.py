# -*- coding: utf-8 -*-
import scrapy


class ItjuziSpider(scrapy.Spider):
    name = 'itjuzi'
    allowed_domains = ['https://www.itjuzi.com/']
    start_urls = ['https://www.itjuzi.com/']

    def parse(self, response):
        print(response.text)
