# -*- coding: utf-8 -*-
import scrapy
# 导入连接匹配类
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from TencentSpider.items import TencentspiderItem


class TencentSpider(CrawlSpider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?&start=0#a']

    # Response里面连接的提取规则,返回符合匹配规则的链接匹配对象的列表
    pagelink = LinkExtractor(allow = ("start=\d+"))

    rules = [
        # 获取列表里面的链接一次发送请求并且继续跟进,调用指定的回调函数
        Rule(pagelink, callback = "parseTencent", follow = True)
    ]

    # 指定的回调函数
    def parseTencent(self, response):

        for node in response.xpath("//tr[@class='even'] | tr[@class='odd']"):
            item = TencentspiderItem()
            # 取文本内容
            item['positionName'] = node.xpath("./td[1]/a/text()").extract()[0].encode("utf-8")
            # 取属性
            item['positionLink'] = "http://hr.tencent.com/" + node.xpath("./td[1]/a/@href").extract()[0].encode("utf-8")
            #
            
            if len(node.xpath("./td[2]/text()")):
                item['positionType'] = node.xpath("./td[2]/text()").extract()[0].encode("utf-8")
            else:
                item['positionType'] = ""
            
            item['peopleNum'] = node.xpath("./td[3]/text()").extract()[0].encode("utf-8")
            item['workLocation'] = node.xpath("./td[4]/text()").extract()[0].encode("utf-8")
            item['publishTime'] = node.xpath("./td[5]/text()").extract()[0].encode("utf-8")

            # 返回给管道
            yield item

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
