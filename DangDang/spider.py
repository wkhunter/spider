import requests
from lxml import etree
from config import *
from requests.exceptions import RequestException
import re
import json
# 取种类列表
def get_cate_text(url):
    try:
        response = requests.get(url, headers = HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析种类列表
def get_cate_list(html):
    with open('body.html', 'w') as f:
        f.write(html)
    pattern = re.compile('<dt>.*?<a.*?href="(.*?)".*?>(.*?)</a>.*?</dt>', re.S)
    items = re.findall(pattern, html)
    cate_urls = set()
    for item in items:
        cate_urls.add(item[0])
    return cate_urls

# 取图书列表
def get_book_text(url):
    try:
        response = requests.get(url, headers = HEADERS)
        if response.status_code == 200: 
            return response.text
        return None
    except RequestException:
        return None


# 解析图书列表
def get_book_list(html):
    pattern = re.compile('<li.*?ddt-pit.*?<a.*?class="pic".*?name="itemlist-picture".*?href="(.*?)".*?>.*?</a>.*?</li>', re.S)
    urls = re.findall(pattern, html)
    for url in urls:
        html = get_each_book(url)
        parse_each_book(html)

# 取书详情页
def get_each_book(url):
    try:
        response = requests.get(url, headers = HEADERS)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析书详情页
def parse_each_book(html):
    titlePat = re.compile('<h1.*?title="(.*?)".*?>.*?<img.*?>.*?</h1>', re.S)
    title = re.findall(titlePat, html)
    print(title[0].strip()) 




def main():
    url = 'http://book.dangdang.com/01.54.htm'
    # 取种类文本
    html = get_cate_text(url)
    # 取种类列表
    cate_urls = get_cate_list(html)
    for cate_url in cate_urls:
        html = get_book_text(cate_url)
        get_book_list(html)


if __name__ == '__main__':
    main()



































