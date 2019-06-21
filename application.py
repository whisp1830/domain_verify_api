import tornado.ioloop
import tornado.web
import requests
import hashlib
import time
import json
from post_result import post_result

def deal_with_domains(query_id, url):
	with open(query_id,"r") as f:
		domains = f.readlines()

	with open("file_"+ query_id,"w") as f:
		for d in domains:
			f.write( d.strip() + " DNS record\n")

	d = {
			"time": time.time(),
			"id": query_id,
			"file_url":"http://ip:port/file_2019",
			"file_md5":"xddddd"
	}

	a = requests.post(url, json=d)


class MainHandler(tornado.web.RequestHandler):
    def post(self):
		code = 1
		param = self.request.body.decode('utf-8')
		param = json.loads(param)

		need_to_verify = requests.get(param['file_url']).text

		h = hashlib.md5(need_to_verify.encode("utf-8")).hexdigest()

		with open(param['id'],"w") as f:
			f.writelines(need_to_verify)

		if h != param['file_md5']:
			code = 2
		respond = {"time":param['time'],
				"code":code}
		self.write(respond)

		deal_with_domains(param['id'], 10.245.146.207)


        

def make_app():
    return tornado.web.Application([
        (r"/notify/path/domain_list", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()