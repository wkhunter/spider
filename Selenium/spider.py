from selenium import webdriver
import unittest
from bs4 import BeautifulSoup as bs

class douyu(unittest.TestCase):
	# 初始化方法
	def setUp(self):
		# 创建PhantomJS浏览器对象
		self.driver = webdriver.PhantomJS()

		self.count = 1

	# 测试方法以test开头
	def testDouyu(self):
		self.driver.get('https://www.douyu.com/directory/all')
		while  True:
			self.driver.implicitly_wait(10)
			print(self.count)
			soup = bs(self.driver.page_source, 'lxml')
			# 房间名, 返回列表
			names = soup.find_all('h3', {'class': 'ellipsis'})
			# 观众人数, 返回列表
			numbers = soup.find_all('span', {'class': 'dy-num fr'})
			# zip(names, numbers): 将name和numbers两个列表合并为一个元祖
			for name, number in zip(names, numbers): 
				print('房间名: ', name.get_text().strip(), '人数: ', number.get_text())

			# 如果在页面源码找到"下一页"为隐藏的标签则退出
			if self.driver.page_source.find('shark-pager-disable-next') != -1:
				break

			# 点击事件
			self.driver.find_element_by_class_name('shark-pager-next').click()
			self.count += 1




	# 测试结束
	def tearDown(self):
		self.driver.quit()


if __name__ == '__main__':
	# 启动测试模块
	unittest.main()

































