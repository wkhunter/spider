# -*- coding: utf-8 -*-
import scrapy
from DYTT.items import DyttItem

class MovieSpider(scrapy.Spider):
    name = 'Movie'
    allowed_domains = ['http://www.dy2018.net/']
    start_urls = ['http://www.dy2018.net/']

    def parse(self, response):
        types = response.xpath("//div[@class='contain']//li/a")[:11:]
        for each in types:
        	link = each.xpath('./@href').extract()[0]
        	url = 'http://www.dy2018.net' + str(link)
        	yield scrapy.Request(url, callback = self.parse_movie_list, dont_filter = True)

    def parse_movie_list(self, response):
    	result = response.xpath("//a[@class='ulink']")
    	for each in result:
    		item = DyttItem()
    		title = each.xpath('./text()').extract()[0]
    		item['title'] = title
    		link = each.xpath('./@href').extract()[0]
    		url = 'http://www.dy2018.net/' + str(link)
    		yield scrapy.Request(url, callback = self.parse_movie, meta = {'item': item}, dont_filter = True)

    def parse_movie(self, response):
    	item = response.meta['item']
    	link = response.xpath("//td[@style='WORD-WRAP: break-word']/a/@href").extract()
    	if link:
    		item['downloadlink'] = link
    		yield item

    		