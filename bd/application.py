import tornado.ioloop
import tornado.web
import requests
import hashlib
import time
import json
<<<<<<< HEAD:application.py
import os
from post_result import post_result
=======

>>>>>>> 8f07ace8a91ccebf6647b660bd67145021322287:bd/application.py

def deal_with_domains(query_id, url):
	query_id = str(query_id)

	os.system("nohup python zd_verify.py %s &"%query_id)

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
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()