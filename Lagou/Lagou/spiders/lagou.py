# -*- coding: utf-8 -*-
import scrapy
from Lagou.items import LagouItem

class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com/']
    start_urls = ['https://www.lagou.com/zhaopin/Python/']



    def parse(self, response):
        # 职位名称 /div[@class="position"]
        # 公司名称 /div[@class="company"]/div[1]/a
        # 薪水 /div[@class="position"]/div[@class="p_bot"]//span[@class="money"]
        # 经验 /div[@class="position"]/div[@class="p_bot"]/div[@class="li_b_l"]/text()
        # 发布时间 /div[@class="position"]/div[@class="p_top"]/span
        jobs = response.xpath('//div[@class="list_item_top"]')
        for job in jobs:
            item = LagouItem()
            position = job.xpath('./div[@class="position"]/div[@class="p_top"]/a/h3/text()').extract()[0].encode("utf-8")
            company = job.xpath('./div[@class="company"]/div[1]/a/text()').extract()[0].encode("utf-8")
            money = job.xpath('./div[@class="position"]/div[@class="p_bot"]//span[@class="money"]/text()').extract()[0].encode("utf-8")
            time = job.xpath('./div[@class="position"]/div[@class="p_top"]/span/text()').extract()[0].encode("utf-8")
            link = job.xpath('./div[@class="position"]/div[@class="p_top"]/a/@href').extract()[0].encode("utf-8")

            item['position'] = position
            item['company'] = company
            item['money'] = money
            item['time'] = time
            item['link'] = link

            yield scrapy.Request(link, meta = {'item': item}, callback = self.parse_detail, dont_filter = True)

    def parse_detail(self, response):
        item = response.meta['item']
        exp = response.xpath('//p/span[3]/text()')
        if exp:
            exp = response.xpath('//p/span[3]/text()').extract()[0].encode("utf-8")

        address = response.xpath('//div[@class="work_addr"]')
        if address:
            address = response.xpath('//div[@class="work_addr"]/a[1]/text()').extract()[0].encode("utf-8")
        item['exp'] = exp
        item['address'] = address
        yield item




















