# -*- coding: utf-8 -*-
import scrapy


class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['http://zhibo.renren.com']
    start_urls = ['http://http://zhibo.renren.com/']


    def start_requests(self):
    	url = 'http://www.renren.com/PLogin.do'
    	yield scrapy.FormRequest(
    			url = url,
    			formdata = {
    				'email': '18455086673',
    				'password': 'admin123'
    			},
    			callback = self.parse_page
    		)
    def parse_page(self, response):
    	with open('renren.html', 'wb') as f:
    		f.write(response.body)
