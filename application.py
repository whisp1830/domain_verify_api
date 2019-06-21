import tornado.ioloop
import tornado.web
import requests
import hashlib
import json
from post_result import post_result

def deal_with_domains(filename):
	#模拟对获取的域名进行简单处理
	with open(filename,"r") as f:
		domains = f.readlines()

	print ("i got here")

	with open("result_"+filename,"w") as f:
		for d in domains:
			f.write( d.strip() + " DNS record\n")


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

		deal_with_domains(param['id'])


        

def make_app():
    return tornado.web.Application([
        (r"/notify/path/domain_list", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()