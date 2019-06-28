#encoding:utf-8

import tornado.ioloop
import tornado.web
import requests
import hashlib
import time
import json
import os
from fetch import async_fetch
from tornado import gen
from verify_log import Logger


'''
	to-do list
	1. task finished notify
	2. file path
	3. id + file_path param
	4. exception wait time
	5. log file named by id
'''

def deal_with_domains_sec(request_id, file_name):
	'''
	处理对方请求的定时任务
	参数：
		request_id:   		请求的唯一ID
		file_name:			域名列表文件的读入路径
	'''
	print os.system("nohup python dns_verify/sec_verify.py %s %s & > sec_logs/task_%s.log &"%(request_id, file_name, request_id))

def deal_with_domains_query(request_id, file_name):
	'''
	处理对方请求的实时任务
	参数：
		request_id:   		请求的唯一ID
		file_name:			域名列表文件的读入路径
	'''
	print os.system("nohup python dns_verify/query_verify.py %s %s & > query_logs/task_%s.log &"%(request_id, file_name, request_id))

class ResultFileHandler(tornado.web.RequestHandler):
	'''
	根据文件名，web服务器返回文件
	'''
	@gen.coroutine
	def get(self,filename):
		print('i download file handler : ',filename)
		self.set_header ('Content-Type', 'application/octet-stream')
		self.set_header ('Content-Disposition', 'attachment; filename='+filename)
		with open("./verified_domain/" + filename,"r") as f:
			while True:
				data = f.read(1024)
				if not data:
					break
				self.write(data)
		#记得要finish
		self.finish()

class sectaskconfirmhandler(tornado.web.RequestHandler):
	'''
	通知web服务器，DNS验证程序已处理完毕定时查询的数据
	'''
	def filenameparser(self, filename):
		""":param filename
		:return
		"""
		fname = str(filename).strip()
		fname = fname.replace("file_", "")
		task_id = fname[:fname.index("_")]
		task_etime = fname[fname.index("_") + 1:]
		return task_id, task_etime

	@gen.coroutine
	def post(self):
		filename = self.request.body.decode("utf-8")
		task_id, task_ftime = "", ""
		try:
			task_id, task_ftime = self.filenameparser(filename)
		except Exception as e:
			print "file name parser error -> ", str(e)

		with open(filename, 'r') as f:
			verfied_file = "".join(f.readlines())
			file_md5 = hashlib.md5(verfied_file.encode("utf-8")).hexdigest()

		file_url = "http://{ip}:{port}/file/{filename}".format(ip=zd_IP, port=str(zd_PORT), filename=str(filename))

		d = {
			"id": task_id,
			"time": task_ftime,
			"file_url": file_url,
			"file_md5": file_md5
		}

		r = requests.post(url=sec_zd_url, json=d)
		print r.text


class querytaskconfirmhandler(tornado.web.RequestHandler):
	'''
	通知web服务器，DNS验证程序已处理完毕实时查询的数据
	'''
	@gen.coroutine
	def filenameparser(self, filename):
		""":param filename
		:return
		"""
		fname = str(filename).strip()
		fname = fname.replace("file_", "")
		task_id = fname[:fname.index("_")]
		task_etime = fname[fname.index("_") + 1:]
		return task_id, task_etime

	def post(self):
		filename = self.request.body.decode("utf-8")
		task_id, task_ftime = "", ""
		try:
			task_id, task_ftime = self.filenameparser(filename)
		except Exception as e:
			print "file name parser error -> ", str(e)

		with open(filename, 'r') as f:
			verified_file = "".join(f.readlines())
			file_md5 = hashlib.md5(verified_file.encode("utf-8")).hexdigest()

		file_url = "http://{ip}:{port}/file/{filename}".format(ip=zd_IP, port=str(zd_PORT), filename=str(filename))

		d = {
		"id": task_id,
		"time": task_ftime,
		"file_url": file_url,
		"file_md5": file_md5
		}

		r = requests.post(url=query_zd_url, json=d)
		print r.text


class MainHandler(tornado.web.RequestHandler):
	'''
	接收来自对方服务器的域名实时/非实时验证请求
	'''

	def save_file(self, request_id, need_to_verify):
		with open("./unverified_domains/" +  request_id,"w") as f:
			f.writelines(need_to_verify)

	@gen.coroutine
	def post(self,request_type):
		code = 1
		remote_ip =  self.request.remote_ip
		param = self.request.body.decode('utf-8')
		param = json.loads(param)

		need_to_verify = yield async_fetch(param['file_url'],"txt")
		if not need_to_verify:
			print ("Download Failed !")
			self.finish()

		h = hashlib.md5(need_to_verify.encode("utf-8")).hexdigest()
		if h != param['file_md5']:
			code = 2

		if code == 1:
			request_id = str(param['id'])
			self.save_file(request_id, need_to_verify)

			respond = {"time":param['time'],
						"code":code}
			self.write(respond)

			if request_type == "sec":
				deal_with_domains_sec(request_id, str(param['id']))
			elif request_type == "query":
				deal_with_domains_query(request_id, str(param['id']))
		self.finish()


def make_app():
    return tornado.web.Application([
        (r"/notify/(\w+)/domain_list", MainHandler),
        (r"/file/(\w+)", ResultFileHandler),
        (r'/sec/task_confirm/', sectaskconfirmhandler),
        (r'/query/task_confirm/', querytaskconfirmhandler)
    ])

if __name__ == "__main__":
	log = Logger('all.log',level='debug')
	app = make_app()
	app.listen(8888)
	tornado.ioloop.IOLoop.current().start()