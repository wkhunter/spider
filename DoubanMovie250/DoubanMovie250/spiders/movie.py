# -*- coding: utf-8 -*-
import scrapy
from DoubanMovie250.items import Doubanmovie250Item, DoubanmovieComment

from scrapy.http import Request

class MovieSpider(scrapy.Spider):
	name = 'movie'
	allowed_domains = ['https://movie.douban.com']
	
	start_urls = ["https://movie.douban.com/top250?start=0&filter="]


	def parse(self, response):
		node_list = response.xpath('//div[@class="item"]')

		items = []
		for node in node_list:
			item = Doubanmovie250Item()

			movie_title = node.xpath('./div[@class="info"]/div[@class="hd"]/a/span[1]/text()').extract()[0].encode("utf-8")
			movie_star = node.xpath('./div[@class="info"]/div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0].encode("utf-8")
			movie_link = node.xpath('./div[1]/a/@href').extract()[0].encode("utf-8")
			if len(node.xpath('./div[@class="info"]/div[@class="bd"]/p/span/text()')):
				movie_quote = node.xpath('./div[@class="info"]/div[@class="bd"]/p/span/text()').extract()[0].encode("utf-8")
			else:
				movie_quote = ''
			item['movie_link'] = movie_link
			item['movie_title'] = movie_title
			item['movie_star'] = movie_star
			item['movie_quote'] = movie_quote
			yield  item

		if len(response.xpath('//link[@rel="next" and @href]')):
			nextURL = response.xpath('//link[@rel="next"]/@href').extract()[0]
			url = 'https://movie.douban.com/top250' + nextURL
			yield Request(url, callback = self.parse, dont_filter = True)

	







