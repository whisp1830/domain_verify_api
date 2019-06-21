import requests


#模拟对方服务器发来的请求，请求方式为POST，请求参数为BODY内的JSON
url = "http://localhost:8888/notify/path/domain_list"

d = {
		"time":1555377063049,
		"id":"000112",
		"file_url":"http://ip:port/file_2019",
		"file_md5":"xddddd"
	}

a = requests.post(url,json = d)
print (a.text)