# -*- coding: utf-8 -*-
import scrapy
from ZhihuUser.items import UserItem
import json

class ZhihuSpider(scrapy.Spider):
    name = 'user'
    allowed_domains = ['https://www.zhihu.com']
    follow_url = 'https://www.zhihu.com/api/v4/members/{user}/followees?include=data%5B*%5D.answer_count%2Carticles_count%2Cgender%2Cfollower_count%2Cis_followed%2Cis_following%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics&offset=20&limit=20'
    user_url = 'https://www.zhihu.com/api/v4/members/{user}?include=allow_message%2Cis_followed%2Cis_following%2Cis_org%2Cis_blocking%2Cemployments%2Canswer_count%2Cfollower_count%2Carticles_count%2Cgender%2Cbadge%5B%3F(type%3Dbest_answerer)%5D.topics'
    def start_requests(self):
        yield scrapy.Request(url = self.user_url.format(user = 'excited-vczh'), callback = self.parse_user)
        yield scrapy.Request(url = self.follow_url.format(user = 'excited-vczh'), callback = self.parse_follow)
   
    def parse_user(self, response):
        results = json.loads(response.text)
        item = UserItem()
        for field in item.fields:
            if field in results.keys():
                item[field] = results.get(field)
        yield item
        yield scrapy.Request(url = self.follow_url.format(user = item['url_token']), callback = self.parse_follow)

    def parse_follow(self, response):
        results = json.loads(response.text)
        if 'data' in results.keys():
            for result in results.get('data'):
                url = self.user_url.format(user = result.get('url_token'))
                yield scrapy.Request(url = url, callback = self.parse_user, dont_filter = True)


        is_end = results.get('paging').get('is_end')
        if 'paging' in results.keys() and is_end == False:
            next_url = results.get('paging').get('next')
            yield scrapy.Request(next_url, callback = self.parse_follow, dont_filter = True)
























