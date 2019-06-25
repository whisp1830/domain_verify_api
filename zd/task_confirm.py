#! /usr/bin/env python
# coding:utf-8

import tornado.web
import tornado.ioloop
import hashlib
import requests
zd_IP = "localhost"
zd_PORT = 8888
sec_zd_url = "http://{ip}:{port}/notify/sec/result_list".format(ip=zd_IP, port=zd_PORT)
query_zd_url = "http://{ip}:{port}/notify/query/result_list".format(ip=zd_IP, port=zd_PORT)


class sectaskconfirmhandler(tornado.web.RequestHandler):
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


def application():
    app = tornado.web.Application(
        [(r'/sec/task_confirm/', sectaskconfirmhandler),
         (r'/query/task_confirm/', querytaskconfirmhandler)
         ])
    return app


if __name__ == '__main__':
    app = application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
