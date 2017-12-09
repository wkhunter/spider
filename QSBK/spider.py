import chardet
import json
import threading
from queue import Queue
from lxml import etree
import requests

CRAWL_EXIT = False
PARSE_EXIT = False

class ThreadCrawl(threading.Thread):

	def __init__(self, threadName, pageQueue, dataQueue):
		super(ThreadCrawl, self).__init__()
		self.threadName = threadName
		self.pageQueue = pageQueue
		self.dataQueue = dataQueue

	def run(self):
		print('启动', self.threadName)
		while not CRAWL_EXIT:
			try:
				# 可选参数block: 
				# 1.队列为空,block为True进去阻塞状态
				# 2.队列为空,block为False:弹出异常
				page = self.pageQueue.get(False)
				url = 'https://www.qiushibaike.com/8hr/page/' + str(page) + '/'
				content = requests.get(url, headers = HEADERS)
				self.dataQueue.put(content)
			except:
				pass
		print('结束', self.threadName)

class ThreadParse(threading.Thread):
	def __init__(self, threadName, dataQueue, filename):
		super(ThreadParse, self).__init__()
		self.threadName = threadName
		self.dataQueue = dataQueue
		self.filename = filename

	def run(self):
		while not PARSE_EXIT:
			try:
				html = self.dataQueue.get(False)
				self.parse(html)
			except:
				pass

	def parse(self, html):
		pass

def main():
	# 页码队列,10个队列
	pageQueue = Queue(10)
	for i in range(1, 11):
		pageQueue.put(i)

	# 采集结果的数据队列,参数为空表示队列无限制
	dataQueue = Queue()
	# 
	filename = open('duanzi.json', 'a')
	#采集线程 
	crawlList = ['采集线程1', '采集线程2', '采集线程3']
	threadcrawl = []
	for threadName in crawlList:
		thread = ThreadCrawl(threadName, pageQueue, dataQueue)
		thread.start()
		threadcrawl.append(thread)

	# 解析线程
	parseList = ['解析线程1', '解析线程2', '解析线程3']
	threadparse = []
	for threadName in parseList:
		thread = ThreadParse(threadName, dataQueue, filename)
		thread.start()
		threadparse.append(thread)



	while not pageQueue.empty():
		pass
	# 如果pageQueue为空,采集县城退出
	global CRAWL_EXIT
	CRAWL_EXIT = True
	print('pageQueue为空')

	for thread in threadcrawl:
		thread.join()
		print('join')


if __name__ == '__main__':
	main()




# request = urllib.request.Request(URL, headers = HEADERS)

# html = urllib.request.urlopen(request).read()

# # byte --> str
# encode_type = chardet.detect(html)
# html = html.decode(encode_type['encoding'])

# text = etree.HTML(html)

# # 返回所有段子节点
# # contains(@id, "qiushi_tag"): 模糊查询
# node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')

# for node in node_list:
# 	username = node.xpath('./div/a/h2/text()')
# 	if username:
# 		username = node.xpath('./div/a/h2/text()')[0].replace('\n', '')
# 	else:
# 		username = '匿名用户'

# 	image = node.xpath('.//div[@class="thumb"]//@src')
# 	if image:
# 		image = node.xpath('.//div[@class="thumb"]//@src')
# 	else:
# 		image = ''

# 	content = node.xpath('./a/div/span/text()')[0].strip()
# 	item = {
# 		'username': username,
# 		'image': image,
# 		'content': content
# 	}

# 	with open('result.json', 'a') as f:
# 		f.write(json.dumps(item, ensure_ascii = False, indent = 1) + ',\n')


		

























