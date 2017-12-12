from selenium import webdriver
import unittest
from bs4 import BeautifulSoup as bs
import time
import json

class douyu(unittest.TestCase):
	# 初始化方法
	def setUp(self):
		self.f = open('response.txt', 'a')
		# 创建PhantomJS浏览器对象
		self.driver = webdriver.PhantomJS()

		self.count = 1

	# 测试方法以test开头
	def testDouyu(self):
		self.driver.get('https://www.douyu.com/directory/all')
		with open('response.html', 'w') as f:
			f.write(self.driver.page_source)
		while  True:
			time.sleep(1)
			print(self.count)
			soup = bs(self.driver.page_source, 'lxml')
			# 房间名, 返回列表
			names = soup.find_all('span', {'class': 'dy-name ellipsis fl'})
			# 观众人数, 返回列表
			numbers = soup.find_all('span', {'class': 'dy-num fr'})
			# zip(names, numbers): 将name和numbers两个列表合并为一个元祖
			for name, number in zip(names, numbers): 
				item = {}
				item['name'] = name.get_text()
				item['num'] = number.get_text()
				self.f.write(json.dumps(item, ensure_ascii = False) + '\n')
				print('房间名: ', name.get_text().strip(), '人数: ', number.get_text())

			# 如果在页面源码找到"下一页"为隐藏的标签则退出
			if self.driver.page_source.find('shark-pager-disable-next') != -1:
				break

			# 点击事件
			self.driver.find_element_by_class_name('shark-pager-next').click()
			self.count += 1




	# 测试结束
	def tearDown(self):
		self.f.close()
		self.driver.quit()


if __name__ == '__main__':
	# 启动测试模块
	unittest.main()

































