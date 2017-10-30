# -*- coding: utf-8 -*-
import scrapy
from Douban.items import DoubanItem

class DoubanmovieSpider(scrapy.Spider):
    name = 'doubanMovie'
    allowed_domains = ['movie.douban.com']
    offset = 0
    url = 'https://movie.douban.com/top250?start=' 
    start_urls = [url + str(offset)]

    def parse(self, response):
        movies = response.xpath('//div[@class="info"]')
        item = DoubanItem()
        for each in movies:
            
            title = each.xpath('.//span[@class="title"][1]/text()').extract()[0].encode("utf-8")
            bd = each.xpath('.//div[@class="bd"]/p/text()').extract()[0].encode("utf-8")
            star = each.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0].encode("utf-8")
            quote = each.xpath('.//p[@class="quote"]/span/text()').extract()

            if len(quote) != 0:
                item['quote'] = quote[0].encode("utf-8")

            item['title'] = title
            item['bd'] = bd
            item['star'] = star
            
            yield item

        if self.offset < 225:
            self.offset += 25
            print 'url = ', self.url + str(self.offset)
            yield scrapy.Request(self.url + str(self.offset), callback = self.parse, dont_filter = True)


