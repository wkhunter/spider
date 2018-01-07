# -*- coding: utf-8 -*-
import scrapy
import time
import re
import json
from Meituan.items import MeituanItem

class MeituanSpider(scrapy.Spider):
    name = 'meituan'
    allowed_domains = ['http://tianchang.meituan.com/']
    food_url = 'http://as.meituan.com/meishi/api/poi/getPoiList?cityName={city}&page=1'
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
        cookie = 'mtcdn=K; lsu=; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=160ca0d75b618-0c599821fd7f6b-16386656-fa000-160ca0d75b7c8; _lxsdk=160ca0d75b618-0c599821fd7f6b-16386656-fa000-160ca0d75b7c8; oc=ktEyRwIXrfUG7Mza5eJlC8mW015P-k_3mT6LtmaHXBKSjUnO_F5aI3HbDPyzw9k4gWWp-rY_4CbQcXStXM_-aR1S_1kX4lJhCx5toYBcU5gVTGS_V5HS1UJYpuByNHEv19PmwaeYVuMaWzDKe6XTJ7e1xSfLwjQF4xbvK6NhcRs; iuuid=69F4D0D1ED689EA8B59821A2C4A1B6558AE4713B077AA680CF51F6412BD76F38; isid=D89151DBC2F5B5898099BCF84B6D0020; oops=vY61yM8C8aW_iAb4tcsA7XG7er4AAAAAMgUAAP2W3qEJFrTXhO83XpenuBTRGXkn9ZL7MZ80XlgcGpdsZCagvntNitgG8twPwn-_yw; logintype=normal; cityname=%E5%A4%A9%E9%95%BF; __mta=251982390.1515218368682.1515296258033.1515301346073.18; ci=151; rvct=151%2C742%2C237%2C626; u=320615150; n=bHe902220266; lt=dH1bu9-Et2J5Qd7w7kHQgMeZaqMAAAAAMgUAAIo-BO-0BU7SxZ2wDMNa8GwT8OAsCNpKaLTiP63R30OZgtt79HDZo2ofmcHy-4bUPw; token2=dH1bu9-Et2J5Qd7w7kHQgMeZaqMAAAAAMgUAAIo-BO-0BU7SxZ2wDMNa8GwT8OAsCNpKaLTiP63R30OZgtt79HDZo2ofmcHy-4bUPw; uuid=2f083f6904e74d76a87d.1515218280.3.0.1; em=bnVsbA; om=bnVsbA; unc=bHe902220266; client-id=14872f5e-0bd1-4045-9fae-6cbe4f41b684; p_token=vY61yM8C8aW_iAb4tcsA7XG7er4AAAAAMgUAAP2W3qEJFrTXhO83XpenuBTRGXkn9ZL7MZ80XlgcGpdsZCagvntNitgG8twPwn-_yw; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; __mta=251982390.1515218368682.1515301346073.1515301409203.19; _lxsdk_s=160ceff9769-384-4f2-110%7C%7C10'
        arr = cookie.replace(' ', '').split(';')
        cookies = {}
        for string in arr:
            string = string.split('=')
            cookies[string[0]] = string[1]
        return cookies 

    # 发送获取城市请求
    def start_requests(self):
        cookies = self.get_cookie()
        headers = self.get_header()
        url = 'http://www.meituan.com/changecity/'
        yield scrapy.Request(url = url, headers = headers, cookies = cookies, callback = self.parse_city)

    # 解析获取城市,发送城市对应的美食请求
    def parse_city(self, response):
        cities = response.xpath("//div[@class='city-area']/span[@class='cities']/a/text()").extract()
        headers = self.get_header()
        cookies = self.get_cookie()
        for city in cities:
            # print(city)
            meta = {'city': city}
            yield scrapy.Request(url = self.food_url.format(city = city), headers = headers, 
                            cookies = cookies, meta = meta, callback = self.parse, dont_filter = True)
    # 解析美食
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












