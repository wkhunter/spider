# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['https://movie.douban.com/']
    header={"User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"}

    url = "https://movie.douban.com/subject/24860563/?from=subject-page"

    def start_requests(self):
        return [scrapy.Request('https://accounts.douban.com/login', 
                    callback = self.parse, meta = {'cookiejar':1}, dont_filter = True)]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src").extract()[0].encode('utf-8')
        print(captcha)
        if len(captcha) > 0:
            with open('captcha.jpg', 'wb') as f:
                f.write(captcha)
                f.close()
            captcha = raw_input("please input the captcha\n>")

            data = {
                    "form_email": "731404438@qq.com",
                    "form_password": "ly731404438",
                    "captcha-solution": captcha,
                    # "redir": "https://movie.douban.com/subject/3604148/"
                }
        else:
            data = {
                "form_email": "731404438@qq.com",
                "form_password": "ly731404438",
                # "redir": "https://movie.douban.com/subject/3604148/"
            }
        return [FormRequest.from_response(
                response,
                dont_filter = True,
                meta = {"cookiejar": response.meta['cookiejar']},
                headers = self.header,
                formdata = data,
                callback = self.get_content
            )]

    def get_content(self, response):
        with open('body.html', 'w') as f:
            f.write(response.body)
        return scrapy.Request(self.url, callback = self.parse_movie, meta = {'cookiejar':1}, dont_filter = True)

    def parse_movie(self, response):

        print(response.body)
