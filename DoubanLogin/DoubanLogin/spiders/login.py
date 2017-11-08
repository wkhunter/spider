# -*- coding: utf-8 -*-
import scrapy


class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ["douban.com"]
    start_urls = ['https://movie.douban.com/top250']
    
    def start_requests(self):
        url='https://www.douban.com/accounts/login'
        yield scrapy.FormRequest(
                url = url,
                formdata = {
                    "form_email": "731404438@qq.com",
                    "form_password": "ly731404438",
                },
                callback = self.check_login
            )
    def check_login(self, response):
        yield scrapy.Request('https://www.douban.com/', callback = self.parse_page)
    def parse_page(self, response):
        print 'body = ', response.body
