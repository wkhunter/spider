import requests
import xlwt
from config import HEADERS
import time

def get_one_page():
	data = {
		'first': 'true',
		'pn': '1',
		'kd': 'Python'
	}

	res = requests.post('https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false&isSchoolJob=0',
						data = data, headers = HEADERS)
	result = res.json()
	return result

def get_job_list(pageSize):
	# 创建excel对象
	excel = xlwt.Workbook()
	# 创建单元格对象
	sheet = excel.add_sheet('lagou', cell_overwrite_ok = True)
	n = 1
	for pn in [x+1 for x in range(pageSize)]:
		if pn == 1:
			is_first = 'true'
		else:
			is_first = 'false'

		data = {
			'first': is_first,
			'pn': str(pn),
			'kd': 'Python',
		}
		res = requests.post('https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E4%B8%8A%E6%B5%B7&needAddtionalResult=false&isSchoolJob=0',
						data = data, headers = HEADERS)
		time.sleep(2)
		result = res.json()
		jobs = result.get('content').get('positionResult').get('result')
		sheet.write(0, 0, 'positionName')
		sheet.write(0, 1, 'salary')
		sheet.write(0, 2, 'workYear')
		sheet.write(0, 3, 'education')
		sheet.write(0, 4, 'jobNature')
		sheet.write(0, 5, 'city')
		sheet.write(0, 6, 'companyShortName')
		sheet.write(0, 7, 'district')
		sheet.write(0, 8, 'positionLables')
		sheet.write(0, 9, 'secondType')
		sheet.write(0, 10, 'companyFullName')
		
		for job in jobs:
			sheet.write(n, 0, job['positionName'])
			sheet.write(n, 1, job['salary'])
			sheet.write(n, 2, job['workYear'])
			sheet.write(n, 3, job['education'])
			sheet.write(n, 4, job['jobNature'])
			sheet.write(n, 5, job['city'])
			sheet.write(n, 6, job['companyShortName'])
			sheet.write(n, 7, job['district'])
			sheet.write(n, 8, job['positionLables'])
			sheet.write(n, 9, job['secondType'])
			sheet.write(n, 10, job['companyFullName'])
			n += 1
	excel.save('lagou.xlsx')


def main():
	result = get_one_page()
	pageSize = result['content']['pageSize']
	time.sleep(2)	
	get_job_list(pageSize)


if __name__ == '__main__':
	main()

	

