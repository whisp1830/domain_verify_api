#encoding:utf-8
import requests
import time

#模拟对方服务器发来的请求，请求方式为POST，请求参数为BODY内的JSON
url = "http://localhost:8888/notify/path/domain_list"

d = {
		"time": time.time(),
		"id":"114514",
		"file_url":"http://10.245.146.207/verify_dns/baidu.txt",
		"file_md5":"xddddd"
	}

a = requests.post(url,json = d)
print (a.text)
