import requests
from lxml import etree
from config import *
from requests.exceptions import RequestException
import re
import json
from multiprocessing import Pool
import socket
socket.setdefaulttimeout(3)
from threading import Thread

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
    except requests.exceptions.ConnectTimeout:
        NETWORK_STATUS = False
    except requests.exceptions.Timeout:
        REQUEST_TIMEOUT = True


# 解析图书列表
def parse_book_list(html):
    itemP = re.compile('<li.*?ddt-pit=.*?class=.*?id=.*?<a.*?title="(.*?)".*?ddclick.*?class.*?name.*?dd_name.*?href="(.*?)".*?>.*?<span.*?class.*?>&yen;(.*?)</span>.*?<a.*?href.*?dd_name.*?title=.*?>(.*?)</a>.*?</a>.*?</li>', re.S)
    items = re.findall(itemP, html)
    for item in items:
        each = {}
        each['title'] = item[0].strip()
        each['link'] = item[1]
        each['money'] = item[2] + '元'
        each['author'] = item[3]
        yield each

    # 下一页
    nextP = re.compile('<li.*?class="next"><a.*?href="(.*?)".*?title.*?>.*?</a></li>', re.S)
    next_url = re.findall(nextP, html)
    if next_url:
        next_url = 'http://category.dangdang.com/' + next_url[0]
        html = get_book_text(next_url)
        items = parse_book_list(html)
        for item in items:
            print('正在写入' + item['title'])
            write_to_file(item)
     
# 写入文件
def write_to_file(item):
    with open('book.txt', 'a') as f:
        f.write(json.dumps(item, ensure_ascii = False) + ',\n')

def main(url):
    
    # 取种类文本
    html = get_cate_text(url)
    # 取种类列表
    cate_urls = get_cate_list(html)
    for cate_url in cate_urls:
        html = get_book_text(cate_url)
        items = parse_book_list(html)
        for item in items:
            print('正在写入' + item['title'])
            write_to_file(item)   

if __name__ == '__main__':
    url = 'http://book.dangdang.com/01.54.htm'
    main(url)




