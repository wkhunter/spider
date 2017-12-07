MONGO_URL='localhost'
MONGO_DB='toutiao'
MONGO_TABLE='toutiao'

GROUP_START=1
GROUP_END=20

KEYWORD='街拍'

HEADERS = {
	'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
	'Referer':'https://www.toutiao.com/ch/essay_joke/',
	'Cookie':'uuid="w:53457f85dba843e898fce35518ae2abd"; UM_distinctid=16020360571a68-0c033a961fc9e8-17396d56-fa000-1602036057253e; _ga=GA1.2.23345593.1512368900; tt_webid=6495574961011525134; WEATHER_CITY=%E5%8C%97%E4%BA%AC; CNZZDATA1259612802=1839483616-1512366920-%7C1512629892; utm_source=toutiao; __tasessionId=h1yy8hvah1512634340042; tt_webid=6495574961011525134',
	'_signature':'CSgmSgAAUwbWnuPidlZqqwkoJl'
}

START_URL = 'https://www.toutiao.com/api/article/feed'