# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json
from Meituan.items import MeituanItem

class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['http://tianchang.meituan.com/']
    start_url = 'http://tianchang.meituan.com/meishi/'
    url = 'http://tianchang.meituan.com/meishi/api/poi/getPoiList?cityName=天长&page=1'
    city_url = 'http://tianchang.meituan.com/meishi/api/poi/getPoiList?cityName={city}&page=1'
    def get_header(self):
        headers = {
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Upgrade-Insecure-Requests': '1',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
           'Host': 'tianchang.meituan.com',
        }
        return headers

    def get_cookie(self):
        cookie = 'mtcdn=K; lsu=; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=160ca0d75b618-0c599821fd7f6b-16386656-fa000-160ca0d75b7c8; _lxsdk=160ca0d75b618-0c599821fd7f6b-16386656-fa000-160ca0d75b7c8; __mta=251982390.1515218368682.1515218368682.1515218368682.1; ci=626; client-id=066795d3-04f3-48c5-ab17-a20672c7b8d5; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; oc=ktEyRwIXrfUG7Mza5eJlC8mW015P-k_3mT6LtmaHXBKSjUnO_F5aI3HbDPyzw9k4gWWp-rY_4CbQcXStXM_-aR1S_1kX4lJhCx5toYBcU5gVTGS_V5HS1UJYpuByNHEv19PmwaeYVuMaWzDKe6XTJ7e1xSfLwjQF4xbvK6NhcRs; SID=p8n4gp09c3aklia0qf92rld1m1; em=bnVsbA; om=bnVsbA; __mta=251982390.1515218368682.1515218368682.1515219551991.2; _lxsdk_s=160ca0d75bb-548-d28-97e%7C%7C22; u=320615150; n=bHe902220266; lt=vY61yM8C8aW_iAb4tcsA7XG7er4AAAAAMgUAAP2W3qEJFrTXhO83XpenuBTRGXkn9ZL7MZ80XlgcGpdsZCagvntNitgG8twPwn-_yw; token2=vY61yM8C8aW_iAb4tcsA7XG7er4AAAAAMgUAAP2W3qEJFrTXhO83XpenuBTRGXkn9ZL7MZ80XlgcGpdsZCagvntNitgG8twPwn-_yw; uuid=2f083f6904e74d76a87d.1515218280.2.0.1'
        arr = cookie.replace(' ', '').split(';')
        cookies = {}
        for string in arr:
            string = string.split('=')
            cookies[string[0]] = string[1]
        return cookies 

    def start_requests(self):
        cookies = self.get_cookie()
        headers = self.get_header()
        url = 'http://www.meituan.com/changecity/'
        yield scrapy.Request(url = url, headers = headers, cookies = cookies, callback = self.parse_city)

        # yield scrapy.Request(url = self.url, headers = headers, 
        #                     cookies = cookies, callback = self.parse)

    def parse_city(self, response):
        cities = response.xpath("//div[@class='city-area']/span[@class='cities']/a/text()").extract()
        headers = self.get_header()
        cookies = self.get_cookie()
        for city in cities:
            meta = {'city': city}
            yield scrapy.Request(url = self.city_url.format(city = city), headers = headers, 
                            cookies = cookies, meta = meta, callback = self.parse, dont_filter = True)

    def parse(self, response):
        city = response.meta['city']
        result = response.text
        result = json.loads(result)
        totalCounts = result.get('data').get('totalCounts')
        poiInfos = result.get('data').get('poiInfos')
        if len(poiInfos) >= 1:
            for each in poiInfos:
                item = MeituanItem()
                item['city'] = city
                item['frontImg'] = each.get('frontImg')
                item['title'] = each.get('title')
                item['avgScore'] = each.get('avgScore')
                item['address'] = each.get('address')
                item['avgPrice'] = each.get('avgPrice')
                yield item
        else:
            pass


















