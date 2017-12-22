# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random, base64
from selenium import webdriver
# from settings import USER_AGENTS, PROXIES

from scrapy.downloadermiddlewares.redirect import RedirectMiddleware

class MyRedirectMiddleware(RedirectMiddleware):
    def _redirect(self, redirected, request, spider, reason):
        print('requesturl = ', request.url)
        print('requesturl = ', redirected.url)
        is_redirect = self.is_redirect(redirected.url)
        if is_redirect:
            self.kill_redirect(redirected.url)
        return request

    # 判断是否重定向
    def is_redirect(self, url):
        if 'https://sec.douban.com/b?r=https%3A%2F%2Fmovie.douban.com%2Ftop250%3Fstart%3D' in url:
            return True
        else:
            return False
    # 解决重定向
    def kill_redirect(self, url):
        driver = webdriver.PhantomJS()
        driver.get(url)
        driver.save_screenshot('login.png')
        login = driver.find_element_by_tag_name('a')
        login.submit()
        driver.save_screenshot('login1.png')

        # 账号
        form_email = driver.find_element_by_id('email')
        # 密码
        form_password = driver.find_element_by_id('password')
        # 验证码
        captcha_solution = driver.find_element_by_id('captcha_field')
        # 登录按钮
        submit = driver.find_element_by_class_name('btn-submit')

        # 验证码图片
        captcha = driver.find_element_by_id('captcha_image').get_attribute('src')
        print('captcha = ', captcha)
        # 填写
        form_email.send_keys('15855092013')
        form_password.send_keys('900124')
        capt = input('输入验证码-->')
        captcha_solution.send_keys(capt)

        submit.click()
        driver.save_screenshot('yes.png')



        # href = login.get_attribute('href')
        # driver.get(href)
        # driver.save_screenshot('login1.png')

        # # 账号
        # form_email = driver.find_element_by_id('email')
        # # 密码
        # form_password = driver.find_element_by_id('password')
        # # 验证码
        # captcha_solution = driver.find_element_by_id('captcha_field')
        # # 登录按钮
        # submit = driver.find_element_by_class_name('btn-submit')

        # # 验证码图片
        # captcha = driver.find_element_by_id('captcha_image').get_attribute('src')
        # print('captcha = ', captcha)
        # # 填写
        # form_email.send_keys('15855092013')
        # form_password.send_keys('900124')
        # capt = input('输入验证码-->')
        # captcha_solution.send_keys(capt)

        # submit.click()
        # driver.save_screenshot('yes.png')

        


class RandomUserAgent(object):
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault("User-Agent", useragent)

class RandomProxy(object):
    # pass
    def process_request(self, request, spider):
        proxy = random.choice(PROXIES)
        if proxy['user_password'] is None:
            request.meta['proxy'] = "http://" + proxy['ip_port']
        else:
            base64Userpassword = base64.b64encode(proxy['user_password'])
            request.headers['Proxy-Authorization'] = 'Basic ' + base64Userpassword
            request.meta['proxy'] = "http://" + proxy['ip_port']

        


class DoubanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
