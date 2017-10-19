# -*- coding: utf-8 -*-
import scrapy


class DoubanbookSpider(scrapy.Spider):
    name = 'doubanbook'
    allowed_domains = ['https://book.douban.com/annual2016']
    start_urls = ['https://book.douban.com/annual2016/?source=navigation#1']



    def parse(self, response):
        
        node_list = response.xpath('//ul[@class]/li/a')
        print 'length = ', len(node_list)
        for node in node_list:
        	print 'response.body = ', response.body
        	
