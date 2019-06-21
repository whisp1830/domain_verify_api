import time
import requests


def post_result(url):

	d = {
			"time":time.time(),
			"id":"000112",
			"file_url":"http://ip:port/file_2019",
			"file_md5":"xddddd"
	}

	a = requests.post(url, json=d)
	print (a.text)