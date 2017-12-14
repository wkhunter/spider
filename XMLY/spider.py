import requests
from bs4 import BeautifulSoup
from lxml import etree
import os
import time
from multiprocessing import Pool

headers = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'
}

def get_detail_url(url):
	# pool = Pool()
	# start_urls = ['http://www.ximalaya.com/dq/all/{}/'.format(pn) for pn in range(1, 85)]
	# for url in start_urls:
	response = requests.get(url, headers = headers).text
	soup = BeautifulSoup(response, 'lxml')
	for item in soup.find_all('div', class_ = 'albumfaceOutter'):
		href = item.a['href']
		title = item.img['alt']
		img_url = item.img['src']
		content = {
			'href': href,
			'title': title,
			'img_url': img_url
		}
		print('正在下载--> {}频道'.format(item.img['alt']))
		get_mp3(href, title)
		time.sleep(1)
		break

def get_mp3(url, title):
	response = requests.get(url, headers = headers).text
	num_list = etree.HTML(response).xpath('//div[@class="personal_body"]/@sound_ids')[0].split(',')
	print(title + u'频道存在{}个音频'.format(len(num_list)))
	mkdir(title)
	# 切换路径
	os.chdir('/Users/dllo/Desktop/spiderScrapy/XMLY/dir/' + title)
	for id in num_list:
		json_url = 'http://www.ximalaya.com/tracks/{}.json'.format(id)
		html = requests.get(json_url, headers = headers).json()
		vtitle = html['title']
		mp4_url = html.get('play_path')
		download(mp4_url, vtitle)
		print('{}下载成功'.format(mp4_url))

def download(url, vtitle):
	# print(url)
	# content返回二进制
	content = requests.get(url, headers = headers).content
	name = url.split('.')[-1]
	with open(vtitle+ '.' + name, 'wb') as f:
		f.write(content)

# 创建对应的文件夹
def mkdir(title):
	path = title.strip()
	isExist = os.path.exists(os.path.join(r'/Users/dllo/Desktop/spiderScrapy/XMLY/dir', path))
	if not isExist:
		print(u'创建名字为-->{}-->文件夹'.format(title))
		os.makedirs(os.path.join(r'/Users/dllo/Desktop/spiderScrapy/XMLY/dir', title))
		return True
	else:
		return False
		
if __name__ == '__main__':
	pool = Pool()
	start_urls = ['http://www.ximalaya.com/dq/all/{}/'.format(pn) for pn in range(1, 85)]
	pool.map(get_detail_url, [url for url in start_urls])
	# get_detail_url()



























