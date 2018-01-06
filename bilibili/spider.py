import requests
import random
from config import *
import datetime
import time
import json

def datetime_to_timestamp_in_milliseconds(d):
	def current_milli_time(): 
		return int(round(time.time() * 1000))
	return current_milli_time()

def get_userAgent(uafile):
	uas = []
	with open(uafile, 'rb') as f:
		for ua in f.readlines():
			if ua:
				uas.append(ua.decode('utf-8').strip())
	random.shuffle(uas)
	return uas

uas = get_userAgent('user_agents.txt')

def getUids():
	for m in range(99, 101):
		uids = []
		for i in range(m * 100, (m + 1) * 100):
			uids.append(i)
	return uids
# 粉丝
def getFollowers(vmid):
	pn = 1
	ua = random.choice(uas)
	headers = {
		'User-Agent': ua,
		'Referer': 'https://space.bilibili.com/' + str(vmid)
	}
	
	while 1:
		url = 'https://api.bilibili.com/x/relation/followers?vmid=' + str(vmid) + '&pn=' + str(pn) + '&ps=20'
		jscontent = requests.get(url, headers = headers, proxies = proxies).text
		dicData = json.loads(jscontent)
		if dicData.get('code') == 0:
			datalist = dicData.get('data').get('list')
			for item in datalist:
				mid = item.get('mid')
				info = personInfo(mid)	
				# getFollowers(info.get('mid'))
			pn += 1				
		else:
			break

# 关注


# 个人信息
def personInfo(uid):
	params = {
		'mid': str(uid)
	}
	ua = random.choice(uas)
	headers = {
		'User-Agent': ua,
		'Referer': 'https://space.bilibili.com/' + str(uid)
	}
	jscontent = requests.session().post('http://space.bilibili.com/ajax/member/GetInfo', headers = headers, data = params, proxies = proxies)
	print(jscontent.status_code)
	try:
		dicData = json.loads(jscontent.text)
		status = dicData['status'] if 'status' in dicData.keys() else False
		if status:
			if 'data' in dicData.keys():
				data = dicData.get('data')
				info = {
					'mid': data.get('mid'),
					'name': data.get('name'),
					'approve': data.get('approve'),
					'sex': data.get('sex'),
					'rank': data.get('rank'),
					'face': data.get('face'),
					'regtime': data.get('regtime'),
					'place': data.get('place'),
					'birthday': data.get('birthday'),
					'sign': data.get('sign'),
					'level': data.get('level_info').get('current_level'),
					'image': data.get('nameplate').get('image'),
					'exp': data.get('level_info').get('current_exp')
				}
				write_to_file(str(info))
				print('正在下载-->', info.get('name'))
				return info
		else:
			print('数据错误')

	except ValueError:
		pass

def write_to_file(item):
	with open('info.txt', 'a') as f:
		f.write(item + '\n')
		f.close()

if __name__ == '__main__':
	info = personInfo(85486475)
	getFollowers(info.get('mid'))















