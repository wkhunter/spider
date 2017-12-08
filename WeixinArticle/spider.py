import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError
from config import *
from pyquery import PyQuery as pq

# 获取代理
def get_proxy():
	try:
		response = requests.get(PROXY_POOL_URL)
		if response.status_code == 200:
			return response.text
		return None
	except ConnectionError:
		return None

def get_html(url, count = 1):
	print('Crawling ', url)
	print('Trying Count ', count)
	global proxy
	if count >= max_count:
		print('Tries Too Many Counts')
		return None
	try:
		if proxy:
			proxies = {
				'http': 'http://' + proxy
			}
			response = requests.get(url, allow_redirects = False, headers = HEADERS, 
									proxies = proxies)
		else:
			response = requests.get(url, allow_redirects = False, headers = HEADERS)
		# 成功
		if response.status_code == 200:
			return response.text
		# IP被封
		if response.status_code == 302:
			print('302')
			proxy = get_proxy()
			if proxy:
				print('using proxy', proxy)
				return get_html(url)
			else:
				print('Get Proxy Fail')
				return None
	except ConnectionError as e:
		print('Error Occurred', e.args)
		proxy = get_proxy()
		count += 1
		return get_html(url, count)

def get_index(keyword, page):
	data = {
		'query': keyword,
		'type': '2',
		'page': page
	}

	queries = urlencode(data)
	url = BASE_URL + queries
	html = get_html(url)
	return html

def parse_index(html):
	doc = pq(html)
	items = doc('.news-box .news-list li .txt-box h3 a').items()
	for item in items:
		yield item.attr('href')

def get_detail(url):
	try:
		response = requests.get(url)
		if response.status_code == 200:
			return response.text
		return None
	except ConnectionError:
		return None

def parse_detail(html):
	doc = pq(html)
	title = doc('.rich_media_title').text()
	content = doc('.rich_media_content').text()
	date = doc('#post-date').text()
	nickname = doc('#meta_content > em:nth-child(3)').text()
	wechat = doc('#js_profile_qrcode > div > p:nth-child(3) > span').text()

	return {
		'title': title,
		'content': content,
		'date': date,
		'nickname': nickname,
		'wechat': wechat
	}

def main():
	for page in range(1, 101):
		html = get_index(KEYWORD, page)
		print(html)
		if html:
			article_urls = parse_index(html)
			for article_url in article_urls:
				article_html = get_detail(article_url)
				if article_html:
					article_data = parse_detail(article_html)
					print(article_data)

if __name__ == '__main__':
	main()


# def get_html(url):
	
# 	try:
# 		response = requests.get(url, allow_redirects = False, headers = HEADERS)
# 		# 成功
# 		if response.status_code == 200:
# 			return response.text
# 		# IP被封
# 		if response.status_code == 302:
# 			print('302')
# 	except ConnectionError as e:
# 		return None

# def get_index(keyword, page):
# 	data = {
# 		'query': keyword,
# 		'type': '2',
# 		'page': page
# 	}

# 	queries = urlencode(data)
# 	url = BASE_URL + queries
# 	html = get_html(url)
# 	return html

# def main():
# 	for page in range(1, 101):
# 		html = get_index(KEYWORD, page)
# 		print(html)

# if __name__ == '__main__':
# 	main()


