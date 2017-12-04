# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from BDTB.items import BdtbItem

class TiebaSpider(scrapy.Spider):
    name = 'bdtb'
    allowed_domains = ['https://tieba.baidu.com/']
    pn = 0
    url = 'https://tieba.baidu.com/f?kw=巴塞罗那&ie=utf-8&pn='
    start_urls = [url + str(pn)]


    def parse(self, response):
        cate_name = response.xpath("//a[@class=' card_title_fname']/text()").extract()[0]
        cate_name = cate_name.replace(' ', '').replace('\n', '')

        lists = response.xpath("//a[@class='j_th_tit ']")
        for each in lists:
            item = BdtbItem()
            title = each.xpath('./@title').extract()[0].encode('utf-8')
            link = each.xpath('./@href').extract()[0].encode('utf-8')

            item['title'] = title
            item['link'] = 'https://tieba.baidu.com' + link
            item['cate_name'] = cate_name

            yield item

        # is_exist = response.xpath("//a[@class='next pagination-item ']")
        # if is_exist:
        #   self.pn = self.pn + 50
        #   next_url = self.url + str(self.pn)
        #   yield scrapy.Request(next_url, callback = self.parse, dont_filter = True)



            
