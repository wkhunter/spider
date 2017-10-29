# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from Dongguan.items import DongguanItem

class SunSpider(CrawlSpider):
    name = 'sun'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?type=4&page=0']

    rules = (
        Rule(LinkExtractor(allow=r'type=4'), process_links = 'deal_links', follow = True),
        Rule(LinkExtractor(allow=r'/html/question/\d+/\d+.shtml'), callback = 'parse_item')
    )

    # 处理连接
    # 重新处理每个response里面提取的链接 Type&page=xxx?type=4 修改为 Type?page=xxx&type=4
    # links就是LinkExtractor提取出来的当前页面的链接列表
    def deal_links(self, links):
        for link in links:
            link.url = link.url.replace("?", "&").replace("Type&", "Type?")
        return links

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
