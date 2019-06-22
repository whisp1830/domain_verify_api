#encoding:utf-8

import tornado.ioloop
import tornado.web
import requests
import hashlib
import time
import json
import os


def deal_with_domains(query_id, url):
	query_id = str(query_id)

	os.system("nohup python zd_verify.py %s &"%query_id)

class ResultFileHandler(tornado.web.RequestHandler):
	def get(self,filename):
		print('i download file handler : ',filename)
		self.set_header ('Content-Type', 'application/octet-stream')
		self.set_header ('Content-Disposition', 'attachment; filename='+filename)
		print filename
		print filename
		with open("./domain_verified/" + filename,"r") as f:
			while True:
				data = f.read(1024)
				if not data:
					break
		self.write(data)
		#记得要finish
		self.finish()



class MainHandler(tornado.web.RequestHandler):
    def post(self):
		code = 1
		remote_ip =  self.request.remote_ip
                param = self.request.body.decode('utf-8')
		print param
                param = json.loads(param)
		need_to_verify = requests.get(param['file_url']).text

		h = hashlib.md5(need_to_verify.encode("utf-8")).hexdigest()

		with open("./domain_unverified/" +  str(param['id']),"w") as f:
			f.writelines(need_to_verify)

		if h != param['file_md5']:
			code = 2
		respond = {"time":param['time'],
				"code":code}
		self.write(respond)

                deal_with_domains(param['id'], "10.236.215.85" + ":8888/notify/path/result_list")




def make_app():
    return tornado.web.Application([
        (r"/notify/path/domain_list", MainHandler),
        (r"/file/(\w+)", ResultFileHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()