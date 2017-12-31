# -*- coding: utf-8 -*-
import urllib.request
import re
from config import *
import json
import chardet

class Spider:

	def __init__(self):
		self.page = 1
		# 爬取开关, True则继续爬取
		self.switch = True

	# 下载页面
	def loadPage(self):
		print('page = ', self.page)
		url = 'http://www.neihan8.com/article/list_5_' + str(self.page) + '.html'
		request = urllib.request.Request(url, headers = HEADERS)
		response = urllib.request.urlopen(request)
		# 获取每页html源码字符窜
		html = response.read()
		if html:
			encode_type = chardet.detect(html)
			html = html.decode(encode_type['encoding'])
			# re.S表示匹配全部字符窜内容
			pattern = re.compile('<div\sclass="f18 mb20">(.*?)</div>', re.S)
			content_list = pattern.findall(html)
			self.dealPage(content_list)
		else:
			return None

		self.page += 1
		self.loadPage()

	# 处理每页段子
	def dealPage(self, content_list):
		for item in content_list:
			item = item.replace('<p>', '').replace('</p>', '').replace('<br>', '').replace('<br />', '').strip()
			self.writePage(item)

	# 段子逐个写入文件
	def writePage(self, item):
		# print(item)
		with open('result.txt', 'a', encoding = 'utf-8') as f:
			f.write(json.dumps(item, ensure_ascii = False) + ',\n')
			f.close()

	# 控制爬虫运行
	def startWork(self):
		pass

if __name__ == '__main__':
	spider = Spider()
	spider.loadPage()





































