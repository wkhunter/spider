import urllib.request
from config import *
from lxml import etree
import chardet
import json

request = urllib.request.Request(URL, headers = HEADERS)

html = urllib.request.urlopen(request).read()

# byte --> str
encode_type = chardet.detect(html)
html = html.decode(encode_type['encoding'])

text = etree.HTML(html)

# 返回所有段子节点
# contains(@id, "qiushi_tag"): 模糊查询
node_list = text.xpath('//div[contains(@id, "qiushi_tag")]')

for node in node_list:
	username = node.xpath('./div/a/h2/text()')
	if username:
		username = node.xpath('./div/a/h2/text()')[0].replace('\n', '')
	else:
		username = '匿名用户'

	image = node.xpath('.//div[@class="thumb"]//@src')
	if image:
		image = node.xpath('.//div[@class="thumb"]//@src')
	else:
		image = ''

	content = node.xpath('./a/div/span/text()')[0].strip()
	item = {
		'username': username,
		'image': image,
		'content': content
	}

	with open('result.json', 'a') as f:
		f.write(json.dumps(item, ensure_ascii = False, indent = 1) + ',\n')

























