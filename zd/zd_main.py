#! /usr/bin/env
# encoding:utf-8
"""
API test server
================
Author @ WUD
Date @ 2019/06/21
"""

import tornado.web
import tornado.ioloop
import requests
import time
import hashlib
import json


class test_server_method(object):
    def __init__(self):
        pass

    def post(self, url):
        d = {
            "time": time.time(),
            "id": 1,
            "file_url": "http://10.236.215.85:8888/src/domains",
            "file_md5": ""
        }
        domains = []
        with open("file_20190622160409", "r") as f:
            domains = f.readlines()

        domains_hash = hashlib.md5(domains)
        d["file_md5"] = domains_hash

        requests.post(url, d)


class srchandler(tornado.web.RequestHandler):
    def get(self):
        domains = ""
        with open("file_20190622160409", "r") as f:
            domains = f.readlines()
        for domain in domains:
            self.write(domain + "\n")


class postrsthandler(tornado.web.RequestHandler):
    def post(self):
        rst = self.request.body.decode("utf-8")
        rst = json.loads(rst)

        for key in rst:
            print key, rst[key]


if __name__ == '__main__':
    app = tornado.web.Application([
        (r'/file/file_20190622160409', srchandler),
        (r'/notify/sec/result_list', postrsthandler),
        (r'/notify/query/result_list', postrsthandler),
    ])
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
    # url = "http://10.245.146.xxx:8888/notify/path/domain_list"
    # test_server_method().post(url)
