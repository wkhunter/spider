# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from Tencent.items import TencentItem

class TencentSpider(scrapy.Spider):
    name = 'tencent'
    allowed_domains = ['tencent.com']
    baseURL = "http://hr.tencent.com/position.php?&start="
    offset = 0

    start_urls = [baseURL + str(offset)]

    def parse(self, response):
        node_list = response.xpath("//tr[@class='even'] | //tr[@class='odd']")

        for node in node_list:
        	item = TencentItem()

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
    	if not len(response.xpath("//a[@class='noactive' and @id='next']")):
    		nextURL = response.xpath("//a[@id='next']/@href").extract()[0]
    		yield scrapy.Request("http://hr.tencent.com/" + nextURL, callback = self.parse)

