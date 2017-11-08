# -*- coding: utf-8 -*-
import scrapy
from Douban.items import DoubanItem

class DoubanSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = 'https://movie.douban.com/top250?start=' 
    start_urls = [url + str(offset)]

    def parse(self, response):
        movies = response.xpath('//div[@class="info"]')
        
        for each in movies:
            item = DoubanItem()
            title = title = each.xpath('.//span[@class="title"][1]/text()').extract()[0].encode("utf-8")                
            bd = each.xpath('.//div[@class="bd"]/p/text()').extract()[0].encode("utf-8")
            star = each.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0].encode("utf-8")
            quote = each.xpath('.//p[@class="quote"]/span/text()').extract()
            url = each.xpath('.//a/@href').extract()[0].encode("utf-8")
            if len(quote) != 0:
                item['quote'] = quote[0].encode("utf-8")

            item['title'] = title
            item['bd'] = bd.replace(" ", "").replace("\n", "")
            item['star'] = star
            item['url'] = url   
                     
            yield scrapy.Request(url, meta = {'item': item}, callback = self.parse_detail, dont_filter = True)
        if self.offset < 225:
            self.offset += 25
            yield scrapy.Request(self.url + str(self.offset), callback = self.parse, dont_filter = True)

    def parse_detail(self, response):
        item = response.meta['item']
        info = response.xpath('//div[@class="indent"]/span[1]/text()').extract()[0].encode("utf-8") 
        item['info'] = info.replace(" ", "")
        yield item
