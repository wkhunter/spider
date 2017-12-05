import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
from bs4 import BeautifulSoup
import re
from config import *
from json.decoder import JSONDecodeError

from multiprocessing import Pool

# import pymongo
# client = pymongo.MongoClient(MONGO_URL, connect = False)
# db = client[MONGO_DB]

def get_page_index(offset, keyword):
	data = {
		'offset': offset,
		'format': 'json',
		'keyword': keyword,	
		'autoload': 'true',
		'count': 20,
		'cur_tab': 1,
	}
	url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
	response = requests.get(url)
	try:
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print('请求索引页失败')
		return None

def parse_page_index(html):
	try:
		data = json.loads(html)
		if data and 'data' in data.keys():
			for item in data.get('data'):
				yield item.get('article_url')
	except JSONDecodeError:
		pass


# 详情页
def get_page_detail(url):
	response = requests.get(url)
	try:
		if response.status_code == 200:
			return response.text
		return None
	except RequestException:
		print('请求详情页失败', url)
		return None

# 解析详情页面
def parse_page_detail(html, url):

	soup = BeautifulSoup(html, 'lxml')
	title = soup.select('title')[0].get_text()
	# images_pattern = re.compile('gallery: JSON.parse\("(.*)"\)', re.S)
	# result = re.search(images_pattern, html)
	# if result:
	# 	print(result)
	return {
		'title': title,
		'url': url
	}

# 存储到mongodb
def save_to_mongo(result):
	if db[MONGO_TABLE].insert(result):
		return True
	return False


# 下载图片
def download_image(url):
	pass

def main(offset):
	html = get_page_index(offset, KEYWORD)
	for url in parse_page_index(html):
		if url:
			html = get_page_detail(url)
		if html:
			result = parse_page_detail(html, url)
			print(result)
			# save_to_mongo(result)


if __name__ == '__main__':
	# main()
	groups = [x*20 for x in range(GROUP_START, GROUP_END + 1)]
	
	# 多线程
	pool = Pool()
	pool.map(main, groups)




