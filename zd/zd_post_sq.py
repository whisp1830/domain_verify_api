#! /usr/bin/env
# encoding:utf-8
"""
API test server
================
Author @ WUD
Date @ 2019/06/21
"""

import requests
import time
import hashlib


class test_server_method(object):
    def __init__(self):
        pass

    def post_query(self, url):
        with open("file_20190622160409", "r") as f:
            domains = f.readlines()

        domains_hash = hashlib.md5("".join(domains)).hexdigest()

        d = {
            "time": time.time(),
            "id": "0000001",
            "file_url": "http://10.236.215.85:8888/file/file_20190622160409",
            "file_md5": domains_hash
        }
        print d

        requests.post(url, json=d)

    def post_sec(self, url):
        with open("file_20190622160409", "r") as f:
            domains = f.readlines()

        domains_hash = hashlib.md5("".join(domains)).hexdigest()

        d = {
            "time": time.time(),
            "id": "0000002",
            "file_url": "http://10.236.215.85:8888/file/file_20190622160409",
            "file_md5": domains_hash
        }
        print d

        requests.post(url, json=d)


if __name__ == '__main__':
    url = "http://10.245.146.207:8888/notify/path/domain_list"
    test_server_method().post_sec(url)
    url = "http://10.245.146.207:8888/notify/path/domain_list"
    test_server_method().post_query(url)

