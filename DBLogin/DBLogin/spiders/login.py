# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request, FormRequest

class LoginSpider(scrapy.Spider):
    name = 'login'
    allowed_domains = ['https://movie.douban.com/']
    header={
        "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
    }

    url = "https://movie.douban.com/subject/24860563/?from=subject-page"

    def start_requests(self):
        return [scrapy.Request('https://accounts.douban.com/login', headers = self.header,
                    callback = self.parse, meta = {'cookiejar':1}, dont_filter = True)]

    def parse(self, response):
        captcha = response.xpath("//img[@id='captcha_image']/@src")
        # print(captcha)
        if len(captcha) > 0:
            captcha = response.xpath("//img[@id='captcha_image']/@src").extract()[0].encode('utf-8')
            print(captcha)
            with open('captcha.jpg', 'wb') as f:
                f.write(captcha)
                f.close()
            captcha = raw_input("please input the captcha\n>")

            data = {
                    "form_email": "15855092013",
                    "form_password": "900124",
                    "captcha-solution": captcha,
                    "redir": "https://www.douban.com/people/170486090/"
                }
        else:
            data = {
                "form_email": "15855092013",
                "form_password": "900124",
                "redir": "https://www.douban.com/people/170486090/"
            }
        return [FormRequest.from_response(
                response,
                dont_filter = True,
                meta = {"cookiejar": response.meta['cookiejar']},
                headers = self.header,
                formdata = data,
                callback = self.get_content,
                
            )]

    def get_content(self, response):
        print(response.body)
        with open('body.html', 'w') as f:
            f.write(response.body)
        # return scrapy.Request(self.url, callback = self.parse_movie, meta = {'cookiejar':1}, dont_filter = True)

    def parse_movie(self, response):
        pass
        # print(response.body)
