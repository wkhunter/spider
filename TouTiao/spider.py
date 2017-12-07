import requests
from config import *
import json
import time
import hashlib

def get_one_page(max_behot_time = 0, max_behot_time_tmp = 0):
	time.sleep(5)
	as_cp = get_as_cp()
	params = {
		'category': 'essay_joke',
		'utm_source': 'toutiao',
		'widen': '1',
		'max_behot_time': str(max_behot_time),
		'max_behot_time_tmp': str(max_behot_time_tmp),
		'tadrequire': 'true',
		'as': str(as_cp.get('as')),
		'cp': str(as_cp.get('cp'))
	}
	res = requests.get(START_URL, params = params, headers = HEADERS)
	result = requests.get(res.url, headers = HEADERS)
	result = result.json()
	return result
	
def parse_one_page(result):
	lists = result.get('data')
	for each in lists:
		group = each.get('group')
		item = {}
		item['content'] = group.get('content')
		item['status_desc'] = group.get('status_desc')
		item['user'] = group.get('user').get('name')
		write_to_json(item)

	# 
	has_more = result.get('has_more')
	next_time = result.get('next').get('max_behot_time')
	if has_more:
		res = get_one_page(next_time, next_time)
		parse_one_page(res)

def write_to_json(item):
	with open('duanzi.txt', 'a', encoding = 'utf-8') as f:
		f.write(json.dumps(dict(item), ensure_ascii = False, indent = 1) + ',\n')
		f.close()

def get_as_cp():
	t = str(time.time())[0:10]
	e = hex(int(t)).upper()[2:]
	i = hashlib.md5(str(int(t)).encode()).hexdigest().upper()

	if len(e) != 8:
		zz = {
			'as': '479BB4B7254C150',
			'cp': '7E0AC8874BB0985'
		}
		return zz

	n = i[:5]
	a = i[-5:]
	r = ""
	s = ""
	for i in range(5):
		s = s + n[i] + e[i]
	for j in range(5):
		r = r + e[j + 3] + a[j]
	zz = {
		'as': "A1" + s + e[-3:],
		'cp': e[0:3] + r + "E1"
	}
	return zz

if __name__ == '__main__':
	result = get_one_page()
	parse_one_page(result)



















