#encoding:utf-8
import requests
import time
import sys
#模拟对方服务器发来的请求，请求方式为POST，请求参数为BODY内的JSON
url = "http://localhost:8888/notify/query/domain_list"

if __name__ == "__main__":
	request_id, file_name = sys.argv[1], sys.argv[2]
	d = {
		"time": time.time(),
		"id": str(request_id),
		"file_url":"http://cty.design/verify_dns/%s"%(file_name),
		"file_md5":"1abf74b788108aaa5f3ec0aa21ad399e"
		}

a = requests.post(url,json = d)
print (a.text)
