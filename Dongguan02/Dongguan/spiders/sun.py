# -*- coding: utf-8 -*-
import scrapy

from Dongguan.items import DongguanItem

class SunSpider(scrapy.Spider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    url = 'http://wz.sun0769.com/index.php/question/questionType?type=4&page=0'

    offset = 0
    start_urls = [url + str(offset)]

    def parse(self, response):
        # 每一页的所有帖子的链接集合
        links = response.xpath('//div[@class="greyframe"]/table//td/a[@class="news14"]/@href').extract()
        for link in links:
            # 提取列表里面每个帖子的链接,发送方请求并调用parse_item来处理
            yield scrapy.Request(link, callback = self.parse_item)

        if self.offset <= 71160:
            self.offset += 30
            yield scrapy.Request(self.url + str(self.offset), callback = self.parse)


    # 处理每个帖子的response内容
    def parse_item(self, response):
        item = DongguanItem()
        item['title'] = response.xpath('//div[@class="pagecenter p3"]//strong/text()').extract()[0]
        item['number'] = item['title'].split(' ')[-1].split(':')[-1]

        # 内容,先取出有图片情况下的匹配规则,如果没有内容则列表为空
        content = response.xpath('//div[@class="contentext"]/text()').extract()
        # 没有内容,则返回列表Wie空,则使用无图片情况下的匹配规则
        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()[0]
            item['content'] = "".join(content).strip()
            
        else:
            item['content'] = "".join(content).strip()
        # 
        item['url'] = response.url

        yield item
