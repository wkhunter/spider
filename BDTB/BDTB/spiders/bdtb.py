# -*- coding: UTF-8 -*-
#!/usr/bin/python3
import scrapy
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from BDTB.items import BdtbItem
import json

class TiebaSpider(scrapy.Spider):
    name = 'bdtb'
    allowed_domains = ['https://tieba.baidu.com/']
    pn = 0
    url = 'https://tieba.baidu.com/f?kw=巴塞罗那&ie=utf-8&pn='
    start_urls = [url + str(pn)]


    def parse(self, response):
        lists = response.xpath("//div[@class='threadlist_lz clearfix']")
        for each in lists:
            item = BdtbItem()
            title = each.xpath(".//a[@class='j_th_tit ']/@title").extract()[0].encode('utf-8')
            link = 'https://tieba.baidu.com' + each.xpath(".//a[@class='j_th_tit ']/@href").extract()[0].encode('utf-8')
            author = each.xpath(".//span[@class='frs-author-name-wrap']/a/text()")
            if author:
                author = each.xpath(".//span[@class='frs-author-name-wrap']/a/text()").extract()[0].encode('utf-8')
            item['title'] = title
            item['link'] = link
            item['author'] = author
            comments = []
            current_pn = 1
            meta = {
                "item": item,
                "comments": comments,
                "current_pn": current_pn,
                "link": link
            }
            yield scrapy.Request(link, meta = meta, callback = self.parse_detail, dont_filter = True)

        
        is_exist = response.xpath("//div[@id='frs_list_pager']/a[@class='next pagination-item ']")
        if is_exist:
            self.pn += 50
            next_url = self.url + str(self.pn)
            yield scrapy.Request(next_url, callback = self.parse, dont_filter = True)

    def parse_detail(self, response):
        current_pn = response.meta['current_pn']
        link = response.meta['link']
        comments = response.meta['comments']
        item = response.meta['item']
        lists = response.xpath("//div[contains(@class, 'l_post l_post_bright')]")
        
        totalpage = response.xpath("//div[@class='pb_footer']//li[@class='l_reply_num']/span[2]/text()").extract()[0].encode('utf-8')
        totalpage = int(totalpage)
        next_pn = current_pn + 1
        for each in lists:
            eachone = {}
            name = each.xpath(".//li[@class='d_name']/a/text()").extract()[0].encode('utf-8')
            homelink = "tieba.baidu.com" + each.xpath(".//li[@class='d_name']/a/@href").extract()[0].encode('utf-8')
            content = each.xpath(".//div[contains(@id, 'post_content')]/text()").extract()[0].encode('utf-8')
            if content:
                content = each.xpath(".//div[contains(@id, 'post_content')]/text()").extract()[0].encode('utf-8')
            else:
                content = ''

            eachone['name'] = name
            eachone['homelink'] = homelink
            eachone['content'] = content.replace(" ", '').replace('\\', '')

            comments.append(eachone)
        if next_pn <= totalpage:
            next_url = link + '?pn=' + str(next_pn)
            meta = {
                'item': item,
                'comments': comments,
                'current_pn': next_pn,
                'link': link
            }

            yield scrapy.Request(next_url, meta = meta, callback = self.parse_detail, dont_filter = True)
        else:
            item['comments'] = comments
            yield item
        

            






















            
